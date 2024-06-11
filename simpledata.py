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
    (1, '李明', 20, 'Male'),
    (2, '王静', 19, 'Female'),
    (3, '张强', 21, 'Male'),
    (4, '刘洋', 20, 'Female'),
    (5, '陈浩', 22, 'Male'),
    (6, '赵敏', 19, 'Female'),
    (7, '黄杰', 20, 'Male'),
    (8, '吴霞', 21, 'Female'),
    (9, '周杰', 23, 'Male'),
    (10, '徐丽', 22, 'Female'),
    (11, '孙刚', 20, 'Male'),
    (12, '朱丽', 19, 'Female'),
    (13, '罗娜', 21, 'Female'),
    (14, '高强', 22, 'Male'),
    (15, '林燕', 20, 'Female'),
    (16, '谢勇', 19, 'Male'),
    (17, '戴敏', 21, 'Female'),
    (18, '梁杰', 23, 'Male'),
    (19, '宋佳', 22, 'Female'),
    (20, '韩旭', 20, 'Male'),
    (21, '杨光', 19, 'Male'),
    (22, '郭靖', 21, 'Male'),
    (23, '梅婷', 20, 'Female'),
    (24, '蒋波', 22, 'Male'),
    (25, '蔡娟', 19, 'Female'),
    (26, '廖洋', 21, 'Male'),
    (27, '胡蝶', 23, 'Female'),
    (28, '马超', 22, 'Male'),
    (29, '何瑞', 20, 'Female'),
    (30, '吕飞', 19, 'Male')
]

c.executemany('INSERT OR IGNORE INTO students (id, name, age, gender) VALUES (?, ?, ?, ?)', students_data)

# 插入数据到 student_profiles 表
student_profiles_data = [
    (1, '北京市海淀区学院路1号', '135-1000-1111'),
    (2, '上海市浦东新区张江高科技园区2号', '135-2000-2222'),
    (3, '广州市天河区体育西路3号', '135-3000-3333'),
    (4, '深圳市南山区科技园4号', '135-4000-4444'),
    (5, '杭州市西湖区文三路5号', '135-5000-5555'),
    (6, '南京市玄武区珠江路6号', '135-6000-6666'),
    (7, '武汉市洪山区珞喻路7号', '135-7000-7777'),
    (8, '成都市武侯区科华北路8号', '135-8000-8888'),
    (9, '西安市雁塔区科技二路9号', '135-9000-9999'),
    (10, '苏州市工业园区星湖街10号', '136-1100-1111'),
    (11, '重庆市渝北区金开大道11号', '136-2200-2222'),
    (12, '长沙市岳麓区麓谷大道12号', '136-3300-3333'),
    (13, '大连市沙河口区中山路13号', '136-4400-4444'),
    (14, '青岛市崂山区松岭路14号', '136-5500-5555'),
    (15, '厦门市思明区软件园二期15号', '136-6600-6666'),
    (16, '宁波市鄞州区首南街道16号', '136-7700-7777'),
    (17, '福州市鼓楼区软件大道17号', '136-8800-8888'),
    (18, '合肥市高新区科学大道18号', '136-9900-9999'),
    (19, '昆明市五华区学府路19号', '137-0100-1111'),
    (20, '沈阳市和平区青年大街20号', '137-1200-2222'),
    (21, '哈尔滨市南岗区西大直街21号', '137-3300-3333'),
    (22, '济南市历下区经十路22号', '137-4400-4444'),
    (23, '西安市碑林区长安北路23号', '137-5500-5555'),
    (24, '广州市白云区机场路24号', '137-6600-6666'),
    (25, '成都市锦江区东大街25号', '137-7700-7777'),
    (26, '杭州市滨江区江南大道26号', '137-8800-8888'),
    (27, '武汉市武昌区中北路27号', '137-9900-9999'),
    (28, '南京市建邺区江东中路28号', '138-0100-1111'),
    (29, '重庆市渝中区解放碑步行街29号', '138-1200-2222'),
    (30, '深圳市宝安区新湖路30号', '138-3300-3333')
]

c.executemany('INSERT OR IGNORE INTO student_profiles (student_id, address, phone) VALUES (?, ?, ?)', student_profiles_data)

# 插入数据到 teachers 表
teachers_data = [
    (1, '赵强', '数学'),
    (2, '钱芳', '物理'),
    (3, '孙磊', '化学'),
    (4, '李娜', '生物'),
    (5, '周杰', '历史')
]

c.executemany('INSERT OR IGNORE INTO teachers (id, name, subject) VALUES (?, ?, ?)', teachers_data)

# 插入数据到 courses 表
courses_data = [
    (101, '高等数学I', 1),  # 赵强教授的课程
    (102, '高等数学II', 1),  # 同为赵强教授的另一门课程
    (103, '物理基础', 2),  # 钱芳老师的课程
    (104, '现代物理', 2),  # 钱芳老师的另一门课程
    (105, '有机化学', 3),  # 孙磊博士的课程
    (106, '无机化学', 3),  # 孙磊博士的另一门课程
    (107, '生物科学导论', 4)  # 李娜讲师的课程
]

c.executemany('INSERT OR IGNORE INTO courses (course_id, course_name, teacher_id) VALUES (?, ?, ?)', courses_data)

# 插入数据到 student_courses 表
student_courses_data = [
    (1, 101), (1, 102), (1, 107),
    (2, 101), (2, 103),
    (3, 103), (3, 104), (3, 105),
    (4, 105), (4, 106),
    (5, 106), (5, 107),
    (6, 101), (6, 102),
    (7, 102), (7, 104),
    (8, 103), (8, 105),
    (9, 104), (9, 106),
    (10, 105), (10, 107),
    (11, 101), (11, 103),
    (12, 102), (12, 104),
    (13, 103), (13, 105),
    (14, 104), (14, 106),
    (15, 105), (15, 107),
    (16, 101), (16, 102), (16, 106),
    (17, 102), (17, 103), (17, 107),
    (18, 103), (18, 104),
    (19, 104), (19, 105), (19, 106),
    (20, 105), (20, 107),
    (21, 101), (21, 102), (21, 104),
    (22, 102), (22, 105),
    (23, 103), (23, 106),
    (24, 104), (24, 107),
    (25, 105), (25, 101),
    (26, 106), (26, 102),
    (27, 107), (27, 103),
    (28, 101), (28, 104),
    (29, 102), (29, 105),
    (30, 103), (30, 106)
]

c.executemany('INSERT OR IGNORE INTO student_courses (student_id, course_id) VALUES (?, ?)', student_courses_data)

# 提交事务
conn.commit()

# 关闭连接
conn.close()