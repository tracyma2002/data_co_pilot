
import dashscope

from dashscope import Generation
import re

def get_response(messages):
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               # 将输出设置为"message"格式
                               result_format='message',api_key='sk-50c104e6d0844820bf7c8f81b1a17604')
    return response
def get_sql(request):
    m = """
    from django.db import models

    class students(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.TextField(max_length=100)
        age = models.IntegerField()
        gender = models.TextField(max_length=10)

    class student_profiles(models.Model):
        profile_id = models.AutoField(primary_key=True)
        student_id = models.ForeignKey('students', on_delete=models.CASCADE, unique=True)
        address = models.TextField()
        phone = models.TextField()

    class teachers(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)  
        subject = models.CharField(max_length=100)
        
    class courses(models.Model):
        course_id = models.AutoField(primary_key=True)  # 显式定义主键
        course_name = models.TextField(max_length=100)  # 假设课程名称的最大长度为100
        teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
        
    class student_courses(models.Model):
        student_id = models.ForeignKey('students', on_delete=models.CASCADE)
        course_id = models.ForeignKey('courses', on_delete=models.CASCADE)
        class Meta:
            unique_together = ('student_id', 'course_id')
        当您需要创建或查询学生信息时，请使用students模型，并可以通过学生的id、name、age或gender字段进行过滤
        要获取或更新学生的个人资料，如address和phone，请使用student_profiles模型，并通过外键student_id与students模型关联
        在添加或修改教师信息时，请使用teachers模型，并可以通过教师的id、name或subject字段进行搜索
        创建或查询课程详情时，请使用courses模型，并可以通过课程的course_id或course_name字段进行筛选。同时，可以通过外键teacher与teachers模型关联以获取授课教师信息
        当您需要管理学生选课信息时，请使用student_courses模型。通过student_id和course_id外键字段与students和courses模型关联，并确保通过unique_together元选项保持学生与课程组合的唯一性
        在执行数据库JOIN操作时，例如查询某个学生的所有课程，可以使用Django的select_related和prefetch_related方法来优化查询性能
        student_profiles模型通过外键student_id与students模型一对一连接，所以当您在使用Django ORM查询时，要使用student_id=students.id作为关联条件
        courses模型通过外键teacher与teachers模型连接，所以当您在使用Django ORM查询时，要使用teacher=teachers.id作为关联条件
        student_courses模型通过外键student_id与students模型连接，所以要使用student_id=students.id作为连接条件
        同理，student_courses模型通过外键course_id与courses模型连接，所以要使用course_id=courses.course_id作为连接条件
        当您需要查询某个学生的所有课程时，可以通过students模型的student_course_set相关名称来访问
        如果您想查询某个课程的所有学生，可以通过courses模型的student_course_set相关名称来访问
        使用Django的ORM系统，您可以通过模型的字段和方法来构建复杂的查询，例如筛选特定年龄段的学生或特定教师授课的所有课程
        请记得，当您在Django模型中定义外键关系时，可以通过on_delete参数来指定当被引用的对象被删除时应该如何处理关联对象
        如果查找到一个人的姓名name在students表中，就不要再查询teachers表，如果查找到一个人的姓名name在teachers表中，就不要再查询students表
    再添加一个需求：你在写sql语句的时候就不要换行了比如，你原来可能写成：
    ```sql
        SELECT data_price.price
    FROM data_Price
    JOIN data_GPU ON data_Price.GPU_id = data_gpu.id
    JOIN data_Brand ON data_Price.Brand_id = data_brand.id
    WHERE data_GPU.GPU_name = 'GeForce RTX 4090'
    AND data_Brand.name = 'COLORFUL';
    ```
    但是我要你写成：
    ```sql SELECT data_price.price FROM data_Price JOIN data_GPU ON data_Price.GPU_id = data_gpu.id JOIN data_Brand ON data_Price.Brand_id = data_brand.id WHERE data_GPU.GPU_name = 'GeForce RTX 4090' AND data_Brand.name = 'COLORFUL'; ```
        很简单就是把你原来写的换行符改成空格就行
        """
    messages = [{'role': 'system', 'content': 'You are a helpful assistant who masters'
                                              ' how to translate the natural language into '
                                              'SQL which is specified for MySQL.Now i will provide you with the structure '
                                              'of my database containing my tables by giving you the class define.'
                                              '' + m}]

    # 您可以自定义设置对话轮数，当前为3
    for i in range(1):
        #user_input = input("请输入：")
        user_input = request.POST['query-question']
        messages.append({'role': 'user', 'content': user_input})
        assistant_output = get_response(messages).output.choices[0]['message']['content']
        messages.append({'role': 'assistant', 'content': assistant_output})
        print(f'用户输入：{user_input}')
        print(f'模型输出：{assistant_output}')
        print('\n')
    # 假设这是你想要提取的 SQL 语句
    sql_statement = assistant_output

    # 定义正则表达式来匹配整个 SQL 语句
    pattern = r"(.*) SELECT (.*?) .*"

    # 使用 findall 方法来查找所有匹配的 SQL 语句
    matches = re.findall(r"```sql(.+?)```", sql_statement, re.DOTALL)
    print(matches)
    # 打印匹配结果
    # 假设这是您想要替换的列表
    sql_string = "".join(matches)

    lines = sql_string.splitlines()

    # 使用列表推导式对每行进行替换操作
    # 注意这里我们添加了一个条件来检查行是否为空
    processed_lines = [line.replace('\n', ';') if line.endswith('\n') else line.replace('\n', ' ') for line in lines]

    # 将替换后的行合并成一个单一的字符串
    processed_sql_string = '\n'.join(processed_lines)

    # 打印处理后的 SQL 字符串
    print(processed_sql_string)
    return processed_sql_string


if __name__ == '__main__':
    get_sql()





