open_window = False
show_time = 1


def get_windowstate():
    return open_window, show_time


def set_windowstate(value1, value2):
    global open_window, show_time
    open_window = value1  # 修改全局变量的值
    show_time = value2