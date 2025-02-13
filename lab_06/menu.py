def print_menu(commands):
    """Вывод списка команд на экран"""
    print()
    for i in range(len(commands)):
        print("{0}: {1}".format(i, commands[i][0]))


def input_command(commands):
    """Ввод команды"""
    while True:
        try:
            c = int(input("Введите команду: "))
            if c < 0 or c >= len(commands):
                raise ValueError
            return c
        except ValueError:
            print("Некорректная команда")


def menu(*commands, command_exit_name="Завершить работу программы"):
    """Вызов меню с заданными командами. Команда 0 - выход"""
    commands = [(command_exit_name, exit)] + list(commands)
    while True:
        print_menu(commands)
        command = input_command(commands)  # Текущая команда
        if command == 0:
            break
        try:
            commands[command][1]()  # Вызов команды
        except Exception as e:
            print(f"Ошибка при выполнении команды: {e.__class__.__name__}: {e}")
        if len(commands[command]) > 2 and commands[command][2] == exit:
            break
