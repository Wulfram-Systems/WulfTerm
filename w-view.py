import tkinter as tk
from tkinter import ttk
import psutil

class ProcessMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Wulf-Term")

        # Configure a dark theme
        self.root.tk_setPalette(background='#333', foreground='white', activeBackground='#666', activeForeground='white')

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

        # Add a button to kill the selected process
        self.kill_button = tk.Button(self.root, text="Kill Selected Process", command=self.kill_selected_process)
        self.kill_button.pack()

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
        # For demonstration purposes, we'll simply refresh every 5 seconds
        self.search_processes()
        self.root.after(5000, self.auto_refresh)

    def kill_selected_process(self):
        # Get the selected item in the treeview
        selected_item = self.tree.selection()
        
        if selected_item:
            # Get the process ID from the selected item
            pid = self.tree.item(selected_item, "values")[0]

            # Attempt to terminate the process
            try:
                process = psutil.Process(pid)
                process.terminate()
                self.search_processes()  # Refresh the list after terminating the process
            except psutil.NoSuchProcess:
                print(f"Process with PID {pid} not found.")
            except psutil.AccessDenied:
                print(f"Access denied to terminate process with PID {pid}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessMonitor(root)
    root.mainloop()
