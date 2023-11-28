import tkinter as tk
from tkinter import ttk
import psutil

class ProcessMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Wulf-Term")

        # Add a search entry
        self.search_entry = tk.Entry(self.root, width=20)
        self.search_entry.pack(pady=10)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_processes)
        self.search_button.pack()

        # Set up the treeview
        self.tree = ttk.Treeview(self.root, columns=("pid", "name", "cpu", "memory"))
        self.tree.heading("pid", text="PID")
        self.tree.heading("name", text="Name")
        self.tree.heading("cpu", text="CPU %")
        self.tree.heading("memory", text="Memory %")

        self.tree.pack(expand=True, fill=tk.BOTH)

        # Set up the columns
        self.tree.column("pid", width=50)
        self.tree.column("name", width=150)
        self.tree.column("cpu", width=80)
        self.tree.column("memory", width=80)

        # Set up auto-refresh
        self.auto_refresh()

    def search_processes(self):
        # Clear previous search results
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_term = self.search_entry.get().lower()
        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            if search_term in process.info['name'].lower():
                self.tree.insert("", "end", values=(
                    process.info['pid'],
                    process.info['name'],
                    f"{process.info['cpu_percent']:.2f}",
                    f"{process.info['memory_percent']:.2f}"
                ))

    def auto_refresh(self):
        # Implement your auto-refresh logic here
        # For demonstration purposes, we'll simply refresh every 5 seconds
        self.search_processes()
        self.root.after(5000, self.auto_refresh)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessMonitor(root)
    root.mainloop()
