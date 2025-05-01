import sqlite3

## Connect to sqlite
connection = sqlite3.connect("student.db")
## Create a cursor object to insert record, create table, retrieve
cursor = connection.cursor()

## Create the table
table_info = """
Create table STUDENT (NAME VARCHAR(25), CLASS VARCHAR(25),
SECTION VARCHAR(25), MARKS INT);
"""
cursor.execute(table_info)

## Insert Records
cursor.execute('''Insert Into STUDENT values('Krishna', 'Data Science', 'A', 90)''')
cursor.execute('''Insert Into STUDENT values('Darius', 'Data Science', 'B', 100)''')
cursor.execute('''Insert Into STUDENT values('Sailu', 'Data Science', 'A', 86)''')
cursor.execute('''Insert Into STUDENT values('James', 'DevOps', 'A', 70)''')
cursor.execute('''Insert Into STUDENT values('Raj', 'DevOps', 'A', 80)''')
cursor.execute('''Insert Into STUDENT values('Priya', 'DevOps', 'B', 80)''')

## Display all the records
print("The inserted records are")
data = cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

    ## Close the connection
connection.commit()
connection.close()

