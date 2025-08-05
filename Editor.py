import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json, os

SESSION_FILE = ".session.json"

class TextEditorWithSidebar:
    def __init__(self, root):
        self.root = root
        self.root.title("StackPad")
        self.zoom_level = 12
        self.tabs = {}
        self.autosave_interval = 30000

        self.setup_ui()
        self.create_menus()
        self.restore_session()
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.root.after(self.autosave_interval, self.auto_save)

    def setup_ui(self):
        self.container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.container.pack(fill=tk.BOTH, expand=1)

        # Sidebar
        self.sidebar = ttk.Frame(self.container, width=200)
        self.sidebar.pack_propagate(False)
        self.tree = ttk.Treeview(self.sidebar)
        self.tree.pack(fill=tk.BOTH, expand=1)
        self.tree.bind("<<TreeviewOpen>>", self.expand_folder)
        self.tree.bind("<Double-1>", self.on_tree_item_double_click)

        self.container.add(self.sidebar)

        # Editor Area
        self.editor_area = ttk.Frame(self.container)
        self.notebook = ttk.Notebook(self.editor_area)
        self.notebook.pack(fill=tk.BOTH, expand=1)
        self.container.add(self.editor_area)

    def create_menus(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Tab", command=self.new_tab)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.edit_undo)
        edit_menu.add_command(label="Redo", command=self.edit_redo)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        search_menu = tk.Menu(menubar, tearoff=0)
        search_menu.add_command(label="Find & Replace", command=self.find_replace)
        menubar.add_cascade(label="Search", menu=search_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Zoom In", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        menubar.add_cascade(label="View", menu=view_menu)

        self.root.config(menu=menubar)

    def populate_tree(self, parent, path):
        self.tree.delete(*self.tree.get_children(parent))
        try:
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                node = self.tree.insert(parent, 'end', text=item, open=False)
                self.tree.set(node, 'fullpath', full_path)
                if os.path.isdir(full_path):
                    self.tree.insert(node, 'end')  # dummy to allow expansion
        except Exception as e:
            print(f"Error reading folder: {e}")

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.tree.delete(*self.tree.get_children())
            root_node = self.tree.insert('', 'end', text=folder_path, open=True)
            self.tree.set(root_node, 'fullpath', folder_path)
            self.populate_tree(root_node, folder_path)

    def expand_folder(self, event):
        item = self.tree.focus()
        path = self.tree.item(item, 'text')
        full_path = self.get_full_path(item)
        if os.path.isdir(full_path):
            self.populate_tree(item, full_path)

    def get_full_path(self, item):
        path = self.tree.item(item, 'text')
        parent = self.tree.parent(item)
        while parent:
            path = os.path.join(self.tree.item(parent, 'text'), path)
            parent = self.tree.parent(parent)
        return path

    def on_tree_item_double_click(self, event):
        item = self.tree.focus()
        path = self.get_full_path(item)
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.new_tab(content, path)

    def new_tab(self, content="", file_path=None):
        frame = tk.Frame(self.notebook)
        text = tk.Text(frame, font=("Consolas", self.zoom_level), undo=True, wrap='word')
        text.pack(fill=tk.BOTH, expand=1)

        scroll = tk.Scrollbar(text)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.config(command=text.yview)
        text.config(yscrollcommand=scroll.set)

        name = os.path.basename(file_path) if file_path else "Untitled"
        self.notebook.add(frame, text=name)
        self.notebook.select(frame)

        self.tabs[frame] = {'text': text, 'file_path': file_path}
        text.insert(tk.END, content)

    def current_tab(self):
        return self.notebook.select()

    def current_text_widget(self):
        tab_id = self.current_tab()
        return self.tabs[self.notebook.nametowidget(tab_id)]['text']

    def open_file(self):
        file = filedialog.askopenfilename()
        if file:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            self.new_tab(content, file)

    def save_file(self):
        tab_id = self.current_tab()
        tab = self.tabs[self.notebook.nametowidget(tab_id)]
        file_path = tab.get("file_path")

        if file_path:
            content = tab['text'].get(1.0, tk.END)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Saved to {file_path}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            tab_id = self.current_tab()
            tab = self.tabs[self.notebook.nametowidget(tab_id)]
            content = tab['text'].get(1.0, tk.END)
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)
            tab['file_path'] = file
            self.notebook.tab(tab_id, text=os.path.basename(file))
            messagebox.showinfo("Saved", f"Saved to {file}")

    def zoom_in(self):
        self.zoom_level += 2
        for tab in self.tabs.values():
            tab['text'].config(font=("Consolas", self.zoom_level))

    def zoom_out(self):
        if self.zoom_level > 6:
            self.zoom_level -= 2
            for tab in self.tabs.values():
                tab['text'].config(font=("Consolas", self.zoom_level))

    def edit_undo(self):
        try:
            self.current_text_widget().edit_undo()
        except tk.TclError:
            pass

    def edit_redo(self):
        try:
            self.current_text_widget().edit_redo()
        except tk.TclError:
            pass

    def find_replace(self):
        def replace_text():
            search = search_entry.get()
            replace = replace_entry.get()
            text_widget = self.current_text_widget()
            content = text_widget.get("1.0", tk.END)
            new_content = content.replace(search, replace)
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", new_content)

        window = tk.Toplevel(self.root)
        window.title("Find & Replace")

        tk.Label(window, text="Find:").grid(row=0, column=0)
        search_entry = tk.Entry(window, width=30)
        search_entry.grid(row=0, column=1)

        tk.Label(window, text="Replace:").grid(row=1, column=0)
        replace_entry = tk.Entry(window, width=30)
        replace_entry.grid(row=1, column=1)

        tk.Button(window, text="Replace All", command=replace_text).grid(row=2, column=1, pady=5)

    def auto_save(self):
        try:
            session_data = []
            for frame, tab in self.tabs.items():
                text_content = tab['text'].get("1.0", tk.END)
                session_data.append({
                    'file_path': tab['file_path'],
                    'content': text_content
                })
            with open(SESSION_FILE, 'w', encoding='utf-8') as f:
                json.dump(session_data, f)
        except Exception as e:
            print(f"Auto-save error: {e}")

        self.root.after(self.autosave_interval, self.auto_save)

    def restore_session(self):
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                for entry in session_data:
                    self.new_tab(entry['content'], entry['file_path'])
            except Exception as e:
                print(f"Session restore failed: {e}")
        else:
            self.new_tab()

    def on_exit(self):
        self.auto_save()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = TextEditorWithSidebar(root)
    root.mainloop()
