import mysql.connector
from datetime import datetime

# -------------------- DATABASE CONNECTION --------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="schoolmangement"
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f" Error: {err}")
    exit()

# -------------------- TABLE CREATION --------------------
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        class VARCHAR(20),
        age INT,
        gender VARCHAR(10)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        teacher_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        subject VARCHAR(50)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        date DATE,
        status VARCHAR(10),
        FOREIGN KEY(student_id) REFERENCES students(student_id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        subject VARCHAR(50),
        marks INT,
        FOREIGN KEY(student_id) REFERENCES students(student_id)
    )""")

    conn.commit()

# -------------------- STUDENT FUNCTIONS --------------------
def add_student():
    name = input("Enter student name: ")
    student_class = input("Enter class: ")
    while True:
        try:
            age = int(input("Enter age: "))
            break
        except ValueError:
            print(" Please enter a valid number for age.")
    gender = input("Enter gender (M/F): ").upper()
    cursor.execute("INSERT INTO students (name, class, age, gender) VALUES (%s, %s, %s, %s)",
                   (name, student_class, age, gender))
    conn.commit()
    print(" Student added!")

def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    print("\n--- All Students ---")
    print("ID\tName\t\t\tClass\tAge\tGender")
    for row in rows:
        print(f"{row[0]}\t{row[1]:20}\t{row[2]}\t{row[3]}\t{row[4]}")

# -------------------- TEACHER FUNCTIONS --------------------
def add_teacher():
    name = input("Enter teacher name: ")
    subject = input("Enter subject: ")
    cursor.execute("INSERT INTO teachers (name, subject) VALUES (%s, %s)", (name, subject))
    conn.commit()
    print(" Teacher added!")

def view_teachers():
    cursor.execute("SELECT * FROM teachers")
    rows = cursor.fetchall()
    print("\n--- All Teachers ---")
    print("ID\tName\t\t\tSubject")
    for row in rows:
        print(f"{row[0]}\t{row[1]:20}\t{row[2]}")

# -------------------- ATTENDANCE FUNCTIONS --------------------
def mark_attendance():
    student_id = input("Enter Student ID: ")
    date = datetime.today().strftime('%Y-%m-%d')

    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    if cursor.fetchone() is None:
        print(" Student ID not found.")
        return

    status = input("Enter status (Present/Absent): ").capitalize()
    cursor.execute("SELECT * FROM attendance WHERE student_id = %s AND date = %s", (student_id, date))
    if cursor.fetchone():
        print("Attendance already marked for today.")
    else:
        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
                       (student_id, date, status))
        conn.commit()
        print(" Attendance marked!")

def view_attendance():
    cursor.execute("""
        SELECT a.id, s.student_id, s.name, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        ORDER BY a.date DESC
    """)
    rows = cursor.fetchall()
    print("\n--- Attendance Records ---")
    print("ID\tStudent ID\tName\t\t\tDate\t\tStatus")
    for row in rows:
        print(f"{row[0]}\t{row[1]}\t\t{row[2]:20}\t{row[3]}\t{row[4]}")


def view_attendance_summary():
    cursor.execute("""
        SELECT 
            s.student_id,
            s.name,
            SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS PresentCount,
            SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) AS AbsentCount
        FROM students s
        LEFT JOIN attendance a ON s.student_id = a.student_id
        GROUP BY s.student_id, s.name
        ORDER BY s.student_id
    """)
    rows = cursor.fetchall()

    print("\n--- Attendance Summary Per Student ---")
    print("Student ID\tName\t\t\tPresent\tAbsent")
    for row in rows:
        print(f"{row[0]}\t\t{row[1]:20}\t{row[2]}\t{row[3]}")

# -------------------- MARKS FUNCTIONS --------------------
def add_marks():
    student_id = input("Enter Student ID: ")

    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    if cursor.fetchone() is None:
        print(" Student ID not found.")
        return

    subject = input("Enter subject: ")
    while True:
        try:
            marks = int(input("Enter marks: "))
            break
        except ValueError:
            print(" Please enter a valid number.")
    cursor.execute("INSERT INTO marks (student_id, subject, marks) VALUES (%s, %s, %s)",
                   (student_id, subject, marks))
    conn.commit()
    print(" Marks added!")

def view_marks():
    cursor.execute("""
        SELECT m.id, s.student_id, s.name, m.subject, m.marks
        FROM marks m
        JOIN students s ON m.student_id = s.student_id
    """)
    rows = cursor.fetchall()
    print("\n--- Marks Records ---")
    print("ID\tStudent ID\tName\t\t\tSubject\t\tMarks")
    for row in rows:
        print(f"{row[0]}\t{row[1]}\t\t{row[2]:20}\t{row[3]:10}\t{row[4]}")

# -------------------- MAIN MENU --------------------
def main_menu():
    create_tables()
    while True:
        print("\n===== SCHOOL MANAGEMENT MENU =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Add Teacher")
        print("4. View Teachers")
        print("5. Mark Attendance")
        print("6. View Attendance")
        print("7. Add Marks")
        print("8. View Marks")
        print("9. View Attendance Summary")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            add_teacher()
        elif choice == "4":
            view_teachers()
        elif choice == "5":
            mark_attendance()
        elif choice == "6":
            view_attendance()
        elif choice == "7":
            add_marks()
        elif choice == "8":
            view_marks()
        elif choice == "9":
            view_attendance_summary()
        elif choice == "10":
            print(" Goodbye! Exiting...")
            break
        else:
            print(" Invalid option. Try again!")

# -------------------- RUN APP --------------------
try:
    main_menu()
finally:
    cursor.close()
    conn.close()
