from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import Json
from concurrent.futures import ThreadPoolExecutor
import random
import string

app = Flask(__name__)

db_config = {
    'dbname': 'student_db',
    'user': 'MYUSERNAME',
    'password': 'MYPASSWORD',
    'host': 'localhost'
}


def get_db_connection():
    return psycopg2.connect(**db_config)

@app.route('/', methods=['GET'])
def index():
    return "Welcome!", 200

@app.route('/create_student', methods=['POST'])
def create_student():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    address = data['address']
    courses = data['courses']
    grades = data['grades']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id FROM students WHERE first_name = %s AND last_name = %s
        """, (first_name, last_name))
    existing_student = cur.fetchone()

    if existing_student:
        student_id = existing_student[0]
        print("Student exists")
    else:
        cur.execute("""
            INSERT INTO students (first_name, last_name, address, courses, grades)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (first_name, last_name, address, courses, Json(grades)))
        student_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()

    return jsonify({'id': student_id}), 201

@app.route('/update_student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    address = data['address']
    courses = data['courses']
    grades = data['grades']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE students
        SET first_name = %s,
            last_name = %s,
            address = %s,
            courses = %s,
            grades = %s
        WHERE id = %s
        """, (first_name, last_name, address, courses, Json(grades), student_id))
    conn.commit()
    cur.close()
    conn.close()
   
    return jsonify({'status': 'success'}), 200

@app.route('/list_students', methods=['GET'])
def list_students():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, first_name, last_name, address, courses, grades FROM students")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    students = []
    for row in rows:
        student = {
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'address': row[3],
            'courses': row[4],
            'grades': row[5]
        }
        students.append(student)
   
    return jsonify(students)

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_random_student():
    first_name = generate_random_string()
    last_name = generate_random_string()
    address = generate_random_string(20)
    courses = ["course_" + generate_random_string(5) for _ in range(random.randint(1, 5))]
    grades = {course: random.randint(50, 100) for course in courses}
    return first_name, last_name, address, courses, grades


def insert_student():
    conn = get_db_connection()
    cur = conn.cursor()
    first_name, last_name, address, courses, grades = generate_random_student()
    cur.execute("""
        INSERT INTO students (first_name, last_name, address, courses, grades)
        VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, address, courses, Json(grades)))
    conn.commit()
    cur.close()
    conn.close()

@app.route('/populate_students', methods=['POST'])
def populate_students():
    num_records = request.json.get('num_records', 1000)  
    with ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(num_records):
            executor.submit(insert_student)
    return jsonify({'status': 'success', 'records_inserted': num_records}), 201

if __name__ == '__main__':
    app.run(debug=True)




