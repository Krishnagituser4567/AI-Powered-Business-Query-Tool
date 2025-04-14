import pyodbc
import json

def fetch_sql_server_metadata(server, database):
    """
    Connect to a local SQL Server and fetch table metadata.
    """
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    )
    cursor = conn.cursor()

    # Fetch table schemas
    cursor.execute("""
        SELECT TABLE_SCHEMA, TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
    """)
    tables = cursor.fetchall()

    tables_json = []
    for schema, table in tables:
        cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}'
        """)
        column_meta = cursor.fetchall()
        columns = [{"name": col[0], "datatype": col[1]} for col in column_meta]

        try:
            query = f"SELECT TOP 5 * FROM [{schema}].[{table}]"
            cursor.execute(query)
            col_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            sample_data = [dict(zip(col_names, row)) for row in rows]
        except Exception as e:
            sample_data = []

        tables_json.append({
            "table_name": f"{schema}.{table}",
            "columns": columns,
            "sample_data": sample_data
        })

    return json.dumps(tables_json, indent=4, default=str)