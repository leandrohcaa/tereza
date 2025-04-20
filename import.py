import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
import uuid
import traceback

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="d39rhapjrpv0p8",
            host="cc0gj7hsrh0ht8.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
            port="5432",
            user="u16gr8ru9c07tr",
            password="pac9d70a4c01d0615afeb08fbbcedbaaadeac4bc4a5e24d43c1cba58107e00100",
            sslmode="require"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        raise

def get_or_create_user_id(conn, username):
    try:
        with conn.cursor() as cur:
            # Check if user exists
            cur.execute("SELECT id FROM tereza.usuarios WHERE nome = %s", (username,))
            result = cur.fetchone()
            
            if result:
                return result[0]
            else:
                # Create new user
                new_id = str(uuid.uuid4())
                cur.execute("INSERT INTO tereza.usuarios (id, nome) VALUES (%s, %s)", (new_id, username))
                conn.commit()
                return new_id
    except Exception as e:
        print(f"Error in get_or_create_user_id for user {username}: {str(e)}")
        conn.rollback()
        raise

def read_excel_with_dates(file_path, sheet_names):
    results = {}
    for sheet_name in sheet_names:
        try:
            # Read Excel file without header
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            
            # Print the first few rows to help debug
            print(f"\nFirst few rows in sheet '{sheet_name}':")
            print(df.head())
            
            # Select only the columns we need (B, C, D, E, F)
            # Note: pandas uses 0-based indexing, so column B is index 1
            df = df.iloc[:, [1, 2, 3, 4, 5]]  # Select columns B, C, D, E, F
            
            # Rename columns according to specification
            df.columns = ['data', 'usuario', 'torneio', 'compras', 'premiacao']
            
            # Convert date column
            df['data'] = pd.to_datetime(df['data'], errors='coerce')
            
            # Convert numeric columns
            df['compras'] = pd.to_numeric(df['compras'], errors='coerce').fillna(0)
            df['premiacao'] = pd.to_numeric(df['premiacao'], errors='coerce').fillna(0)
            
            # Filter out rows with invalid dates
            filtered_df = df[df['data'].notna()]
            results[sheet_name] = filtered_df
            print(f"\nFound {len(filtered_df)} rows with dates in sheet '{sheet_name}'")
            
            # Print the first few rows of the filtered data
            print("\nFirst few rows of filtered data:")
            print(filtered_df.head())
            
        except Exception as e:
            print(f"Error processing sheet '{sheet_name}': {str(e)}")
            print("Full error details:", str(e))
            print("Traceback:", traceback.format_exc())
    return results

def insert_results(conn, df):
    try:
        with conn.cursor() as cur:
            for _, row in df.iterrows():
                try:
                    # Get or create user ID
                    user_id = get_or_create_user_id(conn, row['usuario'])
                    
                    # Insert game result
                    cur.execute("""
                        INSERT INTO tereza.resultados 
                        (usuario_id, data, torneio, compras, premiacao)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (usuario_id, data, torneio) DO UPDATE
                        SET compras = EXCLUDED.compras,
                            premiacao = EXCLUDED.premiacao
                    """, (
                        user_id,
                        row['data'].date(),
                        row['torneio'],
                        row['compras'],
                        row['premiacao']
                    ))
                except Exception as e:
                    print(f"Error processing row: {row.to_dict()}")
                    print(f"Error details: {str(e)}")
                    conn.rollback()
                    continue
            conn.commit()
    except Exception as e:
        print(f"Error in insert_results: {str(e)}")
        conn.rollback()
        raise

def main():
    # Specify the Excel file path and sheet names
    excel_file = "input.xlsx"  # Replace with your Excel file name
    sheet_names = [
        "ALBERTO MAGNO",
        "ANDERSON JOSE DA SILVA PORTELA",
        "BRUNO ZEBRAL",
        "BRUNO ESTEVES",
        "CARLOS BRANT",
        "DANILO BURLE",
        "DAVID BRAINERD",
        "DIEGO ARANDA",
        "FABIO RODRIGO",
        "GABRIEL VAZ",
        "GUILHERME ANDRADE",
        "GUSTAVO RODRIGUES",
        "HENRIQUE ANGELO",
        "IGOR LUIZ",
        "ITHALO ALVES",
        "JEFERSON GUSTAVO",
        "JP CURVELLO",
        "JONATAS CASTRO",
        "LUCAS AUGUSTO",
        "LUCAS LlOYD",
        "LUIS HENRIQUE ARCANJO",
        "MATEUS MARTINS",
        "MATEUS BRITO",
        "MIGUEL GARCIA",
        "OTAVIO CASEMIRO DE SA",
        "PEDRO RIBAS",
        "PEDRO LIMA",
        "RAFAEL MARTINS",
        "RAFAEL MOURA",
        "RAINER ASSIS",
        "RODRIGO PAPINI",
        "WELINGTON FERREIRA DE SOUZA",
        "WILLIAN ISRAEL",
        "LUIZ GUSTAVO ASSUNCAO",
        "PEDRO BEAUMONTE",
        "LUIZ CARLOS",
        "IGOR HENRIQUE",
        "DIEGO ALMEIDA",
        "JEFERSON CESAR"
    ]
    
    # Get database connection
    conn = None
    try:
        conn = get_db_connection()
        
        # Read and filter the Excel file
        results = read_excel_with_dates(excel_file, sheet_names)
        
        # Process each sheet
        for sheet_name, df in results.items():
            print(f"\nProcessing sheet '{sheet_name}'...")
            insert_results(conn, df)
            print(f"Successfully processed {len(df)} rows from {sheet_name}")
            
    except Exception as e:
        print(f"Error in main: {str(e)}")
        print("Traceback:", traceback.format_exc())
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main() 