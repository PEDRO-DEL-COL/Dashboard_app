import tkinter as tk
from tkinter import messagebox

class EditCandidatePopup(tk.Toplevel):
    def __init__(self, master, companies, on_edit_callback):
        super().__init__(master)
        self.title("Edit candidate")
        self.geometry("800x800")
        self.companies = companies
        self.on_edit_callback = on_edit_callback
        self.selected_company_index = None
        self.selected_job_index = None
        self.selected_candidate_index = None

        #company selection
        tk.Label(self, text="Select a company").pack()
        self.company_listbox = tk.Listbox(self, width=50)
        self.company_listbox.pack(pady=10)
        self.company_listbox.bind("<<ListboxSelect>>", self.show_jobs)

        #job selection
        tk.Label(self, text="Select a job").pack()
        self.job_listbox = tk.Listbox(self, width=50)
        self.job_listbox.pack()
        self.job_listbox.bind("<<ListboxSelect>>", self.show_candidates)

        #candidate selection
        tk.Label(self, text="Select a candidate").pack()
        self.candidate_listbox = tk.Listbox(self, width=50)
        self.candidate_listbox.pack()
        self.candidate_listbox.bind("<<ListboxSelect>>", self.show_candidates_details)

        #candidate name
        tk.Label(self, text="Name").pack()
        self.name_entry = tk.Entry(self, width=50)
        self.name_entry.pack()

        #candidate status
        tk.Label(self, text="Status").pack()
        self.status_var = tk.StringVar()
        self.status_var.set("Undefined")
        self.status_menu = tk.OptionMenu(self, self.status_var, "Submitted", "Interview Scheduling","Interview Scheduled","Interview Completed", "Offer Extended", "Offer Accepted", "Started", "Rejected")
        self.status_menu.pack()

        #save button
        tk.Button(self, text="Save changes", command=self.save_candidate_changes).pack(pady=10)

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

    def show_candidates(self, event=None):
        selection = self.job_listbox.curselection()
        if selection:
            self.selected_job_index = selection[0]
        else:
            return

        self.candidate_listbox.delete(0, tk.END)
        company = self.companies[self.selected_company_index]
        job = company.jobs[self.selected_job_index]
        for candidate in job.candidates:
            self.candidate_listbox.insert(tk.END, f"{candidate.name} - {candidate.status}")

    def show_candidates_details(self, event=None):
        if self.selected_job_index is None:
            return

        selection = self.candidate_listbox.curselection()
        if not selection:
            return

        self.selected_candidate_index = selection[0]
        candidate = self.companies[self.selected_company_index].jobs[self.selected_job_index].candidates[self.selected_candidate_index]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, candidate.name)

        self.status_var.set(candidate.status)

    def save_candidate_changes(self):
        if self.selected_company_index is None or self.selected_job_index is None or self.selected_candidate_index is None:
            messagebox.showwarning("Warning", "Select a candidate to edit.")
            return

        name = self.name_entry.get().strip()
        status = self.status_var.get()

        if not name:
            messagebox.showwarning("Warning", "Name cannot be empty.")
            return

        candidate = self.companies[self.selected_company_index].jobs[self.selected_job_index].candidates[self.selected_candidate_index]
        candidate.name = name
        candidate.status = status

        self.on_edit_callback()
        self.show_candidates()
        messagebox.showinfo("Success", "Candidate updated.")