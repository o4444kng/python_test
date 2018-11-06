# 2018-10-20txt格式数据，目前理解一般都是整体操作，不能对其中数据单独操作；但如果是大量数据，那就应该是对其中数据逐条处理。
import json
import os

path = '/students.txt'

def menu():
    menu_info = '''＋－－－－－－－－－－－－－－－－－－－－－－＋
｜　１）添加学生信息　　　　　　　　　　　　　｜
｜　２）显示所有学生的信息　　　　　　　　　　｜
｜　３）删除学生信息　　　　　　　　　　　　　｜
｜　４）修改学生信息　　　　　　　　　　　　　｜
｜　５）按学生成绩高－低显示学生信息　　　　　｜
｜　６）按学生成绩低－高显示学生信息　　　　　｜
｜　７）按学生年龄高－低显示学生信息　　　　　｜
｜　８）按学生年龄低－高显示学生信息　　　　　｜
｜ ９）保存学生信息到文件（students.txt)   ｜
｜ １０）从文件中读取数据（students.txt)   ｜
｜ 退出：其他任意按键＜回车＞              ｜

＋－－－－－－－－－－－－－－－－－－－－－－＋
'''
    print(menu_info)


class Student(object):
    def __init__(self, name=None, age=None, score=None):
        self.name = name
        self.age = age
        self.score = score


def student_json(student):
    return {'name': student.name, 'age': student.age, 'score':student.score}


def student_handle(dict):
    return Student(dict['name'], dict['age'], dict['score'])


def get_need_change():
    change_result = input('是否同意修改:Y/N ')
    while change_result != 'Y' and change_result != 'N':
        print('请输入')
        change_result = input('是否同意修改:Y/N ')
    if change_result == 'Y':
        return True
    else:
        return False


def get_input_digit(input_reminder_message='', error_message=''):
    if isinstance(input_reminder_message, str):
        while True:
            input_str = input(input_reminder_message)
            if not input_str:
                return None
            if not input_str.isdigit():
                if not error_message:
                    error_message = '输入的信息必须为数字'
                print(error_message)
            else:
                return int(input_str)
    else:
        raise Exception('input_reminder_message必须是字符串')


def add_student_by(student_list=None):

    if student_list is None:
        student_list = []

    name_list = []
    for student in student_list:
        name_list.append(student.name)

    while True:

        name = input('请输入学生姓名:')
        if not name:
            break

        exsit_need_change = False
        if name in name_list:
            print('已存在该学生姓名')
            exsit_need_change = get_need_change()
            if not exsit_need_change:
                break

        name_list.append(name)

        student = Student()
        student.name = name
        age = get_input_digit('请输入学生年龄:')
        score = get_input_digit('请输入学生分数:')

        if age is None or score is None:
            return student_list
        else:
            student.age = age
            student.score = score

        if exsit_need_change:
            index = name_list.index(name)
            student_list[index] = student
        else:
            student_list.append(student)

    return student_list


def show_student(student_list):

    if not student_list:
        print('---学生信息列表为空---')
        return
    print('名字'.center(8), '年龄'.center(4), '成绩'.center(4))

    for student in student_list:
        print(student.name.center(10), str(student.age).center(5), str(student.score).center(5))


def del_student(student_list):

    if not student_list:
        print('---学生信息列表为空---')
        return student_list

    del_name = input('请输入需要删除的学生姓名:')
    if not del_name:
        return student_list

    for student in student_list:
        if del_name == student.name:
            student_list.remove(student)
            print('成功删除%s学生信息' % del_name)
            return student_list

    print('未能找到需要删除的学生姓名:%s' % del_name)
    return student_list


def modi_student(student_list):

    if not student_list:
        print('---学生信息列表为空---')
        return student_list

    modi_name = input('请输入需要修改学生的姓名:')
    if not modi_name:
        return student_list

    for student in student_list:
        if modi_name == student.name:
            student.age = get_input_digit('请输入学生年龄')
            student.score = get_input_digit('请输入学生分数')
            return student_list

    print('未能找到需要修改的学生姓名:%s' % modi_name)
    return student_list


def sort_by_student(student_list, sort_name='', sort_order=''):
    sort_student_list = student_list
    if sort_name == 'age' and sort_order == 'ascend':
        sort_student_list = sorted(student_list, key=lambda x:x.age, reverse=False)
    elif sort_name == 'age' and sort_order == 'descend':
        sort_student_list = sorted(student_list, key=lambda x:x.age, reverse=True)
    elif sort_name == 'score' and sort_order == 'ascend':
        sort_student_list = sorted(student_list, key=lambda x:x.score, reverse=False)
    elif sort_name == 'score' and sort_order == 'descend':
        sort_student_list = sorted(student_list, key=lambda x:x.score, reverse=True)
    else:
        print('请输入正确的关键字')
    return sort_student_list


def write_student(student_list):
    student_list_json = json.dumps(student_list, default=student_json)
    filepath = os.path.abspath('.') + path
    with open(filepath, 'w', encoding='UTF-8') as f:
        f.write(student_list_json)
        f.close()


def read_student():
    filepath = os.path.abspath('.') + path
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='UTF-8') as f:
        read_result = f.read()
        if read_result is None:
            return []
        student_list = json.loads(read_result, object_hook=student_handle)
        return student_list


def main():
    menu()

    while True:
        operation_str = input('')
        operation_list = []
        for index in range(1, 11):
            operation_list.append(str(index))
        if operation_str not in operation_list:
            return

        student_list = read_student()

        if operation_str == '1':
            student_list = add_student_by(student_list)
            write_student(student_list)
        elif operation_str == '2':
            show_student(student_list)
        elif operation_str == '3':
            student_list = del_student(student_list)
            write_student(student_list)
        elif operation_str == '4':
            student_list = modi_student(student_list)
            write_student(student_list)
        elif operation_str == '5':
            sort_student_list = sort_by_student(student_list, 'score', 'descend')
            show_student(sort_student_list)
        elif operation_str == '6':
            sort_student_list = sort_by_student(student_list, 'score', 'ascend')
            show_student(sort_student_list)
        elif operation_str == '7':
            sort_student_list = sort_by_student(student_list, 'age', 'descend')
            show_student(sort_student_list)
        elif operation_str == '8':
            sort_student_list = sort_by_student(student_list, 'age', 'ascend')
            show_student(sort_student_list)
        elif operation_str == '9':
            write_student(student_list)
        elif operation_str == '10':
            student_list = read_student()
            show_student(student_list)
        else:
            return


if __name__ == '__main__':
    main()