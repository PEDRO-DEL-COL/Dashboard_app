import tkinter as tk
from tkinter import messagebox

class EditJobPopup(tk.Toplevel):
    def __init__(self, master, companies, on_edit_callback):
        super().__init__(master)
        self.title("Edit Job")
        self.geometry("800x600")
        self.companies = companies
        self.on_edit_callback = on_edit_callback
        self.selected_company_index = None
        self.selected_job_index = None

        # Company selection
        tk.Label(self, text="Select a company").pack()
        self.company_listbox = tk.Listbox(self, width=50)
        self.company_listbox.pack()
        self.company_listbox.bind("<<ListboxSelect>>", self.show_jobs)

        # Job selection
        tk.Label(self, text="Select a job to edit").pack()
        self.job_listbox = tk.Listbox(self, width=50)
        self.job_listbox.pack()
        self.job_listbox.bind("<<ListboxSelect>>", self.show_job_details)

        # Job Title
        tk.Label(self, text="Title").pack()
        self.title_entry = tk.Entry(self, width=50)
        self.title_entry.pack()

        # Job Status (Option Menu)
        tk.Label(self, text="Status").pack()
        self.status_var = tk.StringVar()
        self.status_var.set("Open")
        self.status_menu = tk.OptionMenu(self, self.status_var, "Open", "On hold", "Closed")
        self.status_menu.pack()

        # Coverage
        tk.Label(self, text="Coverage (%)").pack()
        self.coverage_entry = tk.Entry(self, width=50)
        self.coverage_entry.pack()

        # Save Button
        tk.Button(self, text="Save Changes", command=self.save_job_changes).pack(pady=10)

        self.update_company_list()

    def update_company_list(self):
        self.company_listbox.delete(0, tk.END)
        for company in self.companies:
            self.company_listbox.insert(tk.END, f"{company.name} ({company.companyId})")

    def show_jobs(self, event=None):
        selection = self.company_listbox.curselection()
        if selection:
            self.selected_company_index = selection[0]
        else:
            return

        self.job_listbox.delete(0, tk.END)
        company = self.companies[self.selected_company_index]
        for job in company.jobs:
            self.job_listbox.insert(tk.END, f"{job.title} - {job.status}")

    def show_job_details(self, event=None):
        if self.selected_company_index is None:
            return

        selection = self.job_listbox.curselection()
        if not selection:
            return

        self.selected_job_index = selection[0]
        job = self.companies[self.selected_company_index].jobs[self.selected_job_index]

        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, job.title)

        self.status_var.set(job.status)

        self.coverage_entry.delete(0, tk.END)
        self.coverage_entry.insert(0, str(job.coverage))


    def save_job_changes(self):
        if self.selected_company_index is None or self.selected_job_index is None:
            messagebox.showwarning("Warning", "Select a job to edit.")
            return

        title = self.title_entry.get().strip()
        status = self.status_var.get()
        coverage_input = self.coverage_entry.get().strip()

        if not title:
            messagebox.showwarning("Warning", "Title cannot be empty.")
            return

        if not coverage_input.isdigit():
            messagebox.showwarning("Warning", "Coverage must be a number.")
            return

        coverage = int(coverage_input)

        job = self.companies[self.selected_company_index].jobs[self.selected_job_index]
        job.title = title
        job.status = status
        job.coverage = coverage

        self.on_edit_callback()
        self.show_jobs()
        messagebox.showinfo("Success", "Job updated.")

