from CopyPaste import *
from EXpandData import *
from ConvertFormat import *
from MakeDataSet import *
from CheckData import *
from Crawler import *
from GetParameters import set_windowstate

def open_CopyPaste():
    main_menu.pack_forget()
    CopyPaste.pack()
    global moudle_name
    moudle_name = '贴图裁剪'


def open_ExpandData():
    main_menu.pack_forget()
    ExpandData.pack()
    global moudle_name
    moudle_name = '数据增强'


def open_ConvertFormat():
    main_menu.pack_forget()
    ConvertFormat.pack()
    global moudle_name
    moudle_name = '转换格式'


def open_MakeDataset():
    main_menu.pack_forget()
    MakeDataset.pack()
    global moudle_name
    moudle_name = '制作数据集'


def open_CheckData():
    main_menu.pack_forget()
    CheckData.pack()
    global moudle_name
    moudle_name = '检查数据集'


def open_Crawler():
    main_menu.pack_forget()
    Crawler.pack()
    global moudle_name
    moudle_name = '爬虫'


def open_Model():
    main_menu.pack_forget()
    Model.pack()
    global moudle_name
    moudle_name = '神经网络'


def return_to_main_menu():
    main_entry[moudle_name].pack_forget()
    main_menu.pack()          # 显示主菜单


def return_to_Module():
    Module_entry[call_name].pack_forget()   # 隐藏所有子菜单
    main_entry[moudle_name].pack()          # 回到上一级菜单


def submit_input():
    user_input = UI_input[call_name].get()  # 获取用户输入内容
    if call_name == 'grawler_image':
        messagebox.showwarning('警告！！！！！', '骗你的，grawler_image没有加入搜索引擎功能，developer懒得加进来了，developer要睡大觉打游戏'
                               '自己在后面弹出的设置界面手动输入网址，也能爬取图片，点开任意图片，复制图片地址输入即可'
                               '此系统皆对所有图片进行了高质量处理，提高保存图片的质量')
    if user_input:
        # run_function[call_name](user_input)
        try:
            run_function[call_name](user_input)
        except:
            messagebox.showinfo('警告', '进行任务时发生错误！\n发生错误可能有以下原因：\n'
                                      '1.输入的路径不符合规范或本地计算机不存在此路径，请确认输入的路径是否为真实路径。\n'
                                      '2.目标路径中的文件类型或内容不符合任务识别内容，任务无法正确识别目标信息，无法完成任务。\n'
                                      '3.执行无图像处理任务时，若开启了可视化界面，则会爬取网页图像，因本地启用了代理服务器，'
                                      'SSL证书验证失败导致爬取失败发生错误，关闭可视化界面即可正常完成任务。\n'
                                      '4.使用爬虫功能时，本地启用了代理服务器，请关闭代理服务器或联系开发者（hzy）帮助添加代理服务器IP。\n'
                                      '5.输入的路径为中文或特殊字符，特殊字符可能引起读取错误，请更改为标准英文路径重试。\n')
    else:
        messagebox.showwarning("警告", "输入框为空，请输入内容！")


def quit_app():
    root.destroy()


def call_ROI_buff():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(ROI_buff, text="请输入3个路径的列表\n路径格式为“待处理文件夹，背景图文件夹，存放处理后文件夹“\n"
                    "如C:/work/txt/,C:/work/ground/,C:/work/roi/", font=("Arial", 14))
    show_label.pack(pady=10)
    ROI_buff.pack()
    ack_window()
    global call_name
    call_name = 'ROI_buff'


def call_ROI_armor():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(ROI_armor, text="请输入3个路径的列表\n路径格式为“待处理文件夹，背景图文件夹，存放处理后文件夹“\n"
                    "如C:/work/txt/,C:/work/ground/,C:/work/roi/\n此功能因为日常并不会使用，因此不做维护", font=("Arial", 14))
    show_label.pack(pady=10)
    ROI_armor.pack()
    ack_window()
    global call_name
    call_name = 'ROI_armor'


def call_ROI_rock():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(ROI_rock, text="请输入3个路径的列表\n路径格式为“待处理文件夹，背景图文件夹，存放处理后文件夹“\n"
                    "如C:/work/txt/,C:/work/ground/,C:/work/roi/", font=("Arial", 14))
    show_label.pack(pady=10)
    ROI_rock.pack()
    ack_window()
    global call_name
    call_name = 'ROI_rock'


def call_ROI_to_ground():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(ROI_to_ground, text="请输入3个路径的列表\n路径格式为“待处理文件夹，背景图文件夹，存放处理后文件夹“\n"
                                         "如C:/work/txt/,C:/work/ground/,C:/work/roi/\n"
                                         "此功能为将待处理图片批量随机贴图到背景文件夹中随机图片中心\n"
                                         "此功能旨在为用户提供一个裁剪贴图的框架，用户可按需求对源码实例进行更改", font=("Arial", 14))
    show_label.pack(pady=10)
    ROI_to_ground.pack()
    ack_window()
    global call_name
    call_name = 'ROI_to_ground'


def call_change_bright():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(change_bright, text="请输入所需调整亮度的图片路径\n路径格式为’C:/Pictures/work/txt/bule.png‘\n"
                                              "此功能只能处理一张图片", font=("Arial", 14))
    show_label.pack(pady=10)
    change_bright.pack()
    ack_window()
    global call_name
    call_name = 'change_bright'


def call_brightData():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(brightData, text="请输入所需调整亮度的图片文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n"
                                           "此功能将批量处理文件夹中的图片", font=("Arial", 14))
    show_label.pack(pady=10)
    brightData.pack()
    ack_window()
    global call_name
    call_name = 'brightData'


def call_AntiColor():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(AntiColor, text="请输入所需红蓝转换的图片文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n"
                                          "此功能将批量处理文件夹中的图片", font=("Arial", 14))
    show_label.pack(pady=10)
    AntiColor.pack()
    ack_window()
    global call_name
    call_name = 'AntiColor'


def call_json_to_buff():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(json_to_buff, text="请输入文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n"
                                             "此功能将神符标签文件的json格式转成txt格式", font=("Arial", 14))
    show_label.pack(pady=10)
    json_to_buff.pack()
    ack_window()
    global call_name
    call_name = 'json_to_buff'


def call_json_to_txt():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(json_to_txt, text="请输入文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n此功能将批量将json格式转换成txt格式\n"
                                            "区别于前一个功能为只单纯提取json文件中的数据", font=("Arial", 14))
    show_label.pack(pady=10)
    json_to_txt.pack()
    ack_window()
    global call_name
    call_name = 'json_to_txt'


def call_label_add_xywh():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(label_add_xywh, text="请输入待处理文件的文件夹路径\n路径格式为’C:/work/txt/‘\n"
                          "此功能为将在正常的数据集标签框前添加xywh矩形框并生成新文件到目录下的test文件夹中", font=("Arial", 14))
    show_label.pack(pady=10)
    label_add_xywh.pack()
    ack_window()
    global call_name
    call_name = 'label_add_xywh'


def call_label_cut_xywh():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(label_cut_xywh, text="请输入待处理文件的文件夹路径\n路径格式为’C:/work/txt/‘\n"
                          "此功能为将去除数据集标签中的xywh矩形框，并直接修改原txt文件", font=("Arial", 14))
    show_label.pack(pady=10)
    label_cut_xywh.pack()
    ack_window()
    global call_name
    call_name = 'label_cut_xywh'


def call_video_to_daset():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(video_to_daset, text="请输入视频路径\n路径格式为’C:/Pictures/work/txt/‘或’C:/Pictures/work/txt/1.mp4\n"
                                               "此功能可通过批量或单个视频制作数据集", font=("Arial", 14))
    show_label.pack(pady=10)
    video_to_daset.pack()
    ack_window()
    global call_name
    call_name = 'video_to_daset'


def call_image_to_video():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(image_to_video, text="请输入图片文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n"
                                               "此功能将图片制作成视频", font=("Arial", 14))
    show_label.pack(pady=10)
    image_to_video.pack()
    ack_window()
    global call_name
    call_name = 'image_to_video'


def call_montage_video():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(montage_video, text="请输入视频集所在文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n此功能将视频集自动拼接成方形阵图，并生成新视频\n"
                                              "规定拼接顺序为索引顺序，可自行设置每个视频图像间的间隔差", font=("Arial", 14))
    show_label.pack(pady=10)
    montage_video.pack()
    ack_window()
    global call_name
    call_name = 'montage_video'


def call_connect_video():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(connect_video, text="请输入视频集所在文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n"
                          "此功能将按索引顺序将各个视频首尾连接起来，并将生成新视频", font=("Arial", 14))
    show_label.pack(pady=10)
    connect_video.pack()
    ack_window()
    global call_name
    call_name = 'connect_video'


def call_modify_classes():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(modify_classes, text="当数据集中各类定义的对象变化时，提供批量修改数据集中类的工具\n"
                          "要对txt文件中的类别进行修改需要根据自己的需求在源码中更改\n源码中已给定实例参考", font=("Arial", 14))
    show_label.pack(pady=10)
    modify_classes.pack()
    ack_window()
    global call_name
    call_name = 'modify_classes'


def call_rename_file():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(rename_file, text="请输入文件所在文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n"
                          "此功能将按设定前缀将文件批量重命名并按索引顺序排序\n若需设定其他命名规则，请自行更改源码", font=("Arial", 14))
    show_label.pack(pady=10)
    rename_file.pack()
    ack_window()
    global call_name
    call_name = 'rename_file'


def call_check_txt():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(check_txt, text="请输入文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n此功能将批量检查数据集标签\n"
                          "因为此功能用法需结合实际情况，请自行根据用途修改源码得以启用此功能\n应注意使用英文字符", font=("Arial", 14))
    show_label.pack(pady=10)
    check_txt.pack()
    ack_window()
    global call_name
    call_name = 'check_txt'


def call_check_imgsize():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(check_imgsize, text="请输入文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n"
                                              "此功能将批量检查图片尺寸并将不符合尺寸的图片变为规定尺寸", font=("Arial", 14))
    show_label.pack(pady=10)
    check_imgsize.pack()
    ack_window()
    global call_name
    call_name = 'check_imgsize'


def call_check_buffdata():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(check_buffdata, text="请输入文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n"
                                               "此功能将批量进行神符数据集校对", font=("Arial", 14))
    show_label.pack(pady=10)
    check_buffdata.pack()
    ack_window()
    global call_name
    call_name = 'check_buffdata'


def call_check_armordata():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(check_armordata, text="请输入文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n"
                                                "此功能将批量进行装甲板数据集校对", font=("Arial", 14))
    show_label.pack(pady=10)
    check_armordata.pack()
    ack_window()
    global call_name
    call_name = 'check_armordata'


def call_check_rockdata():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(check_rockdata, text="请输入文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n"
                                               "此功能将批量进行兑换框数据集校对", font=("Arial", 14))
    show_label.pack(pady=10)
    check_rockdata.pack()
    ack_window()
    global call_name
    call_name = 'check_rockdata'


def call_grawler_text():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(grawler_text, text="此模块将为用户提供爬取文本信息功能\n若用户需要使用搜索引擎，请在输入框直接输入关键字进行搜索\n"
                                             "若用户不需要使用搜索引擎，只爬取指定网址的文本信息，请输入’0‘(无需引号)\n注意:请勿随意爬取网站，"
                          "请在合法范围内使用此功能\n若用户使用此功能造成不良后果，请自行承担责任\n一切责任均与开发者无关", font=("Arial", 14))
    try:
        image_bytes = np.asarray(
            bytearray(requests.get('https://pics0.baidu.com/feed/d058ccbf6c81800afde25b68717b13f7828b4729.jpeg?token=7461a25686594efe855f1a99ee61e5f2').content),
            dtype=np.uint8)
        img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (1920, 1200))
        cv2.namedWindow('Tip', cv2.WINDOW_NORMAL)
        cv2.imshow('Tip', img)
        cv2.waitKey(0)
    except:
        messagebox.showwarning('温馨提示', '您的计算机已启用代理')
    show_label.pack(pady=10)
    grawler_text.pack()
    global call_name
    call_name = 'grawler_text'


def call_grawler_image():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(grawler_image, text="此模块将为用户提供爬取文本信息功能\n若用户需要使用搜索引擎，请在输入框直接输入关键字进行搜索\n"
                                             "若用户不需要使用搜索引擎，只爬取指定网址的文本信息，请输入’0‘(无需引号)\n注意:请勿随意爬取网站，"
                          "请在合法范围内使用此功能\n若用户使用此功能造成不良后果，请自行承担责任\n一切责任均与开发者无关", font=("Arial", 14))
    try:
        image_bytes = np.asarray(
            bytearray(requests.get('https://pics0.baidu.com/feed/d058ccbf6c81800afde25b68717b13f7828b4729.jpeg?token=7461a25686594efe855f1a99ee61e5f2').content),
            dtype=np.uint8)
        img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (1920, 1200))
        cv2.namedWindow('Tip', cv2.WINDOW_NORMAL)
        cv2.imshow('Tip', img)
        cv2.waitKey(0)
    except:
        messagebox.showwarning('温馨提示', '您的计算机已启用代理')
    show_label.pack(pady=10)
    grawler_image.pack()
    ack_window()
    global call_name
    call_name = 'grawler_image'


def ack_window():
    input_window = tk.Toplevel()
    input_window.geometry("300x200")
    input_window.title("Tip")

    def set_showtime():
        input_window.destroy()
        input_showtime = tk.Toplevel()
        input_showtime.geometry("500x380")
        input_showtime.title("显示设置")
        tk.Label(input_showtime, text="请输入可视化界面每帧图片展示时间\n输入0时，画面将持续停留在此帧\n直至获取到用户键盘的任意输入\n"
                                      "输入其他值时，如1，则每帧图片显示1毫秒\n（注意：此参数设定的时间因用户设备性能，\n"
                                      "使用状态如可视化界面大小等而定，\n可能实际显示时间要长于设定时长）\n请勿输入负数!!!\n默认显示1ms",
                 font=("Arial", 16)).pack(pady=10)
        showtime_entry = tk.Entry(input_showtime, width=30, font=("Arial", 12))
        showtime_entry.pack(pady=10)
        flag = 1

        def isopen_window():                                    # 创建提交按钮
            global flag
            flag = 0
            showtime = int(showtime_entry.get()) if showtime_entry.get() else 1
            set_windowstate(True, showtime)
            input_showtime.destroy()
        tk.Button(input_showtime, text="提交", command=isopen_window, width=20, bg="lightblue").pack(pady=10)
        input_showtime.wait_window()                          # 等待直到输入窗口关闭
        if flag:
            set_windowstate(True, 1)

    def close_window():
        set_windowstate(False, 1)
        input_window.destroy()
    tk.Label(input_window, text="是否打开任务进度可视化界面:\n(默认关闭可视化界面)", font=("Arial", 14)).pack(pady=10)
    tk.Button(input_window, text="是", command=set_showtime, width=20, bg="lightblue").pack(pady=10)
    tk.Button(input_window, text="否", command=close_window, width=20, bg="lightblue").pack(pady=10)
    input_window.wait_window()                          # 等待直到输入窗口关闭


root = tk.Tk()                                                          # 创建主窗口
root.title("DATA TOOL")
root.geometry("800x800")                                                # 窗口大小
main_menu = tk.Frame(root)                                              # 主菜单界面
tk.Label(main_menu, text="MENU", font=("Arial", 16)).pack(pady=10)
main_btn = ["贴图裁剪", "数据增强", "转换格式", "制作数据集", "检查数据集", '爬虫', '神经网络', "退出"]
main_function = [open_CopyPaste, open_ExpandData, open_ConvertFormat, open_MakeDataset, open_CheckData, open_Crawler, open_Model, quit_app]
CopyPaste, ExpandData, ConvertFormat, MakeDataset, CheckData, Crawler, Model =\
    tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
module_call = [CopyPaste, ExpandData, ConvertFormat, MakeDataset, CheckData, Crawler, Model]
main_entry = {}
show_label = None
# 主菜单按钮
for i in range(len(main_function)):
    # 父容器，按钮文本，按钮点击时调用的函数，按钮宽度，按钮背景颜色
    btn_main = tk.Button(main_menu, text=main_btn[i], command=main_function[i], width=20, bg="lightblue")
    btn_main.pack(pady=10)                                              # 按钮大小
    if i < len(module_call):
        main_entry[main_btn[i]] = module_call[i]
        tk.Label(module_call[i], text="Please select the function you want to use", font=("Arial", 14)).pack(pady=10)


CopyPaste_call = ['ROI_buff', 'ROI_armor', 'ROI_rock', "ROI_to_ground",  "返回上一级菜单"]
CopyPaste_function = [call_ROI_buff, call_ROI_armor, call_ROI_rock, call_ROI_to_ground, return_to_main_menu]

ExpandData_call = ['change_bright', 'brightData', 'AntiColor', "返回上一级菜单"]
ExpandData_function = [call_change_bright, call_brightData, call_AntiColor, return_to_main_menu]

ConvertFormat_call = ['json_to_buff', 'json_to_txt', 'label_add_xywh', 'label_cut_xywh', "返回上一级菜单"]
ConvertFormat_function = [call_json_to_buff, call_json_to_txt, call_label_add_xywh, call_label_cut_xywh, return_to_main_menu]

MakeDataset_call = ["video_to_daset", "image_to_video", "montage_video", "connect_video",
                    "modify_classes", "rename_file", "返回上一级菜单"]
MakeDataset_function = [call_video_to_daset, call_image_to_video, call_montage_video, call_connect_video,
                        call_modify_classes, call_rename_file, return_to_main_menu]

CheckData_call = ["check_txt", "check_imgsize", "check_buffdata", "check_armordata", "check_rockdata", "返回上一级菜单"]
CheckData_function = [call_check_txt, call_check_imgsize, call_check_buffdata,
                      call_check_armordata, call_check_rockdata, return_to_main_menu]

Crawler_call = ["grawler_text", "grawler_image", "返回上一级菜单"]
Crawler_function = [call_grawler_text, call_grawler_image, return_to_main_menu]

Model_call = ["返回上一级菜单"]
Model_function = [return_to_main_menu]

All_call = [CopyPaste_call, ExpandData_call, ConvertFormat_call, MakeDataset_call, CheckData_call, Crawler_call, Model_call]
All_function = [CopyPaste_function, ExpandData_function, ConvertFormat_function, MakeDataset_function, CheckData_function, Crawler_function, Model_function]
# MakeDataset菜单按钮
for i in range(len(module_call)):
    for k in range(len(All_call[i])):
        btn_submit_MakeDataset = tk.Button(module_call[i], text=All_call[i][k], command=All_function[i][k], width=20,
                                           bg="lightblue")
        btn_submit_MakeDataset.pack(pady=10)

ROI_buff, ROI_armor, ROI_rock, ROI_to_ground, to_CopyPaste =\
    tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
CopyPaste_submeum = [ROI_buff, ROI_armor, ROI_rock, ROI_to_ground, to_CopyPaste]

json_to_buff, json_to_txt, label_add_xywh, label_cut_xywh, to_ConvertFormat =\
    tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
ConvertFormat_submeum = [json_to_buff, json_to_txt, label_add_xywh, label_cut_xywh, to_ConvertFormat]

change_bright, brightData, AntiColor, to_ExpandData = tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
ExpandData_submeum = [change_bright, brightData, AntiColor, to_ExpandData]

video_to_daset, image_to_video, montage_video, connect_video, modify_classes, rename_file, to_MakeDataset =\
    tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
MakeDataset_submeum = [video_to_daset, image_to_video, montage_video, connect_video, modify_classes, rename_file, to_MakeDataset]

check_txt, check_imgsize, check_armordata, check_rockdata, check_buffdata, to_CheckData =\
    tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
CheckData_submeum = [check_txt, check_imgsize, check_buffdata, check_armordata, check_rockdata, to_CheckData]

grawler_text, grawler_image, to_Crawler = tk.Frame(root), tk.Frame(root), tk.Frame(root)
Crawler_submeum = [grawler_text, grawler_image, to_Crawler]

to_Model = tk.Frame(root)
Model_submeum = [to_Model]

ALL_submeum = [CopyPaste_submeum, ExpandData_submeum, ConvertFormat_submeum, MakeDataset_submeum, CheckData_submeum, Crawler_submeum, Model_submeum]
UI_input = {}
Module_entry = {}
All_run = [[COPYPaste().ROI_buff, COPYPaste().ROI_armor, COPYPaste().ROI_rock, COPYPaste().ROI_to_ground],
           [EXpandData().change_bright, EXpandData().brightData, EXpandData().AntiColor],
           [Format().json_to_buff, Format().json_to_txt, Format().label_add_xywh, Format().label_cut_xywh],
           [DataSet().video_to_daset, DataSet().image_to_video, DataSet().montage_video, DataSet().connect_video, DataSet().modify_classes, DataSet().rename_file],
           [CheckDaset().check_txt, CheckDaset().check_imgsize, CheckDaset().check_buffdata, CheckDaset().check_armordata, CheckDaset().check_rockdata],
           [CRawler().grawler_text, CRawler().grawler_image]]
run_function = {}

# 功能子菜单
for i in range(len(All_call)):
    for k in range(len(All_call[i])):
        if k < len(All_call[i]) - 1:
            run_function[All_call[i][k]] = All_run[i][k]
        Module_entry[All_call[i][k]] = ALL_submeum[i][k]
        UI_input[All_call[i][k]] = tk.Entry(ALL_submeum[i][k], width=30, font=("Arial", 12))
        UI_input[All_call[i][k]].pack(pady=10)
        btn_submit = tk.Button(ALL_submeum[i][k], text="提交", command=submit_input, width=20, bg="lightblue")
        btn_submit.pack(pady=10)
        btn_back = tk.Button(ALL_submeum[i][k], text="返回上一级菜单", command=return_to_Module, width=20, bg="lightgray")
        btn_back.pack(pady=10)

main_menu.pack()           # 默认显示主菜单
tk.Label(main_menu, text="未经开发者允许，严禁转载此工具，违者后果自负！\n如有疑问或发现bug，以及提出改进意见，\n请致信1795438624@qq.com反馈。\n"
                         "开发者将十分感激获得您的宝贵反馈。", font=("Arial", 18)).pack(pady=120)
messagebox.showwarning("温馨提示", "输入本地路径时，可进入到文件夹中，选定目标图片或视频等文件，使用Crtl+C复制文件，"
                               "再使用Ctrl+V粘贴到路径输入框中，将自动获取该文件路径，删去文件名以及扩展名即可获得此文件夹路径")
messagebox.showwarning("注意！！", "为避免用户疲于输入参数和弹出窗口，后续所有需要输入的参数都可直接关闭弹出的输入窗口，只需输入路径，系统会自动使用确保程序正常运行的默认参数。")
root.mainloop()            # 运行主循环


"""shutil.move(name[0] + ".txt", folder_path + "error/" + filename.split('.')[0] + ".txt")  # 在文件夹下创建一个txt文件
os.makedirs(folder_path + "error/", exist_ok=True)   # 创建文件夹
root = tk.Tk()
root.withdraw()  # 隐藏主窗口
a = simpledialog.askstring("输入", "请输入您的名字:")
# 发送HTTP请求并获取图像内容
image_bytes = np.asarray(bytearray(requests.get("https://pic.quanjing.com/28/h3/QJ5100545083.jpg@%21350h").content), dtype=np.uint8)
# 解码图像数据
image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)"""