import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# 1. Connect to Database
db_connection = mysql.connector.connect(
  host="localHost",
  user="root",
  password="........",
  database="MyCompany"
)

cursor = db_connection.cursor()

q = "CREATE DATABASE IF NOT EXISTS MyCompany"
cursor.execute(q)

cursor.execute("USE MyCompany")

# ------------------------------------------------------
# 2. Employees Table
# ------------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(50),
    salary INT,
    hire_date DATE
)
""")

cursor.execute("SELECT COUNT(*) FROM Employees")
if cursor.fetchone()[0] == 0:
  sql = "INSERT INTO Employees (name, department, salary, hire_date) VALUES (%s, %s, %s, %s)"
  val = [
    ('Karim', 'Data Science', 8000, '2024-01-15'),
    ('Ahmed', 'HR', 4000, '2023-05-20'),
    ('Sara', 'Marketing', 5500, '2023-08-10'),
    ('Mona', 'Data Science', 7500, '2024-02-01'),
    ('Ali', 'Sales', 3000, '2022-11-05'),
    ('Omar', 'HR', 4200, '2021-06-30')
  ]
  cursor.executemany(sql, val)
  db_connection.commit()

# --------------------------------------------------
# 3. Projects Table
# --------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(50),
    emp_id INT
)
""")

cursor.execute("SELECT COUNT(*) FROM Projects")
if cursor.fetchone()[0] == 0:
  sql_projects = "INSERT INTO Projects (project_name, emp_id) VALUES (%s, %s)"
  val_projects = [
    ('AI System', 1),
    ('New Website', 3),
    ('Mobile App', 1),
    ('Cloud Database', 5),
    ('Select Project X', None)
  ]
  cursor.executemany(sql_projects, val_projects)
  db_connection.commit()

query = """
  SELECT 
    Employees.name,
    Projects.project_name
  FROM Employees
  LEFT JOIN Projects
  ON Employees.id = Projects.emp_id
"""

# -------------------------------------------------
# 4. Task
# -------------------------------------------------
df = pd.read_sql(query, db_connection)
print(df)

project_count = df.groupby('name')['project_name'].count()
print("--- Number of Projects per Employees ---")
print(project_count)

# -------------------------------------------------------
# 5. Diagram
# -------------------------------------------------------
plt.figure(figsize=(10, 6))
project_count.plot(kind='bar', color='green', edgecolor='k')

plt.title('Number of Projects per Employee', fontsize=14)
plt.xlabel('Employee Name')
plt.ylabel('Project Count')
plt.xticks(rotation=0)
plt.grid(axis='y', ls='--', alpha=0.7)

plt.show()


db_connection.close()

