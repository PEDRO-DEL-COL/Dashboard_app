import tkinter as tk
from tkinter import messagebox


class DeleteCandidatePopup(tk.Toplevel):
    def __init__(self, master, companies, on_delete_callback):
        super().__init__(master)
        self.title("Delete Candidate")
        self.geometry("800x600")
        self.companies = companies
        self.on_delete_callback = on_delete_callback
        self.selected_company_index = None
        self.selected_job_index = None

        # Lista de empresas
        tk.Label(self, text="Select a company").pack(pady=5)
        self.company_listbox = tk.Listbox(self, width=50)
        self.company_listbox.pack()
        self.company_listbox.bind("<<ListboxSelect>>", self.show_jobs)

        # Lista de vagas
        tk.Label(self, text="Select a job").pack(pady=5)
        self.job_listbox = tk.Listbox(self, width=50)
        self.job_listbox.pack()
        self.job_listbox.bind("<<ListboxSelect>>", self.show_candidates)

        # Lista de candidatos
        tk.Label(self, text="Select a candidate to delete").pack(pady=5)
        self.candidate_listbox = tk.Listbox(self, width=50)
        self.candidate_listbox.pack()

        tk.Button(self, text="Delete Candidate", command=self.delete_candidate).pack(pady=10)

        self.update_company_list()

    def update_company_list(self):
        self.company_listbox.delete(0, tk.END)
        for company in self.companies:
            self.company_listbox.insert(tk.END, f"{company.name} ({company.companyId})")

    def show_jobs(self, event=None):
        selection = self.company_listbox.curselection()
        if not selection:
            return

        self.selected_company_index = selection[0]
        self.job_listbox.delete(0, tk.END)
        self.candidate_listbox.delete(0, tk.END)

        company = self.companies[self.selected_company_index]
        for job in company.jobs:
            self.job_listbox.insert(tk.END, f"{job.title} - {job.status}")

    def show_candidates(self, event=None):
        job_selection = self.job_listbox.curselection()
        if not job_selection:
            return

        self.selected_job_index = job_selection[0]
        self.candidate_listbox.delete(0, tk.END)

        company = self.companies[self.selected_company_index]
        job = company.jobs[self.selected_job_index]
        for candidate in job.candidates:
            self.candidate_listbox.insert(tk.END, str(candidate))

    def delete_candidate(self):
        if self.selected_company_index is None or self.selected_job_index is None:
            messagebox.showwarning("Warning", "Select a company and a job.")
            return

        candidate_index = self.candidate_listbox.curselection()
        if not candidate_index:
            messagebox.showwarning("Warning", "Select a candidate to delete.")
            return

        company = self.companies[self.selected_company_index]
        job = company.jobs[self.selected_job_index]

        del job.candidates[candidate_index[0]]
        self.on_delete_callback()
        self.show_candidates()
        messagebox.showinfo("Success", "Candidate deleted.")
