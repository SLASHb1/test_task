import numpy as np
import peewee
from tabulate import tabulate

from main import Group, Student, Subject, Teacher, TeacherSubject


def input_number(prompt):
    while True:
        try:
            num = int(input(prompt))
            break
        except ValueError:
            print('Неверный ввод')
    return num


def get_students():
    student = (Student
               .select(Student.id, Student.first_name, Student.last_name, Group.number)
               .join(Group)
               .dicts()
               .execute())
    print(tabulate(student, headers={}, tablefmt='grid'))


def get_teacher():
    teacher = (Teacher
               .select(Teacher.id, Teacher.first_name, Teacher.last_name, Subject.name)
               .join(TeacherSubject)
               .join(Subject)
               .dicts()
               .execute())
    print(tabulate(teacher, headers={}, tablefmt='grid'))


def add_group():
    while True:
        try:
            number = input_number('Введите номер группы: ')
            Group.create(number=number)
            break
        except peewee.IntegrityError:
            print('Группа с таким номером уже существует')


def add_student():
    first_name = input('Введите имя: ')
    last_name = input('Введите фамилию: ')

    while True:
        group_number = input_number('Введите номер группы: ')
        try:
            group = Group.get(Group.number == group_number)
            break
        except peewee.DoesNotExist:
            print('Группы с таким номером не существует')
    Student.create(first_name=first_name, last_name=last_name, group_id=group.id)


def add_subject():
    while True:
        try:
            name = input('Введите название: ')
            Subject.create(name=name)
            break
        except peewee.IntegrityError:
            print('Предмет с таким названием уже существует')


def add_teacher():
    first_name = input('Введите имя: ')
    last_name = input('Введите фамилию: ')
    subjects = []
    while True:
        subject_name = input('Введите название предмета для добавления (exit для выхода): ')
        if subject_name == 'exit':
            break
        try:
            s = Subject.get(name=subject_name)
            subjects.append(s)
        except peewee.DoesNotExist:
            print('Предмета с таким названием нет')
    teacher = Teacher(first_name=first_name, last_name=last_name)
    teacher.save()
    for subject in subjects:
        teacher.subjects.add(subject)


def edit_group():
    while True:
        try:
            number = input_number('Введите номер группы: ')
            group = Group.get(number=number)
            break
        except peewee.DoesNotExist:
            print('Группы с таким номером не существует')
    while True:
        new_group_number = input('Введите новый номер группы (exit для отмены): ')
        if new_group_number == 'exit':
            return
        try:
            new_group_number = int(new_group_number)
            break
        except ValueError:
            print('Введите число')
    try:
        group.number = new_group_number
        group.save()
    except peewee.IntegrityError:
        print('Группа с таким номером уже существует')


def edit_student():
    while True:
        student_id = input_number('Введите id студента: ')
        try:
            student = Student.get(id=student_id)
            break
        except peewee.DoesNotExist:
            print('Студента с данным id нет в базе')

    while True:
        choose = 0
        while choose < 1 or choose > 4:
            print('Выберете параметр для изменения: ')
            print('1. Имя')
            print('2. Фамилия')
            print('3. Группа')
            print('4. Выход')
            choose = input_number('')
        if choose == 1:
            new_first_name = input('Введите новое имя (оставьте пустым для отмены): ')
            if new_first_name:
                student.first_name = new_first_name
        elif choose == 2:
            new_last_name = input('Введите новую фамилию (оставьте пустым для отмены): ')
            if new_last_name:
                student.last_name = new_last_name
        elif choose == 3:
            new_group_number = input('Введите новый номер группы (оставьте пустым для отмены); ')
            if new_group_number:
                while True:
                    try:
                        new_group_number = int(new_group_number)
                    except ValueError:
                        print('Вы ввели не число')
                        new_group_number = input_number('')
                    try:
                        group = Group.get(number=new_group_number)
                        break
                    except peewee.DoesNotExist:
                        print('Группы с данным номером нет в базе')
                        new_group_number = input_number('')
                student.group = group.id
        elif choose == 4:
            student.save()
            break


def edit_subject():
    while True:
        try:
            name = input('Введите название предмета: ')
            subject = Subject.get(name=name)
            break
        except peewee.DoesNotExist:
            print('Предмета с таким названием не существует')

    new_subject_name = input('Введите новое название предмета (exit для отмены): ')
    if new_subject_name == 'exit':
        return
    try:
        subject.name = new_subject_name
        subject.save()
    except peewee.IntegrityError:
        print('Предмет с таким названием уже существует')


def get_subject():
    subject_name = input('Введите название предмета: ')
    try:
        s = Subject.get(name=subject_name)
        return s
    except peewee.DoesNotExist:
        print('Предмета с таким названием нет')


def edit_teacher():
    while True:
        teacher_id = input_number('Введите id преподователя: ')
        try:
            teacher = Teacher.get(id=teacher_id)
            break
        except peewee.DoesNotExist:
            print('Преподователя с данным id нет в базе')

    while True:
        choose = 0
        while choose < 1 or choose > 4:
            print('Выберете параметр для изменения: ')
            print('1. Имя')
            print('2. Фамилия')
            print('3. Предметы')
            print('4. Выход')
            choose = input_number('')
        if choose == 1:
            new_first_name = input('Введите новое имя (оставьте пустым для отмены): ')
            if new_first_name:
                teacher.first_name = new_first_name
        elif choose == 2:
            new_last_name = input('Введите новую фамилию (оставьте пустым для отмены): ')
            if new_last_name:
                teacher.last_name = new_last_name
        elif choose == 3:
            add_or_delete = 0
            while add_or_delete not in [1, 2]:
                add_or_delete = input_number('1. Добавить\n2. Удалить\n')
            subject = get_subject()
            if add_or_delete == 1:
                try:
                    teacher.subjects.add(subject)
                except peewee.IntegrityError:
                    print('Данный предмет уже есть в списке преподователя')
            elif add_or_delete == 2:
                teacher.subjects.remove(subject)

        elif choose == 4:
            teacher.save()
            break


def delete_teacher(teacher):
    TeacherSubject.delete().where(TeacherSubject.teacher_id == teacher.id).execute()
    teacher.delete_instance()


TABLE_NAME = {
    Group: 'group',
    Student: 'student',
    Subject: 'subject',
    Teacher: 'teacher',
}


def display_menu(options, table_name=None):
    if table_name:
        print(table_name)
    for i in range(len(options)):
        print(f'{i + 1}. {options[i]}')
    choice = 0
    while not np.any(choice == np.arange(len(options)) + 1):
        choice = input_number('Выберете пункт меню: ')
    return choice


def submenu(class_name, add, edit, get=None, delete=None):
    while True:
        menu_items = np.array([
            f'Get {TABLE_NAME[class_name]}s',
            f'Add {TABLE_NAME[class_name]}',
            f'Delete {TABLE_NAME[class_name]}',
            f'Edit {TABLE_NAME[class_name]}',
            'Back to main menu'
        ])
        choice = display_menu(menu_items)
        if choice == 1:
            if not get:
                query = class_name.select().dicts().execute()
                print(tabulate(query, headers={}, tablefmt='grid'))
            else:
                get()
        elif choice == 2:
            add()
        elif choice == 3:
            while True:
                try:
                    item_id = input_number(f'Enter {TABLE_NAME[class_name]} id: ')
                    obj = class_name.get(id=item_id)
                    break
                except peewee.DoesNotExist:
                    print('Записи с данным id нет в базе')
            if not delete:
                obj.delete_instance()
            else:
                delete(obj)
        elif choice == 4:
            edit()
        if choice == 5:
            break
        continue


def main_menu():
    while True:
        menu_items = np.array(["Groups", "Students", "Subjects",
                               "Teachers", "Quit"])
        choice = display_menu(menu_items)
        if choice == 1:
            submenu(Group, add_group, edit_group)
        elif choice == 2:
            submenu(Student, add_student, edit_student, get=get_students)
        elif choice == 3:
            submenu(Subject, add_subject, edit_subject)
        elif choice == 4:
            submenu(Teacher, add_teacher, edit_teacher, get=get_teacher, delete=delete_teacher)
        elif choice == 5:
            break
