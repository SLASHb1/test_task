from peewee import *

import menu

db = SqliteDatabase('db.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class Group(BaseModel):
    id = AutoField(column_name='id')
    number = IntegerField(unique=True, verbose_name='Номер группы')

    class Meta:
        table_name = 'Group'


class Student(BaseModel):
    id = AutoField(column_name='id')
    first_name = CharField(max_length=150, verbose_name='Имя')
    last_name = CharField(max_length=150, verbose_name='Фамилия')
    group = ForeignKeyField(Group, related_name='students', verbose_name='Группа')

    class Meta:
        table_name = 'Student'


class Subject(BaseModel):
    id = AutoField(column_name='id')
    name = CharField(max_length=150, unique=True, verbose_name='Название')

    class Meta:
        table_name = 'Subject'


class Teacher(BaseModel):
    id = AutoField(column_name='id')
    first_name = CharField(max_length=150, verbose_name='Имя')
    last_name = CharField(max_length=150, verbose_name='Фамилия')
    subjects = ManyToManyField(Subject, backref='teachers')

    class Meta:
        table_name = 'Teacher'


TeacherSubject = Teacher.subjects.get_through_model()


def populate_test_data():
    from itertools import combinations
    db.create_tables([Student, Group, Subject, Teacher, TeacherSubject])

    students_groups = (
        ('Алексей', 'Лапицкий', 951006),
        ('Владислав', 'Рязанцев', 951007),
        ('Илья', 'Курбацкий', 951008))
    for first_name, last_name, group_number in students_groups:
        group = Group.create(number=group_number)
        Student.create(first_name=first_name, last_name=last_name, group_id=group.id)

    subjects_tuple = ('Русский язык', 'Математика', 'География')
    subjects_list = []
    for subject_name in subjects_tuple:
        subject = Subject.create(name=subject_name)
        subjects_list.append(subject)

    teacher_names = (
        ('Анастасия', 'Ходько'),
        ('Иван', 'Козырев'),
        ('Анатолий', 'Пучинский'),
    )
    s = combinations(subjects_list, 2)
    for first_name, last_name in teacher_names:
        teacher = Teacher.create(first_name=first_name, last_name=last_name)
        for sub in next(s):
            teacher.subjects.add(sub)


cursor = db.cursor()
if __name__ == '__main__':
    populate_test_data()
    menu.main_menu()

db.close()
