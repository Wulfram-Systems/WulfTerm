import tkinter as tk
from tkinter import ttk
import psutil  # You may need to install this library: pip install psutil

class ProcessMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Monitor")

        # Dark theme
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use a theme that supports dark mode
        self.style.configure("Treeview", background="#2E2E2E", foreground="white")
        self.style.map("Treeview", background=[("selected", "#007ACC")])

        # Create a Treeview widget to display process information
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("pid", "name", "cpu_percent", "memory_percent")
        self.tree.heading("#0", text="Process ID")
        self.tree.column("#0", width=70)
        self.tree.heading("pid", text="PID", command=lambda: self.sort_column("pid"))
        self.tree.column("pid", width=70)
        self.tree.heading("name", text="Name", command=lambda: self.sort_column("name"))
        self.tree.column("name", width=150)
        self.tree.heading("cpu_percent", text="CPU %", command=lambda: self.sort_column("cpu_percent"))
        self.tree.column("cpu_percent", width=70)
        self.tree.heading("memory_percent", text="Memory %", command=lambda: self.sort_column("memory_percent"))
        self.tree.column("memory_percent", width=70)
        self.tree.pack(expand=True, fill="both")

        # Button to refresh the process list
        refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_processes)
        refresh_button.pack(pady=10)

        # Button to kill the selected process
        kill_button = tk.Button(self.root, text="Kill Selected", command=self.kill_selected_process)
        kill_button.pack(pady=10)

        # Flag to prevent selection during refresh
        self.refreshing = False

        # Initial process refresh
        self.refresh_processes()

        # Schedule automatic refresh every second
        self.root.after(1000, self.auto_refresh)

        # Bind mouse events
        self.tree.bind("<Button-1>", self.on_tree_click)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_release)
        self.tree.bind("<B1-Motion>", self.on_tree_motion)

    def auto_refresh(self):
        # Set the refreshing flag to True
        self.refreshing = True

        # Unbind mouse events during refresh
        self.tree.unbind("<Button-1>")
        self.tree.unbind("<ButtonRelease-1>")
        self.tree.unbind("<B1-Motion>")

        # Call refresh_processes and schedule the next auto-refresh
        self.refresh_processes()
        self.root.after(1000, self.auto_refresh)

        # Set the refreshing flag to False after refresh is complete
        self.refreshing = False

        # Rebind mouse events after refresh
        self.tree.bind("<Button-1>", self.on_tree_click)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_release)
        self.tree.bind("<B1-Motion>", self.on_tree_motion)

    def refresh_processes(self):
        # Clear existing items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get a list of running processes and sort by CPU usage
        processes = sorted(
            psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_percent"]),
            key=lambda x: x.info["cpu_percent"],
            reverse=True
        )

        # Insert process information into the Treeview with color coding
        for process in processes:
            cpu_percent = process.info["cpu_percent"]
            color = self.get_color(cpu_percent)
            self.tree.insert("", "end", values=(
                process.info["pid"],
                process.info["name"],
                f"{cpu_percent:.2f}%",
                process.info["memory_percent"]
            ), tags=(color,))

    def kill_selected_process(self):
        # Check if refreshing is in progress, and if so, do not allow selection
        if not self.refreshing:
            # Get the selected item in the Treeview
            selected_item = self.tree.selection()
            if selected_item:
                # Extract the process ID from the selected item and convert it to an integer
                pid = int(self.tree.item(selected_item, "values")[0])

                # Try to terminate the process
                try:
                    process = psutil.Process(pid)
                    process.terminate()
                except psutil.NoSuchProcess:
                    pass  # Handle the case where the process no longer exists

    def sort_column(self, column):
        # Get the current values from the Treeview
        data = [(self.tree.set(child, column), child) for child in self.tree.get_children("")]

        # Sort the data based on the column values
        data.sort(reverse=False, key=lambda x: self.convert_to_numeric(x[0]))

        # Rearrange the items in the Treeview based on the sorted data
        for index, item in enumerate(data):
            self.tree.move(item[1], "", index)

    def convert_to_numeric(self, value):
        # Convert values to numeric, handling non-numeric values
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            return value  # Return the original value for non-numeric values

    def get_color(self, cpu_percent):
        # Define color thresholds for CPU usage
        high_threshold = 80
        normal_threshold = 50

        # Assign colors based on CPU usage
        if cpu_percent > high_threshold:
            return "red"
        elif cpu_percent > normal_threshold:
            return "yellow"
        else:
            return "green"

    def on_tree_click(self, event):
        pass

    def on_tree_release(self, event):
        pass

    def on_tree_motion(self, event):
        self.tree.yview_moveto((event.y - 20) / self.tree.winfo_height())


if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessMonitor(root)
    root.mainloop()
