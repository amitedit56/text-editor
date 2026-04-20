import tkinter as tk
from tkinter import filedialog, messagebox, font
from tkinter.scrolledtext import ScrolledText

class ProfessionalTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Amit Text Editor")
        self.root.geometry("1000x650")

        self.file_path = None

        # Font
        self.text_font = font.Font(family="Times New Roman", size=12)

        # Text Area
        self.text_area = ScrolledText(root, undo=True, font=self.text_font, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Menu Bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: root.focus_get().event_generate('<<Cut>>'))
        edit_menu.add_command(label="Copy", command=lambda: root.focus_get().event_generate('<<Copy>>'))
        edit_menu.add_command(label="Paste", command=lambda: root.focus_get().event_generate('<<Paste>>'))
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # View Menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Zoom In", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

        # Status Bar
        self.status = tk.Label(root, text="Ready", anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind
        self.text_area.bind("<KeyRelease>", self.update_status)

    # Functions
    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.status.config(text="New File")

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            with open(path, 'r', encoding='utf-8') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.file_path = path
            self.status.config(text=f"Opened: {path}")

    def save_file(self):
        if self.file_path:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.status.config(text="File Saved")
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            self.file_path = path
            self.save_file()

    def zoom_in(self):
        size = self.text_font['size']
        self.text_font.configure(size=size+1)

    def zoom_out(self):
        size = self.text_font['size']
        if size > 6:
            self.text_font.configure(size=size-1)

    def update_status(self, event=None):
        text = self.text_area.get(1.0, tk.END)
        words = len(text.split())
        chars = len(text)
        self.status.config(text=f"Words: {words} | Characters: {chars}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalTextEditor(root)
    root.mainloop()