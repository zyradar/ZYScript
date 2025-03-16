import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import win32com.client
from GetParameters import get_windowstate


empty_files_by_folder={'D:/MYproject/ZYscript/test': ['D:/MYproject/ZYscript/test\\test1\\b',
                                                      'D:/MYproject/ZYscript/test\\test1\\c',
                                                      'D:/MYproject/ZYscript/test\\test1\\d',
                                                      'D:/MYproject/ZYscript/test\\test1\\f'],
                       'D:/MYproject/ZYscript/test\\dst': ['D:/MYproject/ZYscript/test\\dst\\1\\5'],
                       'D:/MYproject/ZYscript/test\\test1': ['D:/MYproject/ZYscript/test\\test1\\a\\a',
                                                             'D:/MYproject/ZYscript/test\\test1\\a\\新建文件夹']}



class Systemtool:
    def __init__(self):
        self.empty_files_by_folder = {}
        self.path = None       # 设置要扫描的根目录
        self.selected_folder = None                 # 记录当前选中的文件夹路径
        self.tree = None
        self.root = None
        self.progress = None
        self.label = None
        self.flag = None
        self.desktop_path = None
        self.exe_path = None
        self.logo_path = None
        self.tip = None
        self.progress_bar = None
        self.progress_label = None
        self.get_entry_path = {'desktop_path': None, 'exe_path': None, 'logo_path': None, 'tip': None}
        self.open_window = False
        self.show_time = 1

    def find_empty_files(self, path):
        self.path = path
        self.flag = '空文件'
        self.open_window, self.show_time = get_windowstate()
        self.find_empty(self.path)  # 预扫描文件
        self.Tree_UI()
        self.root.mainloop()
        messagebox.showwarning('温馨提示', 'find_empty_files任务已完成')

    def find_empty_folders(self, path):
        self.path = path
        self.flag = '空文件夹'
        self.open_window, self.show_time = get_windowstate()
        self.find_empty(self.path)  # 预扫描文件
        self.Tree_UI()
        self.root.mainloop()
        messagebox.showwarning('温馨提示', 'find_empty_folders任务已完成')

    def create_shortcut(self, flag):
        self.set_shortcut()
        if self.logo_path and self.exe_path:
            desktop = self.desktop_path
            shortcut_path = os.path.join(desktop, "ZYScript.lnk")  # 快捷方式路径
            target_exe = self.exe_path  # 目标 EXE 文件路径
            shell = win32com.client.Dispatch("WScript.Shell")  # 创建快捷方式
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.Targetpath = target_exe  # 目标路径
            shortcut.WorkingDirectory = os.path.dirname(target_exe)  # 运行目录
            shortcut.IconLocation = self.logo_path  # 图标
            shortcut.Description = self.tip  # 快捷方式描述
            try:
                shortcut.Save()  # 保存快捷方式
                messagebox.showwarning('温馨提示', 'create_shortcut任务已完成')
            except:
                messagebox.showwarning('警告', '无法正确创建快捷方式，极大可能的原因是您现在所使用的本地计算机账号为非管理员账户，'
                                             '该系统运行确少管理员权限，请退出该系统，并以管理员方式打开此系统重试此功能。')
        else:
            messagebox.showwarning('警告', '发生错误，可执行文件路径和logo路径都不可为空')

    def Tree_UI(self,):
        self.root = tk.Tk()
        self.root.title("ZY空文件管理器")
        self.root.geometry("700x500")
        self.tree = ttk.Treeview(self.root)                             # 创建树形结构
        self.tree.heading("#0", text=f"文件夹 / {self.flag}", anchor="w")       # 设置表头
        # expand=True允许Treeview组件扩展，fill="both"水平垂直方向填充整个窗口
        self.tree.pack(side="left", expand=True, fill="both")
        # "vertical"垂直方向滚动条‘horizontal’水平滚动条， command=self.tree.yview将滚动条关联到Treeview的y轴滚动
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="left", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)   # 连接Treeview和滚动条,yscrollcommand同步Treeview的滚动行为
        self.tree.bind("<<TreeviewOpen>>", self.on_expand)              # 绑定展开事件
        self.tree.bind("<<TreeviewSelect>>", self.on_select)            # 绑定选择事件
        info_frame = tk.Frame(self.root)                                # 右侧按钮和信息区域
        info_frame.pack(side="right", fill="y", padx=10)                # fill="y"让info_frame充满 y 轴
        self.label = tk.Label(info_frame, text="当前选中: ", font=("Arial", 12), wraplength=200)
        self.label.pack(pady=10)
        delete_btn = tk.Button(info_frame, text="删除该目录下的所有空文件",
                                    font=("Arial", 12), bg="red", fg="white",
                                    command=self.delete_empty_files)
        delete_btn.pack(pady=10)
        # ""	空字符串表示该节点是根节点（没有父节点）
        # "end"	在 Treeview 末尾添加此节点
        # iid=self.path	节点的唯一 ID（这里用路径字符串 self.path 作为 ID，方便后续查找）
        # text=self.path	节点显示的文本内容（这里显示根目录路径，比如 C:/Users）
        # open=False	默认不展开（点击才展开子目录）
        root_node = self.tree.insert("", "end", iid=self.path, text=self.path, open=False)              # 添加根节点
        # root_node父节点， text="加载中..."表示正在加载子文件夹， iid=f"{self.path}_loading"唯一ID（路径_loading后缀，避免重复）
        self.tree.insert(root_node, "end", text="加载中...", iid=f"{self.path}_loading")

    def on_expand(self, event):                                 # 处理目录展开时的事件
        self.selected_folder = self.tree.focus()                       # 获取当前选中的目录
        if self.selected_folder.endswith("_loading"):
            return  # 防止展开占位符
        for child in self.tree.get_children(self.selected_folder):     # 清空之前的占位符
            self.tree.delete(child)
        subfolders = self.get_subfolders(self.selected_folder)         # 获取子文件夹
        for folder in subfolders:
            node_id = self.tree.insert(self.selected_folder, "end", iid=folder, text=folder, open=False)
            self.tree.insert(node_id, "end", text="加载中...", iid=f"{folder}_loading")  # 继续添加占位符
        empty_files = self.empty_files_by_folder.get(self.selected_folder, [])
        if self.flag == '空文件':
            for file in empty_files:
                self.tree.insert(self.selected_folder, "end", text=file, iid=file, open=False)  # 叶子节点

    def on_select(self, event):                                         # 处理用户选中目录的事件
        self.selected_folder = self.tree.focus()                               # 获取当前选中的目录或文件
        if self.selected_folder:
            self.label.config(text=f"当前选中: {self.selected_folder}")
        else:
            self.label.config(text="当前选中: (请选择文件夹)")

    def delete_empty_files(self):  # 递归删除当前选中目录及所有子目录下的空文件
        if not self.selected_folder:
            messagebox.showwarning("警告", "请先选择一个文件夹！")
            return
        confirm = messagebox.askyesno("确认删除", f"确定删除 {self.selected_folder} 及其所有子目录中的空文件吗？")
        if not confirm:
            return
        deleted_count = 0  # 记录删除数量

        def delete_in_folder(folder):
            nonlocal deleted_count
            if folder in self.empty_files_by_folder:  # 如果该目录下有空文件
                empty_files = self.empty_files_by_folder[folder]
                for file in empty_files:
                    try:
                        if self.flag == '空文件':
                            os.remove(file)
                        elif self.flag == '空文件夹':
                            os.rmdir(file)
                        deleted_count += 1
                    except PermissionError:
                        continue
            try:        # 递归遍历子目录
                for subfolder in os.listdir(folder):
                    subfolder_path = os.path.join(folder, subfolder)
                    if os.path.isdir(subfolder_path):  # 如果是子目录，则递归删除
                        delete_in_folder(subfolder_path)
            except PermissionError:
                pass  # 忽略权限不足的目录

        delete_in_folder(self.selected_folder)      # 调用递归函数
        self.find_empty(self.path)      # 重新扫描并更新界面
        self.refresh_tree()
        messagebox.showinfo("删除成功", f"已删除 {deleted_count} 个空文件！")

    def refresh_tree(self):                                             # 重新加载 Treeview
        self.tree.delete(*self.tree.get_children())                     # 清空Treeview
        root_node = self.tree.insert("", "end", iid=self.path, text=self.path, open=False)
        self.tree.insert(root_node, "end", text="加载中...", iid=f"{self.path}_loading")

    def find_empty(self, path):                                         # 遍历整个目录，按文件夹分类存储空文件
        self.empty_files_by_folder.clear()                              # 清空旧数据
        step = 0
        if self.open_window:
            self.take_gui()
            walk_list = list(os.walk(path))
            total_steps = len(walk_list)
            self.progress_bar["maximum"] = total_steps
        for foldername, subfolders, filenames in os.walk(path):
            step += 1
            if self.open_window:
                self.progress_bar["value"] = step
                self.progress_label.config(text=f"正在遍历: {foldername} ({step}/{total_steps})")
                self.progress.update_idletasks()
            empty_files = []
            if self.flag == '空文件':                                    # 该文件夹下的空文件列表
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    try:
                        if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
                            empty_files.append(file_path)                   # 记录空文件
                    except PermissionError:                                 # 忽略权限不足的文件
                        continue
            elif self.flag == '空文件夹':
                for filename in subfolders:
                    file_path = os.path.join(foldername, filename)
                    if len(os.listdir(file_path)) == 0:
                        empty_files.append(file_path)
            if empty_files:
                self.empty_files_by_folder[foldername] = empty_files
        if self.open_window:
            self.progress.destroy()

    def get_subfolders(self, folder):                                   # 获取某个文件夹下的所有子文件夹
        subfolders = []
        try:
            for entry in os.scandir(folder):                            # 遍历目录
                if entry.is_dir():
                    subfolders.append(entry.path)
        except PermissionError:
            pass
        return subfolders

    def select_path(self, entry_name):
        if entry_name == 'desktop_path':
            folder_selected = filedialog.askdirectory()  # 打开文件夹选择对话框
        else:
            folder_selected = filedialog.askopenfilename()  # 打开文件夹选择对话框
        if folder_selected:
            self.get_entry_path[entry_name].delete(0, tk.END)  # 清空已有内容
            self.get_entry_path[entry_name].insert(0, folder_selected)  # 插入选定路径

    def set_shortcut(self):
        root = tk.Tk()
        root.geometry("750x600")
        root.title("路径设置")
        setshortcut, tipwindow = tk.Frame(root), tk.Frame(root)
        setshortcut.pack()
        tipwindow.pack()
        tk.Label(setshortcut, text="因涉及本地路径，该窗口配置不可跳过！", font=("Arial", 18)).grid(row=0, column=1, pady=10, padx=0)
        tk.Label(setshortcut, text="您的桌面路径:", font=("Arial", 18)).grid(row=1, column=0, pady=10, padx=0)
        desktop_path_entry = tk.Entry(setshortcut, width=30, font=("Arial", 18))
        desktop_path_entry.grid(row=1, column=1, pady=10, padx=0)
        self.get_entry_path['desktop_path'] = desktop_path_entry
        tk.Button(setshortcut, text="浏览", command=lambda: self.select_path('desktop_path'), width=10, bg="lightblue",
                  font=("Arial", 14)).grid(row=1, column=2, pady=10, padx=0)
        tk.Label(setshortcut, text="可执行文件路径:", font=("Arial", 18)).grid(row=2, column=0, pady=10, padx=0)
        exe_path_entry = tk.Entry(setshortcut, width=30, font=("Arial", 18))
        exe_path_entry.grid(row=2, column=1, pady=10, padx=0)
        self.get_entry_path['exe_path'] = exe_path_entry
        tk.Button(setshortcut, text="浏览", command=lambda: self.select_path('exe_path'), width=10, bg="lightblue",
                  font=("Arial", 14)).grid(row=2, column=2, pady=10, padx=0)
        tk.Label(setshortcut, text="选定的logo路径:", font=("Arial", 18)).grid(row=3, column=0, pady=10, padx=0)
        logo_path_entry = tk.Entry(setshortcut, width=30, font=("Arial", 18))
        logo_path_entry.grid(row=3, column=1, pady=10, padx=0)
        self.get_entry_path['logo_path'] = logo_path_entry
        tk.Button(setshortcut, text="浏览", command=lambda: self.select_path('logo_path'), width=10, bg="lightblue",
                  font=("Arial", 14)).grid(row=3, column=2, pady=10, padx=0)
        tk.Label(setshortcut, text="快捷方式的描述:", font=("Arial", 18)).grid(row=4, column=0, pady=10, padx=0)
        tip_entry = tk.Entry(setshortcut, width=30, font=("Arial", 18))
        tip_entry.grid(row=4, column=1, pady=10, padx=0)
        self.get_entry_path['tip'] = tip_entry

        tk.Label(tipwindow, text="桌面路径可回到自己的电脑桌面，随机右键一个快捷方式，\n点击属性，打开属性界面后点击上方导航栏中常规按钮，\n"
                                 "即可获取本地计算机系统默认的桌面。\n可执行文件路径可随机右键桌面中的快捷方式,\n找到‘打开文件所在的位置’,\n"
                                 "即可从打开的文件夹中找到该快捷方式绑定的可执行文件\nlogo路径即选取一个你想为此软件设置的快捷方式图标文件。",
                 font=("Arial", 18)).pack()

        def on_submit():                                    # 创建提交按钮
            self.desktop_path = desktop_path_entry.get() if desktop_path_entry.get() else 'C:/Users/Public/Desktop'
            self.exe_path = exe_path_entry.get() if exe_path_entry.get() else None
            self.logo_path = logo_path_entry.get() if logo_path_entry.get() else None
            self.tip = tip_entry.get() if tip_entry.get() else '无描述'
            root.destroy()                          # 关闭输入窗口
        tk.Button(setshortcut, text="提交", command=on_submit, width=20, bg="lightblue", font=("Arial", 18))\
            .grid(row=5, column=1, columnspan=1, pady=10)
        root.wait_window()                          # 等待直到输入窗口关闭

    def take_gui(self):
        self.progress = tk.Tk()
        self.progress.title("文件加载进度")
        self.progress.geometry("400x150")
        self.progress_bar = ttk.Progressbar(self.progress, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=20)
        self.progress_label = tk.Label(self.progress, text="等待开始...")
        self.progress_label.pack()


# Systemtool().find_empty_files('D:/MYproject/ZYscript/test')
# Systemtool().create_shortcut(1)
# Systemtool().tese()

