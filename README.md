# Flask-Postgres-Student-API


This project provides a RESTful API for managing student information using Flask and PostgreSQL. The API allows you to create, update, list, and populate student records in a database. Additionally, there is a benchmarking script for measuring query performance with and without database indexing. The index on first_name cut the execution time in half.

## Technologies Used

- **Python**
- **Flask**: 
- **PostgreSQL**
- **DBeaver**
- **psycopg2**
- **ThreadPoolExecutor**

## Project Structure

- `app.py`: Contains the main Flask application with API endpoints.
- `index.py`: Contains the benchmarking script for database indexing.

## API Endpoints

### 1. GET `/`
Returns a welcome message.

**Response:**
```json
{
    "message": "Welcome to the Student API!"
}
```

### 2. POST `/create_student`
Creates a new student record. This endpoint is intended for creating a single student record.

**Request Body:**
```json
{
    "first_name": "Arya",
    "last_name": "Gupta",
    "address": "123 Main St",
    "courses": ["Math", "Science"],
    "grades": {"Math": "A", "Science": "B"}
}
```

**Response:**
```json
{
    "id": 1
}
```

### 3. PUT `/update_student/<int:student_id>`
Updates an existing student record by student ID.

**Request Body:**
```json
{
    "first_name": "Bob",
    "last_name": "Jones",
    "address": "456 Min St",
    "courses": ["Math", "Science", "History"],
    "grades": {"Math": "A", "Science": "B", "History": "B+"}

}
```

**Response:**
```json
{
    "status": "success"
}
```

### 4. GET `/list_students`
Lists all student records.

**Response:**
```json
[
    {
        "id": 1,
        "first_name": "Arya",
        "last_name": "Gupta",
        "address": "123 Main St",
        "courses": ["Math", "Science"],
        "grades": {"Math": "A", "Science": "B"}
    },
    ...
]
```

### 5. POST `/populate_students`
Populates the database with a specified number of random student records. This endpoint is intended for rapidly populating the database to ultimately perform indexing.

**Request Body:**
```json
{
    "num_records": 1000
}
```

**Response:**
```json
{
    "status": "success",
    "records_inserted": 1000
}
```
### Helper Functions for `/populate_students`

**generate_random_string(length=10):**
Generates a random string of lowercase letters.

**generate_random_student():**
Generates random student data including first name, last name, address, courses, and grades.

**insert_student():**
Inserts a randomly generated student into the database.


## Running the Code

1. **Install Packages:**
   Install flask and psycopg2-binary
   
2. **Create a PostgreSQL database**
   Once you create your Database, create a table using the following:
   ```
    CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address TEXT,
    courses TEXT[],
    grades JSONB);
   ```
   Then, add a unique constraint:
   ```
   ALTER TABLE students ADD CONSTRAINT unique_student UNIQUE (first_name, last_name);
   ```
4. **Start Flask Application**
   ```
   python concurrent_app.py
   ```
   The API will be available at http://127.0.0.1:5000.

5. **Run the Benchmark Script**
   Once the database is sufficiently populated, to measure query performance with and without indexing, run:
   ```
   python index.py
   ```
   Here are the results of the index.py file on my database, which consisted of north of 115,000 records:
   ```
   Query time without index: 0.13237881660461426 seconds
   Query time with index: 0.05349302291870117 seconds
   ```


# Example cURL commands
Once you have ran concurrent_app.py, in a new terminal you may run the following commands:

**Create a Student**
```
curl -X POST http://127.0.0.1:5000/create_student -H "Content-Type: application/json" -d '{
    "first_name": "Arya",
    "last_name": "Gupta",
    "address": "123 Main St",
    "courses": ["Math", "Science"],
    "grades": {"Math": "A", "Science": "B"}
}'
```

**Update a Student**
```
curl -X PUT http://127.0.0.1:5000/update_student/1 -H "Content-Type: application/json" -d '{
    "first_name": "Bob",
    "last_name": "Point",
    "address": "456 Min St",
    "courses": ["Math", "Science", "History"],
    "grades": {"Math": "A", "Science": "B", "History": "B+"}
}'
```

**List Students (limited to first 100)**
```
curl -X GET "http://127.0.0.1:5000/list_students?limit=100"
```

**Populate Database**
```
curl -X POST -H "Content-Type: application/json" -d '{"num_records": 1000}' http://127.0.0.1:5000/populate_students
```
