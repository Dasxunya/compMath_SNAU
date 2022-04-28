import colors as color
import functions as f


def main():
    try:
        print(color.BLUE + "\nЧто решаем?:\n1 - одно уравнение\n2 - систему\n3 - хочу выйти")
        choice = input("> ")
        while (choice != '1') and (choice != '2') and (choice != '3'):
            print("Воспользуйтесь командами, предложенными в меню!")
            choice = input("> ")
        if choice == "1":
            answer1, answer2 = f.solve_equation()
            print(f"\nКорень уравнения:\n {answer1:.8f} (метод касательных) \n {answer2:.8f} (метод итераций)")
            print(f"\nРазница между ответами: {answer1 - answer2:.8f}")
            # print(f"Значение функции в корне: {answer[1]}")
            # print(f"Число итераций: {answer[1]}")
        elif choice == "3":
            print(color.GREEN + "\nВы успешно вышли")
            exit(0)
        else:
            x, y, system = f.solve_system()
            print(f"\nКорни уравнения: ({x:.8f}, {y:.8f}), Отличается на: ({system[0](x, y):.8f} , {system[1](x, y):.8f})")

    except KeyboardInterrupt:
        print(color.RED + "\n\nПрограмма прервана:(")
        exit(1)


main()
