import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Systemtool:
    def __init__(self):
        self.empty_files_by_folder = {}
        self.path = None       # 设置要扫描的根目录
        self.selected_folder = None                 # 记录当前选中的文件夹路径
        self.tree = None
        self.root = None
        self.label = None
        self.flag = None

    def find_empty_files(self, path):
        self.path = path
        self.flag = '空文件'
        self.find_empty(self.path)  # 预扫描文件
        self.Tree_UI()
        self.root.mainloop()

    def find_empty_folders(self, path):
        self.path = path
        self.flag = '空文件夹'
        self.find_empty(self.path)  # 预扫描文件
        self.Tree_UI()
        self.root.mainloop()

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
        for file in empty_files:
            self.tree.insert(self.selected_folder, "end", text=file, iid=file, open=False)  # 叶子节点

    def on_select(self, event):                                         # 处理用户选中目录的事件
        self.selected_folder = self.tree.focus()                               # 获取当前选中的目录或文件
        if self.selected_folder:
            self.label.config(text=f"当前选中: {self.selected_folder}")
        else:
            self.label.config(text="当前选中: (请选择文件夹)")

    def delete_empty_files(self):                                       # 删除当前选中目录下的所有空文件
        if not self.selected_folder:
            messagebox.showwarning("警告", "请先选择一个文件夹！")
            return
        confirm = messagebox.askyesno("确认删除", f"确定删除 {self.selected_folder} 下的所有空文件吗？")
        if confirm:
            empty_files = self.empty_files_by_folder.get(self.selected_folder, [])
            deleted_count = 0
            for file in empty_files:
                try:
                    os.remove(file)
                    deleted_count += 1
                except PermissionError:
                    continue
            self.find_empty(self.path)                                  # 重新扫描并更新界面
            self.refresh_tree()
            messagebox.showinfo("删除成功", f"已删除 {deleted_count} 个空文件！")

    def refresh_tree(self):                                             # 重新加载 Treeview
        self.tree.delete(*self.tree.get_children())                     # 清空Treeview
        root_node = self.tree.insert("", "end", iid=self.path, text=self.path, open=False)
        self.tree.insert(root_node, "end", text="加载中...", iid=f"{self.path}_loading")

    def find_empty(self, path):                                         # 遍历整个目录，按文件夹分类存储空文件
        self.empty_files_by_folder.clear()                              # 清空旧数据
        for foldername, subfolders, filenames in os.walk(path):
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
                if not subfolders and not filenames:  # 如果没有子文件夹且没有文件
                    empty_files.append(foldername)
            if empty_files:
                self.empty_files_by_folder[foldername] = empty_files

    def get_subfolders(self, folder):                                   # 获取某个文件夹下的所有子文件夹
        subfolders = []
        try:
            for entry in os.scandir(folder):                            # 遍历目录
                if entry.is_dir():
                    subfolders.append(entry.path)
        except PermissionError:
            pass
        return subfolders


# Systemtool().find_empty_files('D:\\MYproject\\ZYscript')

