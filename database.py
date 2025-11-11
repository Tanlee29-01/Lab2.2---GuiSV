import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager

# Connection pool configuration
_pool = None

def init_pool():
    """Khởi tạo connection pool một lần khi ứng dụng khởi động"""
    global _pool
    if _pool is None:
        try:
            _pool = pooling.MySQLConnectionPool(
                pool_name="library_pool",
                pool_size=5,
                pool_reset_session=True,
                host="127.0.0.1",
                user="root",
                password="LuuNhutTan120206@",
                database="library_management",
                autocommit=False
            )
            print("✓ Database connection pool đã được khởi tạo")
        except Exception as e:
            print(f"✗ Lỗi khởi tạo connection pool: {e}")
            raise
    return _pool

def get_connection():
    """Lấy connection từ pool"""
    if _pool is None:
        init_pool()
    try:
        return _pool.get_connection()
    except Exception as e:
        print(f"✗ Lỗi lấy connection từ pool: {e}")
        raise

@contextmanager
def get_db_connection():
    """Context manager để quản lý database connection"""
    conn = None
    try:
        conn = get_connection()
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()

class Database:
    def __init__(self):
<<<<<<< HEAD
        self.connection = mysql.connector.connect(
            host="127.0.0.1", 
            user="root", 
            password="29012006TanLee!", 
            database="library"
        )
=======
        self.connection = get_connection()
>>>>>>> 1b046944f0e2cdf8e6d4d1097113f9ebbae2e871
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.cursor.close()
        if self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise

    def fetch_all(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()
