import tkinter as tk
from tkinter import messagebox


class DeleteJobPopup(tk.Toplevel):
    def __init__(self, master, companies, on_delete_callback):
        super().__init__(master)
        self.title("Delete Job")
        self.geometry("400x400")
        self.companies = companies
        self.on_delete_callback = on_delete_callback
        self.selected_company_index = None

        tk.Label(self, text="Select a company").pack(pady=5)
        self.company_listbox = tk.Listbox(self, width=50)
        self.company_listbox.pack()
        self.company_listbox.bind("<<ListboxSelect>>", self.show_jobs)

        tk.Label(self, text="Select a job").pack(pady=5)
        self.job_listbox = tk.Listbox(self, width=50)
        self.job_listbox.pack()

        tk.Button(self, text="Delete Job", command=self.delete_job).pack(pady=10)

        self.update_company_list()

    def update_company_list(self):
        self.company_listbox.delete(0, tk.END)
        for company in self.companies:
            self.company_listbox.insert(tk.END, f"{company.name} (Job ID: {company.jobId})")

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

    def delete_job(self):
        if self.selected_company_index is None:
            messagebox.showwarning("Warning", "Select a company.")
            return

        job_index = self.job_listbox.curselection()
        if not job_index:
            messagebox.showwarning("Warning", "Select a job to delete.")
            return

        company = self.companies[self.selected_company_index]
        del company.jobs[job_index[0]]
        self.on_delete_callback()
        self.show_jobs()
        messagebox.showinfo("Success", "Job deleted.")

