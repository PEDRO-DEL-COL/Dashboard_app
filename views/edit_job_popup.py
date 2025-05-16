import tkinter as tk
from tkinter import messagebox

class EditJobPopup(tk.Toplevel):
    def __init__(self, master, jobs, on_edit_callback):
        super().__init__(master)
        self.title("Edit Job")
        self.geometry("400x350")
        self.jobs = jobs
        self.on_edit_callback = on_edit_callback
        self.selected_index = None

        tk.Label(self, text="Select a job").pack(pady=5)
        self.listbox = tk.Listbox(self, width=50)
        self.listbox.pack(pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        tk.Label(self, text="New title").pack(pady=5)
        self.entry_title = tk.Entry(self, width=40)
        self.entry_title.pack(pady=5)

        tk.Label(self, text="New coverage").pack(pady=5)
        self.entry_coverage = tk.Entry(self, width=40)
        self.entry_coverage.pack(pady=5)

        tk.Button(self, text="Save Changes", command=self.edit_job).pack(pady=10)

        self.update_job_list()

    def update_job_list(self):
        self.listbox.delete(0, tk.END)
        for job in self.jobs:
            self.listbox.insert(tk.END, f"{job.title}")

    def on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            self.selected_index = selection[0]
            selected_job = self.jobs[self.selected_index]
            self.entry_title.delete(0, tk.END)
            self.entry_title.insert(0, selected_job.title)
            self.entry_coverage.delete(0, tk.END)
            self.entry_coverage.insert(0, selected_job.coverage)

    def edit_job(self):
        if self.selected_index is None:
            messagebox.showwarning("Warning", "Please select a job.")
            return

        new_title = self.entry_title.get().strip()
        new_coverage = self.entry_coverage.get().strip()

        if not new_title:
            messagebox.showwarning("Warning", "Job title cannot be empty.")
            return
        if not new_coverage:
            messagebox.showwarning("Warning", "Coverage cannot be empty.")
            return

        self.jobs[self.selected_index].title = new_title
        self.jobs[self.selected_index].coverage = new_coverage
        self.on_edit_callback()
        messagebox.showinfo("Success", "Job updated successfully.")
        self.destroy()
