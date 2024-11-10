import mariadb
import os

db_config = {
    'user':     'app',
    'password': 'Y7Yhg%tvbP$c2',
    'host':     'localhost',
    'database': 'inhibi_scan',
    'port': 3307
}

class BaseModel:
    def __init__(self, table_name):
        self.table_name = table_name
        self.conn = mariadb.connect(**db_config)
        self.conn.autocommit = True
        self.c = self.conn.cursor(dictionary=True)

    def create_table(self, columns):
        columns_def = ', '.join(f"{col} {dtype}" for col, dtype in columns.items())
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INT PRIMARY KEY AUTO_INCREMENT, 
            {columns_def}, 
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            modified_date DATETIME DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
            is_active tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
            is_delete tinyint(1) UNSIGNED NOT NULL DEFAULT 0
        )
        """
        self.c.execute(query)

    def create(self, data, unique_field=None):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

        try:
            self.c.execute(query, tuple(data.values()))
            self.conn.commit()
            return {'success': True, 'id': self.c.lastrowid}
        except mysql.connector.IntegrityError:
            unique_value = data.get(unique_field)
            return {'success': False, 'msg': f"خطا: {unique_field} '{unique_value}' قبلاً ثبت شده است."}

    def read(self, conditions):
        where_clause = ' AND '.join([f"{col} = %s" for col in conditions.keys()])
        query = f"SELECT * FROM {self.table_name} WHERE {where_clause}"
        params = tuple(conditions.values())
        self.c.execute(query, params)
        row = self.c.fetchone()
        return row if row else None

    def update(self, data, conditions):
        set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
        where_clause = ' AND '.join([f"{col} = %s" for col in conditions.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {where_clause}"
        params = tuple(data.values()) + tuple(conditions.values())
        self.c.execute(query, params)
        self.conn.commit()
        return self.c.rowcount

    def delete(self, conditions):
        where_clause = ' AND '.join([f"{col} = %s" for col in conditions.keys()])
        query = f"DELETE FROM {self.table_name} WHERE {where_clause}"
        params = tuple(conditions.values())
        self.c.execute(query, params)
        self.conn.commit()
        return self.c.rowcount

    def fetch_all(self,  draw: int = 1,page: int = 1, limit: int = 10, conditions: dict = None, order: str = None) -> dict:
        offset = (page - 1) * limit

        self.c.execute(f"SELECT COUNT(*) AS total FROM {self.table_name}")
        records_total = self.c.fetchone()['total']

        query = f"SELECT * FROM {self.table_name}"
        params = []

        if conditions:
            where_clause = ' AND '.join([f"{col} = %s" for col in conditions.keys()])
            query += f" WHERE {where_clause}"
            params.extend(conditions.values())

        filter_query = f"SELECT COUNT(*) AS total_filtered FROM {self.table_name} WHERE {where_clause}" if conditions else f"SELECT COUNT(*) AS total_filtered FROM {self.table_name}"
        self.c.execute(filter_query, tuple(params))
        records_filtered = self.c.fetchone()['total_filtered']

        if order:
            query += f" ORDER BY {order}"

        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        self.c.execute(query, tuple(params))
        rows = self.c.fetchall()

        return {
            'draw':draw,
            'data': rows,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered
        }

    def close_connection(self):
        self.conn.close()
