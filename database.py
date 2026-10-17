import sqlite3

DB_FILE = "tasks.db"

# testlerde ayni connection'i kullanmak icin bi trick
# normalde None, test sirasinda set ediyorum
_shared_conn = None


def get_connection(db_name=None):
    """db baglantisi ac"""
    global _shared_conn
    if _shared_conn is not None:
        return _shared_conn
    conn = sqlite3.connect(db_name or DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def set_shared_connection(conn):
    """testlerde kullanmak icin disardan conn atiyorum"""
    global _shared_conn
    _shared_conn = conn


def clear_shared_connection():
    global _shared_conn
    _shared_conn = None


def init_db(db_name=None):
    """tasks tablosunu olustur, varsa dokunma"""
    conn = get_connection(db_name)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()


def add_task(description, db_name=None):
    """yeni gorev ekle, id dondur"""
    conn = get_connection(db_name)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (description) VALUES (?)", (description,))
    conn.commit()
    return cur.lastrowid


def delete_task(task_id, db_name=None):
    """gorevi sil, basariliysa True"""
    conn = get_connection(db_name)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return cur.rowcount > 0


def get_tasks(db_name=None):
    """butun gorevleri getir"""
    conn = get_connection(db_name)
    cur = conn.cursor()
    cur.execute("SELECT id, description, completed FROM tasks")
    return cur.fetchall()


def get_task(task_id, db_name=None):
    """tek gorev getir, yoksa None"""
    conn = get_connection(db_name)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, description, completed FROM tasks WHERE id = ?",
        (task_id,)
    )
    return cur.fetchone()


def complete_task(task_id, db_name=None):
    """gorevi tamamlandi yap"""
    conn = get_connection(db_name)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    return cur.rowcount > 0