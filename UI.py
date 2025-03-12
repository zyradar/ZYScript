from CopyPaste import *
from EXpandData import *
from ConvertFormat import *
from MakeDataSet import *
from CheckData import *
from Crawler import *
from GetParameters import set_windowstate
from NeuralNetwork import *
from DeCompress import*
from SystemTool import *
from tkinter import filedialog

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


def open_SystemTools():
    global password
    password = None
    askpassword = tk.Tk()
    askpassword.geometry("400x300")
    askpassword.title("权限获取")
    askpermission = tk.Frame(askpassword)
    askpermission.pack()
    tk.Label(askpermission, text="您无使用权限\n请输入密码获取权限", font=("Arial", 18)).pack(pady=20)
    password_entry = tk.Entry(askpermission, width=15, font=("Arial", 20))
    password_entry.pack(pady=20)

    def get_password(event=None):
        getpassword = password_entry.get()
        global password
        if getpassword == 'zy666':
            password = True
        else:
            messagebox.showwarning('温馨提示', '密码错误，无权限')
            password = None
        askpassword.destroy()

    password_entry.bind("<Return>", get_password)
    btn_submit = tk.Button(askpermission, text="提交", command=get_password, width=10, font=("Arial", 18), bg="lightblue")
    btn_submit.pack(pady=20)
    askpermission.wait_window()
    if not password:
        return None
    main_menu.pack_forget()
    SystemTools.pack()
    global moudle_name
    moudle_name = '系统工具'


def open_Crawler():
    main_menu.pack_forget()
    Crawler.pack()
    global moudle_name
    moudle_name = '爬虫'


def open_NeuralNetwork():
    main_menu.pack_forget()
    NeuralNetwork.pack()
    global moudle_name
    moudle_name = '神经网络'


def open_Decompress():
    main_menu.pack_forget()
    Decompress.pack()
    global moudle_name
    moudle_name = '解压压缩'


def open_CheckUpdate():
    main_menu.pack_forget()
    CheckUpdate.pack()
    messagebox.showwarning("温馨提示", "因版本更新所下载的安装包,将保存在./site_package文件夹下。可在run.log文件中查看安装信息,"
                                   "其中记录安装包名及其下载地址。若在更新过程中安装包下载失败，可自行手动打开下载链接，将目标库下载到./site_package文件夹下。"
                                   "若在更新过程中安装包已成功下载，但在安装过程中失败，可手动将./site_package中的安装包，解压到./_internal中。再次尝试打开该系统即可")
    global moudle_name
    moudle_name = '检查更新'


def open_deepseek():
    main_menu.pack_forget()
    Deepseek.pack()
    global moudle_name
    moudle_name = 'deepseek'


def return_to_main_menu():
    main_entry[moudle_name].pack_forget()
    main_menu.pack()          # 显示主菜单


def return_to_Module():
    Module_entry[call_name].pack_forget()   # 隐藏所有子菜单
    main_entry[moudle_name].pack()          # 回到上一级菜单


def jump_to_main_menu():
    Module_entry[call_name].pack_forget()   # 隐藏所有子菜单
    main_entry[moudle_name].pack_forget()   # 隐藏所有模块菜单
    main_menu.pack()


def select_path():
    folder_selected = filedialog.askdirectory()  # 打开文件夹选择对话框
    if folder_selected:
        UI_input[call_name].delete(0, tk.END)  # 清空已有内容
        UI_input[call_name].insert(0, folder_selected)  # 插入选定路径


def submit_input(event=None):
    user_input = UI_input[call_name].get()  # 获取用户输入内容
    if call_name == 'grawler_image':
        messagebox.showwarning('警告！！！！！', '骗你的，grawler_image没有加入搜索引擎功能，developer懒得加进来了，'
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
    if messagebox.askokcancel("退出确认", "你确定要关闭整个系统吗？"):
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


def call_find_empty_files():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(find_empty_files, text="请输入文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n"
                                               "此功能将为您查找此磁盘内所有的空文件及其来源", font=("Arial", 14))
    show_label.pack(pady=10)
    find_empty_files.pack()
    global call_name
    call_name = 'find_empty_files'


def call_find_empty_folders():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(find_empty_folders, text="请输入文件夹路径\n路径格式为’C:/Pictures/work/txt/‘\n"
                                               "此功能将为您查找此磁盘内所有的空文件夹及其来源", font=("Arial", 14))
    show_label.pack(pady=10)
    find_empty_folders.pack()
    global call_name
    call_name = 'find_empty_folders'


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


def call_identify_hand():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(identify_hand, text="该模块为神经网络识别人手模块\n输入框无要求，可随意输入字符\n输入字符无任何含义\n"
                                              "仅作为启动该功能的触发器\n启动功能时请打开电脑摄像头且将手部伸出置于摄像头前\n"
                                              "启动功能后单击键盘esc,再用鼠标单机图像窗口的X即可退出此功能", font=("Arial", 14))
    show_label.pack(pady=10)
    identify_hand.pack()
    global call_name
    call_name = 'identify_hand'


def call_identify_face():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(identify_face, text="该模块为神经网络识别人脸模块\n输入框无要求，可随意输入字符\n输入字符无任何含义\n"
                                              "仅作为启动该功能的触发器\n启动功能时请打开电脑摄像头且将脸部伸出置于摄像头前\n"
                                              "启动功能后单击键盘esc,再用鼠标单机图像窗口的X即可退出此功能", font=("Arial", 14))
    show_label.pack(pady=10)
    identify_face.pack()
    global call_name
    call_name = 'identify_face'


def call_decompress_package():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(decompress_package, text="请输入需要解压缩的包路径\n可输入文件夹路径批量解压多个文件\n如:C:/work/roi/\n"
                          "也可输入单个路径解压单个文件\n如:C:/work/roi/3.zip\n此功能将会对目标文件进行解压缩", font=("Arial", 20))
    show_label.pack(pady=10)
    decompress_package.pack()
    global call_name
    call_name = 'decompress_package'


def call_check_update():
    main_entry[moudle_name].pack_forget()
    global show_label
    if show_label:
        show_label.destroy()
    show_label = tk.Label(check_update, text="请输入'y,125.0.0.1:1230'的格式\n即’(是否开启代理),(你的代理IP)‘\n若未开启代理则填入‘n,n’\n"
                                             "中间要用逗号(英文字符)隔开\n(是否开启代理)可填y或Y或n或N\n(你的代理IP)需要参照格式示例填写\n"
                                             "此功能将会检查版本更新\n获取版本信息，并且介绍版本更新内容", font=("Arial", 20))
    show_label.pack(pady=10)
    check_update.pack()
    global call_name
    call_name = 'check_update'


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


def checkupdate(state):
    version_URL = 'https://raw.githubusercontent.com/zyradar/ZYScript/TestScritpt/version.txt'
    Tip_URL = 'https://raw.githubusercontent.com/zyradar/ZYScript/TestScritpt/Update%20Tip.txt'
    flag, proxy = state.split(',')
    flag, proxy = flag.strip(' '), proxy.strip(' ')
    proxies = None
    with open('./_internal/version.txt', 'a+', encoding="utf-8") as f:
        f.seek(0)
        local_version = f.readlines()
    local_version = local_version[0]
    while flag:
        try:
            if flag == 'y' or flag == 'Y':
                proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy}
                version_response = requests.get(version_URL, proxies=proxies)
                tip_response = requests.get(Tip_URL, proxies=proxies)
                flag = None
            elif flag == 'n' or flag == 'N':
                version_response = requests.get(version_URL)
                tip_response = requests.get(Tip_URL)
                flag = None
            else:
                messagebox.showwarning("警告!!!", '用户输入信息不符合规则!!!\n请按照提示输入信息!!!')
                break
            if version_response.status_code == 200 and tip_response.status_code == 200:
                version = version_response.text
                tip = tip_response.text
            messagebox.showwarning("版本内容", f'当前版本为:{local_version}\n最新版本为:{version}\n{tip}')
        except:
            # if printupdate:
            #     messagebox.showwarning("注意!!", '无法获取版本信息!!\n可能的原因为:\n1.用户网络环境较差，请检查网络。\n'
            #                                    '2.用户本地计算机已启用代理,但未输入y或Y，或是用户本地未启用代理却输入y或Y\n'
            #                                    '3.用户已启用代理且输入y或Y,y后的代理IP输入错误，请确认代理IP')
            # else:
            #     messagebox.showwarning("温馨提示", '本系统版本已经更新，暂无法访问更新信息，请自行前往检查更新模块中查询更新信息！')
            break


root = tk.Tk()                                                          # 创建主窗口
root.title("DATA TOOL")
root.geometry("800x900")                                                # 窗口大小
main_menu = tk.Frame(root)                                              # 主菜单界面
tk.Label(main_menu, text="MENU", font=("Arial", 18)).grid(row=0, column=1, columnspan=1, pady=10, padx=0)
main_btn = ["贴图裁剪", "数据增强", "转换格式", "制作数据集", "检查数据集", '无权限', '无权限', '系统工具', '爬虫', '神经网络',
            'deepseek', '无权限', '无权限', '无权限', '解压压缩', '检查更新', "退出"]
main_function = [open_CopyPaste, open_ExpandData, open_ConvertFormat, open_MakeDataset, open_CheckData, None, None, open_SystemTools,
                 open_Crawler, open_NeuralNetwork, open_deepseek, None, None, None,
                 open_Decompress, open_CheckUpdate, quit_app]
CopyPaste, ExpandData, ConvertFormat, MakeDataset, CheckData, SystemTools, Crawler, NeuralNetwork, Deepseek, Decompress, CheckUpdate =\
    tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
module_call = [CopyPaste, ExpandData, ConvertFormat, MakeDataset, CheckData, SystemTools, Crawler, NeuralNetwork, Deepseek, Decompress, CheckUpdate]
main_entry = {}
show_label = None
# 主菜单按钮
column, row = 0, 0
li = [0, 1, 2, 3, 4, 7, 8, 9, 10, 14, 15, 16]
for i in range(len(main_function)):
    if i % 3 == 0:
        column = 0
        row += 1
    else:
        column += 1
    # 父容器，按钮文本，按钮点击时调用的函数，按钮宽度，按钮背景颜色
    tk.Button(main_menu, text=main_btn[i], command=main_function[i], width=16, bg="lightblue",
                         font=("Arial", 16)).grid(row=row, column=column, columnspan=1, pady=10, padx=0)
    if i < len(module_call):
        main_entry[main_btn[li[i]]] = module_call[i]
        if i == 8:
            tk.Label(module_call[i], text="无权限", font=("Arial", 20)).pack(pady=60)
        else:
            tk.Label(module_call[i], text="Please select the function you want to use", font=("Arial", 20)).pack(pady=60)


CopyPaste_call = ['ROI_buff', 'ROI_armor', 'ROI_rock', "ROI_to_ground",  "返回上一级菜单"]
CopyPaste_function = [call_ROI_buff, call_ROI_armor, call_ROI_rock, call_ROI_to_ground, return_to_main_menu]
ROI_buff, ROI_armor, ROI_rock, ROI_to_ground, to_CopyPaste =\
    tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
CopyPaste_submeum = [ROI_buff, ROI_armor, ROI_rock, ROI_to_ground, to_CopyPaste]


ExpandData_call = ['change_bright', 'brightData', 'AntiColor', "返回上一级菜单"]
ExpandData_function = [call_change_bright, call_brightData, call_AntiColor, return_to_main_menu]
change_bright, brightData, AntiColor, to_ExpandData = tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
ExpandData_submeum = [change_bright, brightData, AntiColor, to_ExpandData]


ConvertFormat_call = ['json_to_buff', 'json_to_txt', 'label_add_xywh', 'label_cut_xywh', "返回上一级菜单"]
ConvertFormat_function = [call_json_to_buff, call_json_to_txt, call_label_add_xywh, call_label_cut_xywh, return_to_main_menu]
json_to_buff, json_to_txt, label_add_xywh, label_cut_xywh, to_ConvertFormat =\
    tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
ConvertFormat_submeum = [json_to_buff, json_to_txt, label_add_xywh, label_cut_xywh, to_ConvertFormat]


MakeDataset_call = ["video_to_daset", "image_to_video", "montage_video", "connect_video",
                    "modify_classes", "rename_file", "返回上一级菜单"]
MakeDataset_function = [call_video_to_daset, call_image_to_video, call_montage_video, call_connect_video,
                        call_modify_classes, call_rename_file, return_to_main_menu]
video_to_daset, image_to_video, montage_video, connect_video, modify_classes, rename_file, to_MakeDataset =\
    tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
MakeDataset_submeum = [video_to_daset, image_to_video, montage_video, connect_video, modify_classes, rename_file, to_MakeDataset]


CheckData_call = ["check_txt", "check_imgsize", "check_buffdata", "check_armordata", "check_rockdata", "返回上一级菜单"]
CheckData_function = [call_check_txt, call_check_imgsize, call_check_buffdata,
                      call_check_armordata, call_check_rockdata, return_to_main_menu]
check_txt, check_imgsize, check_armordata, check_rockdata, check_buffdata, to_CheckData =\
    tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)
CheckData_submeum = [check_txt, check_imgsize, check_buffdata, check_armordata, check_rockdata, to_CheckData]


SystemTools_call = ["find_empty_files", "find_empty_folders", "无权限", "无权限", "无权限", "无权限", "返回上一级菜单"]
SystemTools_function = [call_find_empty_files, call_find_empty_folders, None, None, None, None, return_to_main_menu]
find_empty_files, find_empty_folders, to_SystemTools = tk.Frame(root), tk.Frame(root), tk.Frame(root)
SystemTools_submeum = [find_empty_files, find_empty_folders, None, None, None, None, to_SystemTools]


Crawler_call = ["grawler_text", "grawler_image", "返回上一级菜单"]
Crawler_function = [call_grawler_text, call_grawler_image, return_to_main_menu]
grawler_text, grawler_image, to_Crawler = tk.Frame(root), tk.Frame(root), tk.Frame(root)
Crawler_submeum = [grawler_text, grawler_image, to_Crawler]


NeuralNetwork_call = ["identify_hand", 'identify_face', '无权限', '无权限', '无权限', '无权限', "返回上一级菜单"]
NeuralNetwork_function = [call_identify_hand, call_identify_face, None, None, None, None, return_to_main_menu]
identify_hand, identify_face, to_NeuralNetwork = tk.Frame(root), tk.Frame(root), tk.Frame(root)
NeuralNetwork_submeum = [identify_hand, identify_face, None, None, None, None, to_NeuralNetwork]


Deepseek_call = ["返回上一级菜单"]
Deepseek_function = [return_to_main_menu]
to_Deepseek = tk.Frame(root)
Deepseek_submeum = [to_Deepseek]


Decompress_call = ['decompress_package', '无权限', '无权限', '无权限', '无权限', '无权限', "返回上一级菜单"]
Decompress_function = [call_decompress_package, None, None, None, None, None, return_to_main_menu]
decompress_package, to_Decompress = tk.Frame(root), tk.Frame(root)
Decompress_submeum = [decompress_package, None, None, None, None, None, to_Decompress]


CheckUpdate_call = ['check_update', "返回上一级菜单"]
CheckUpdate_function = [call_check_update, return_to_main_menu]
check_update, to_CheckUpdate = tk.Frame(root), tk.Frame(root)
CheckUpdate_submeum = [check_update, to_CheckUpdate]


UI_input = {}
Module_entry = {}
run_function = {}
All_call = [CopyPaste_call, ExpandData_call, ConvertFormat_call, MakeDataset_call, CheckData_call, SystemTools_call, Crawler_call,
            NeuralNetwork_call, Deepseek_call, Decompress_call, CheckUpdate_call]
All_function = [CopyPaste_function, ExpandData_function, ConvertFormat_function, MakeDataset_function, CheckData_function,
                SystemTools_function, Crawler_function, NeuralNetwork_function, Deepseek_function, Decompress_function,
                CheckUpdate_function]
ALL_submeum = [CopyPaste_submeum, ExpandData_submeum, ConvertFormat_submeum, MakeDataset_submeum, CheckData_submeum,
               SystemTools_submeum, Crawler_submeum, NeuralNetwork_submeum, Deepseek_submeum, Decompress_submeum,
               CheckUpdate_submeum]
All_run = [[COPYPaste().ROI_buff, COPYPaste().ROI_armor, COPYPaste().ROI_rock, COPYPaste().ROI_to_ground],
           [EXpandData().change_bright, EXpandData().brightData, EXpandData().AntiColor],
           [Format().json_to_buff, Format().json_to_txt, Format().label_add_xywh, Format().label_cut_xywh],
           [DataSet().video_to_daset, DataSet().image_to_video, DataSet().montage_video, DataSet().connect_video, DataSet().modify_classes, DataSet().rename_file],
           [CheckDaset().check_txt, CheckDaset().check_imgsize, CheckDaset().check_buffdata, CheckDaset().check_armordata, CheckDaset().check_rockdata],
           [Systemtool().find_empty_files, Systemtool().find_empty_folders, None, None, None, None],
           [CRawler().grawler_text, CRawler().grawler_image],
           [Network().identify_hand, Network().identify_face, None, None, None, None],
           [1, None, None, None, None, None],
           [DEcompress().decompress_package],
           [checkupdate]]

# MakeDataset菜单按钮
for i in range(len(module_call)):
    for k in range(len(All_call[i])):
        btn_submit_MakeDataset = tk.Button(module_call[i], text=All_call[i][k], command=All_function[i][k], width=20,
                                           font=("Arial", 20), bg="lightblue")
        btn_submit_MakeDataset.pack(pady=10)

# 功能子菜单
for i in range(len(All_call)):
    for k in range(len(All_call[i])):
        if (i == 7 or i == 5) and k not in (0, 1, 6):
            continue
        if i == 9 and (k not in (0, 6)):
            continue
        if k < len(All_call[i]) - 1:
            run_function[All_call[i][k]] = All_run[i][k]
        Module_entry[All_call[i][k]] = ALL_submeum[i][k]
        UI_input[All_call[i][k]] = tk.Entry(ALL_submeum[i][k], width=30, font=("Arial", 20))
        UI_input[All_call[i][k]].pack(pady=10)
        UI_input[All_call[i][k]].bind("<Return>", submit_input)
        if i not in (6, 7, 10):
            tk.Button(ALL_submeum[i][k], text="浏览", font=("Arial", 18), command=select_path, width=10, bg="lightblue").pack(pady=10, padx=5)
        btn_submit = tk.Button(ALL_submeum[i][k], text="提交", command=submit_input, width=20, font=("Arial", 20), bg="lightblue")
        btn_submit.pack(pady=10)
        btn_back = tk.Button(ALL_submeum[i][k], text="返回上一级菜单", command=return_to_Module, width=20, font=("Arial", 20), bg="lightgray")
        btn_back.pack(pady=10)
        tk.Button(ALL_submeum[i][k], text="返回主菜单", command=jump_to_main_menu, width=20, font=("Arial", 20),bg="lightgray").pack(pady=10)

main_menu.pack()           # 默认显示主菜单
tk.Label(main_menu, text="对于新用户请务必点击检查更新\n仔细阅读更新相关提示\nrun.log文件中将记录系统的运行日志,\n可在日志文件中查看系统运行状况\n"
                         "日志内容过多时用户可随意删除日志信息,\n但不可删除日志文件", font=("Arial", 16), bg="lightblue").grid(row=int(len(main_btn)/3)+2, column=1, columnspan=1, pady=20, padx=0)
tk.Label(main_menu, text="未经开发者允许,\n严禁转载此工具,\n违者后果自负!\n如有疑问或发现bug,\n以及提出改进意见,\n请致信1795438624@qq.com反馈。\n"
         "开发者将十分感激获得您的宝贵反馈。\n", font=("Arial", 16)).grid(row=int(len(main_btn)/3)+4, column=1, columnspan=1, pady=10, padx=0)
# messagebox.showwarning("温馨提示", "输入本地路径时，可进入到文件夹中，选定目标图片或视频等文件，使用Crtl+C复制文件，"
#                                "再使用Ctrl+V粘贴到路径输入框中，将自动获取该文件路径，删去文件名以及扩展名即可获得此文件夹路径")
# messagebox.showwarning("注意！！", "为避免用户疲于输入参数和弹出窗口，后续所有需要输入的参数都可直接关闭弹出的输入窗口，只需输入路径，系统会自动使用确保程序正常运行的默认参数。")
# printupdate = False
# checkupdate('n,n')
# printupdate = True
root.protocol("WM_DELETE_WINDOW", quit_app)
root.mainloop()            # 运行主循环

