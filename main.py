import sqlite3

conn = sqlite3.connect("tracker.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    task_name TEXT,
    deadline TEXT,
    status TEXT
)
""")

conn.commit()

#Add Employee
def add_employee():
    name = input("Enter employee name: ")
    department = input("Enter department: ")

    cursor.execute(
        "INSERT INTO employee (name, department) VALUES (?, ?)",
        (name, department)
    )
    conn.commit()
    print("Employee added successfully")

# Assign Task to Employee
def assign_task():
    emp_id = input("Enter employee ID: ")
    task_name = input("Enter task name: ")
    deadline = input("Enter deadline (YYYY-MM-DD): ")

    cursor.execute(
        "INSERT INTO task (employee_id, task_name, deadline, status) VALUES (?, ?, ?, ?)",
        (emp_id, task_name, deadline, "Pending")
    )
    conn.commit()
    print("Task assigned successfully")

# Update Task Status
def update_task_status():
    task_id = input("Enter task ID: ")
    status = input("Enter status (Pending / In Progress / Completed): ")

    cursor.execute(
        "UPDATE task SET status = ? WHERE id = ?",
        (status, task_id)
    )
    conn.commit()
    print("Task status updated")

# Productivity Summary
def productivity_summary():
    cursor.execute("""
    SELECT employee.name,
           SUM(CASE WHEN task.status = 'Completed' THEN 1 ELSE 0 END) AS completed,
           SUM(CASE WHEN task.status != 'Completed' THEN 1 ELSE 0 END) AS pending
    FROM employee
    JOIN task ON employee.id = task.employee_id
    GROUP BY employee.name
    """)

    results = cursor.fetchall()

    print("Task Summary:")
    for row in results:
        print(f"{row[0]} | Completed: {row[1]} | Pending: {row[2]}")


# Menu System
while True:
    print("\n1. Add Employee")
    print("2. Assign Task")
    print("3. Update Task Status")
    print("4. View Productivity Summary")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_employee()
    elif choice == "2":
        assign_task()
    elif choice == "3":
        update_task_status()
    elif choice == "4":
        productivity_summary()
    elif choice == "5":
        break
    else:
        print("Invalid choice")

