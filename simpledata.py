import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# 创建一对一关系的表
# 学生表
c.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT
)
''')

# 学生个人资料表
c.execute('''
CREATE TABLE IF NOT EXISTS student_profiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER UNIQUE,
    address TEXT,
    phone TEXT,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
)
''')

# 创建一对多关系的表
# 教师表
c.execute('''
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject TEXT NOT NULL
)
''')

# 课程表，每个教师可以教授多门课程
c.execute('''
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
)
''')

# 创建多对多关系的表
# 学生选课表
c.execute('''
CREATE TABLE IF NOT EXISTS student_courses (
    student_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (course_id) REFERENCES courses (course_id)
)
''')

# 插入数据到 students 表
students_data = [
    (1, 'Alice', 20, 'Female'),
    (2, 'Bob', 21, 'Male')
]

c.executemany('INSERT OR IGNORE INTO students (id, name, age, gender) VALUES (?, ?, ?, ?)', students_data)

# 插入数据到 student_profiles 表
student_profiles_data = [
    (1, '123 Maple Street', '555-1234'),
    (2, '456 Oak Avenue', '555-5678')
]

c.executemany('INSERT OR IGNORE INTO student_profiles (student_id, address, phone) VALUES (?, ?, ?)', student_profiles_data)

# 插入数据到 teachers 表
teachers_data = [
    (1, 'Dr. Smith', 'Mathematics')
]

c.executemany('INSERT OR IGNORE INTO teachers (id, name, subject) VALUES (?, ?, ?)', teachers_data)

# 插入数据到 courses 表
courses_data = [
    (101, 'Calculus', 1),
    (102, 'Algebra', 1)
]

c.executemany('INSERT OR IGNORE INTO courses (course_id, course_name, teacher_id) VALUES (?, ?, ?)', courses_data)

# 插入数据到 student_courses 表
student_courses_data = [
    (1, 101),
    (1, 102),
    (2, 101)
]

c.executemany('INSERT OR IGNORE INTO student_courses (student_id, course_id) VALUES (?, ?)', student_courses_data)

# 提交事务
conn.commit()

# 关闭连接
conn.close()