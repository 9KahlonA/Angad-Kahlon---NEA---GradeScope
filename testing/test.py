import pymysql

def inspect_mysql_schema(host, port, user, password, database):
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

    try:
        cursor = conn.cursor()

        print(f"\n📦 Database: `{database}`")

        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]

        schema_info = {}

        for table in tables:
            print(f"\n🗂️ Table: `{table}`")

            cursor.execute(f"DESCRIBE `{table}`;")
            columns = cursor.fetchall()
            print("🔹 Columns:")
            for col in columns:
                print(f"   - {col[0]} ({col[1]}) {'[PK]' if col[3] == 'PRI' else ''}")

            cursor.execute(f"""
                SELECT
                    column_name,
                    referenced_table_name,
                    referenced_column_name
                FROM information_schema.key_column_usage
                WHERE referenced_table_schema = %s
                  AND table_name = %s;
            """, (database, table))
            fks = cursor.fetchall()
            if fks:
                print("🔗 Foreign Keys:")
                for fk in fks:
                    print(f"   - {fk[0]} ➜ {fk[1]}.{fk[2]}")

            cursor.execute(f"SELECT * FROM `{table}` LIMIT 5;")
            rows = cursor.fetchall()
            print(f"🔍 Sample data ({len(rows)} rows):")
            for r in rows:
                print(f"   {r}")

            schema_info[table] = {
                "columns": columns,
                "foreign_keys": fks,
                "sample_data": rows
            }

        return schema_info

    finally:
        conn.close()

schema_data = inspect_mysql_schema(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='GradescopeDev',
    database='gradescope'
)
