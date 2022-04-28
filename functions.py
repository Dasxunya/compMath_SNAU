import numpy as np
import matplotlib.pyplot as plt

# input - для уравнения, input1 - для системы
FILE_IN = "C:/Users/Dasxunya/Desktop/ITMO/comp_math/lab_2/input.txt"


# TODO: подсчет производной функции
def d(n, x, f, h=0.00000001):
    if n <= 0:
        return None
    elif n == 1:
        return (f(x + h) - f(x)) / h

    return (d(n - 1, x + h, f) - d(n - 1, x, f)) / h


# TODO: подсчет значения частной производной для переменной x
def pdx(x, y, f):
    return (f(x + 0.00000001, y) - f(x, y)) / 0.00000001


# TODO: подсчет значения частной производной для переменной y
def pdy(x, y, f):
    return (f(x, y + 0.00000001) - f(x, y)) / 0.00000001


# TODO: Проверка существования предела
def check_convergence(system, x, y):
    maximum = 0
    for equation in system:
        cur_result = 0
        dx = pdx(x, y, equation)
        # print("dx: " + str(dx))
        dy = pdy(x, y, equation)
        # print("dy: " + str(dy))
        cur_result += abs(dx) + abs(dy)
        maximum = max(maximum, cur_result)
        # print("max: " + str(maximum))

    return maximum < 1


# TODO: Метод Ньютона (касательных)
def newton_method(x0, f, e, maxitr=100):
    x, x_prev, i = x0, x0 + 2 * e, 0

    while abs(x - x_prev) >= e and i < maxitr:
        x, x_prev, i = x - f(x) / d(1, x, f), x, i + 1

    return x


# TODO:Метод простой итерации  для уравнения
def iteration_method(x0, f, e, maxitr=100):
    def g(g_x):
        return g_x + (-1 / d(1, g_x, f)) * f(g_x)

    x = g(x0)
    itr = 0
    while abs(x - x0) > e and itr < maxitr:
        if d(1, x, g) >= 1:
            return None
        x0, x = x, g(x)
        itr += 1
    return x


# TODO:Метод простой итерации для системы
def iteration_method_systems2(x0, y0, system, e, maxitr=100):
    def gx(g_x, g_y):
        return g_x - system[0](g_x, g_y)

    def gy(g_x, g_y):
        return g_y - system[1](g_x, g_y)

    system1 = [lambda x, y: gx(x, y), lambda x, y: gy(x, y)]
    if not check_convergence(system1, x0, y0):
        system1 = [lambda x, y: gy(x, y), lambda x, y: gx(x, y)]
        tmp = system[0]
        system[0] = system[1]
        system[1] = tmp
        if not check_convergence(system1, x0, y0):
            return None, None
    x = gx(x0, y0)
    y = gy(x0, y0)
    itr = 0
    while abs(x - x0) > e and abs(y - y0) > e and itr < maxitr:
        x0, x = x, gx(x, y)
        y0, y = y, gy(x, y)
        itr += 1
    return x, y


# TODO: Отрисовка графика по заданным x и y
def plot(x, y):
    plt.gcf().canvas.manager.set_window_title("График функции")
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.plot(1, 0, marker=">", ms=5, color='k',
            transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, marker="^", ms=5, color='k',
            transform=ax.get_xaxis_transform(), clip_on=False)

    # Отрисовываем график
    plt.plot(x, y)
    plt.show(block=False)


def getfunc(function_num):
    if function_num == 1:
        return np.linspace(-1, 3, 200), \
               lambda x: x ** 3 - 2.92 * (x ** 2) + 1.435 * x + 0.791
    elif function_num == 2:
        return np.linspace(-3, 2, 200), \
               lambda x: x ** 3 - x + 4
    elif function_num == 3:
        return np.linspace(-20, 20, 200), \
               lambda x: np.sin(x) + 0.1
    elif function_num == 4:
        return lambda x, y: 0.1 * x ** 2 + x + 0.2 * y ** 2 - 0.3
    elif function_num == 5:
        return lambda x, y: 0.2 * x ** 2 + y - 0.1 * x * y - 0.7
    elif function_num == 6:
        return lambda x, y: x ** 2 + y ** 2 - 4
    elif function_num == 7:
        return lambda x, y: -3 * x ** 2 + y
    else:
        return None


def file_input():
    with open(FILE_IN, 'r', encoding='utf-8') as fin:
        try:
            data = {}

            function_data = getfunc(float(fin.readline().strip()))
            if function_data is None:
                raise ValueError
            x, function = function_data
            plot(x, function(x))
            data['function'] = function

            method = float(fin.readline().strip())
            if (method != 1) and (method != 2) and (method != 3):
                raise ValueError
            data['method'] = method

            if method == 1 or method == 2:
                a, b = map(float, fin.readline().strip().split())
                if a > b:
                    a, b = b, a
                elif a == b:
                    raise ArithmeticError
                elif function(a) * function(b) > 0:
                    raise AttributeError
                data['a'] = a
                data['b'] = b
            elif method == 3:
                x0 = float(fin.readline().strip())
                data['x0'] = x0

            error = float(fin.readline().strip())
            if error < 0:
                raise ArithmeticError
            data['error'] = error

            return data
        except (ValueError, ArithmeticError, AttributeError):
            return None


def manual_input():
    data = {}

    print("\nВыберите функцию.")
    print(" 1 - x³ - 2.92x² + 4.435x + 0.791")
    print(" 2 - x³ - x + 4")
    print(" 3 - sin(x) + 0.1")
    function_data = getfunc(int(input("Функция: ")))
    while function_data is None:
        print("Выберите функцию из списка.")
        function_data = getfunc(int(input("Функция: ")))
    x, function = function_data
    plot(x, function(x))
    data['function'] = function

    # print("\nВыберите метод решения.")
    # print(" 1 - Метод касательных")
    # print(" 2 - Метод простой итерации")
    # method = input("Метод решения: ")
    # while (method != '1') and (method != '2'):
    #     print("Выберите метод решения из списка.")
    #     method = input("Метод решения: ")
    # data['method'] = method

    # if method == '1' or method == '2':
    print("\nВыберите начальное приближение.")
    while True:
        try:
            x0 = float(input("Начальное приближение: "))
            break
        except ValueError:
            print("Начальное приближение должно быть числом.")
    data['x0'] = x0

    print("\nВыберите погрешность вычисления.")
    while True:
        try:
            error = float(input("Погрешность вычисления: "))
            if error <= 0:
                raise ArithmeticError
            break
        except (ValueError, ArithmeticError):
            print("Погрешность вычисления должна быть положительным числом.")
    data['error'] = error

    return data


def manual_input_systems():
    data = {}
    function = [None, None]

    print("\nВыберите 1-ую функцию")
    print("1 : 0.1x² + x + 0.2y² - 0.3")
    print("2 : 0.2x² + y - 0.1xy - 0.7")
    print("3 : x² + y² - 4")
    print("4 : -3x² + y")

    function_data = getfunc(int(input("Функция: ")) + 3)
    while function_data is None:
        print("Выберите функцию из списка.")
        function_data = getfunc(int(input("Функция: ")) + 3)
    function[0] = function_data

    print("\nВыберите 2-ую функцию")
    print("1 : 0.1x² + x + 0.2y² - 0.3")
    print("2 : 0.2x² + y - 0.1xy - 0.7")
    print("3 : x² + y² - 4")
    print("4 : -3x² + y")

    function_data = getfunc(int(input("Функция: ")) + 3)
    while function_data is None:
        print("Выберите функцию из списка.")
        function_data = getfunc(int(input("Функция: ")) + 3)
    function[1] = function_data

    data['system'] = function

    print("\nВыберите начальные приближения.")
    while True:
        try:
            x0 = float(input("Начальное приближение X: "))
            break
        except ValueError:
            print("Начальное приближение должно быть числом.")
    data['x0'] = x0

    while True:
        try:
            y0 = float(input("Начальное приближение Y: "))
            break
        except ValueError:
            print("Начальное приближение должно быть числом.")
    data['y0'] = y0

    print("\nВыберите погрешность вычисления.")
    while True:
        try:
            error = float(input("Погрешность вычисления: "))
            if error <= 0:
                raise ArithmeticError
            break
        except (ValueError, ArithmeticError):
            print("Погрешность вычисления должна быть положительным числом.")
    data['error'] = error

    return data


def file_input_systems():
    with open(FILE_IN, 'rt', encoding='utf-8') as fin:
        data = {}
        function = list([])

        function_data = getfunc(int(fin.readline().strip()) + 3)
        if function_data is None:
            raise ValueError
        function.append(function_data)

        function_data = getfunc(int(fin.readline().strip()) + 3)
        if function_data is None:
            raise ValueError
        function.append(function_data)

        data['system'] = function

        x0 = float(fin.readline().strip())
        data['x0'] = x0

        y0 = float(fin.readline().strip())
        data['y0'] = y0

        error = float(fin.readline().strip())
        if error < 0:
            raise ArithmeticError
        data['error'] = error

        return data


def solve_equation():
    print("\nВыберите режим ввода:\n1 - из файла\n2 - с клавиатуры")
    choice = input("Режим ввода: ")
    while (choice != '1') and (choice != '2'):
        print("Введите '1' или '2' для выбора способа ввода!")
        choice = input("Режим ввода: ")

    if choice == '1':
        data = file_input()
        if data is None:
            print("\nПри считывании данных из файла произошла ошибка!")
            exit(1)
        answer1 = newton_method(data['b'], data['function'], data['error'])
        answer2 = iteration_method(data['b'], data['function'], data['error'])

    else:
        data = manual_input()

        # if data['method'] == '1':
        answer1 = newton_method(data['x0'], data['function'], data['error'])
        if answer1 is None:
            print("Знаки функций и вторых производных не равны ни в 'a', ни в 'b'.")
        # elif data['method'] == '2':
        answer2 = iteration_method(data['x0'], data['function'], data['error'])
        if answer2 is None:
            print("Не выполняется условие сходимости.")
    return answer1, answer2


def solve_system():
    global answerx, answery
    print("\nВыберите режим ввода:\n1 - из файла\n2 - с клавиатуры")
    choice = input("> ")
    while (choice != '1') and (choice != '2'):
        print("Введите '1' или '2' для выбора способа ввода!")
        choice = input("> ")

    if choice == '1':
        data = file_input_systems()
        answerx, answery = iteration_method_systems2(data['x0'], data['y0'], data['system'], data['error'])
        if data is None:
            print("\nПри считывании данных из файла произошла ошибка!")
            exit(1)
    else:
        data = manual_input_systems()
        answerx, answery = iteration_method_systems2(data['x0'], data['y0'], data['system'], data['error'])
        if answerx is None:
            print("Не выполняется условие сходимости.")
            exit(1)
    return answerx, answery, data['system']
