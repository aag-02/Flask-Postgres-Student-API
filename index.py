import psycopg2
import time

db_config = {
    'dbname': 'student_db',
    'user': 'MYUSERNAME',
    'password': 'MYPASSWORD',
    'host': 'localhost'
}

def get_db_connection():
    return psycopg2.connect(**db_config)

def measure_query_time(query):
    start_time = time.time()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query)
    cur.fetchall()
    cur.close()
    conn.close()
    return time.time() - start_time

def create_index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_first_name ON students(first_name)")
   # cur.execute("CREATE INDEX IF NOT EXISTS idx_last_first_name ON students(last_name, first_name)")

    conn.commit()
    cur.close()
    conn.close()

def drop_index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DROP INDEX IF EXISTS idx_first_name")
    #cur.execute("DROP INDEX IF EXISTS idx_last_first_name")
    conn.commit()
    cur.close()
    conn.close()

def benchmark():
    #query = "SELECT * FROM students WHERE first_name ILIKE '%soa%' AND last_name ILIKE '%d%'"
    query = "SELECT * FROM students WHERE first_name ILIKE '%soa%' ORDER BY first_name"

    time_without_index = measure_query_time(query)
    print(f"Query time without index: {time_without_index} seconds")

    create_index()
    time_with_index = measure_query_time(query)
    print(f"Query time with index: {time_with_index} seconds")

    drop_index()

if __name__ == '__main__':
    benchmark()

