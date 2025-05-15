import tkinter as tk
from tkinter import messagebox
from utils.persistence import loadCompanies, saveCompanies
from models.candidate import Candidate

class RegisterCandidatePopup(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.companies = loadCompanies()
        self.selected_company_index = None
        self.selected_job_index = None

        tk.Label(self, text="Select a Company").pack()
        self.companyListbox = tk.Listbox(self, width=50)
        self.companyListbox.pack()
        self.companyListbox.bind("<<ListboxSelect>>", self.showCompanyJobs)

        tk.Label(self, text="Jobs for Selected Company").pack()
        self.jobListbox = tk.Listbox(self, width=50)
        self.jobListbox.pack()
        self.jobListbox.bind("<<ListboxSelect>>", self.showJobCandidates)

        tk.Label(self, text="Candidates for Selected Job").pack()
        self.candidateListbox = tk.Listbox(self, width=50)
        self.candidateListbox.pack()

        tk.Button(self, text="Add Candidate", command=self.openAddCandidatePopup).pack(pady=10)

        self.updateCompanyList()

    def updateCompanyList(self):
        self.companyListbox.delete(0, tk.END)
        for company in self.companies:
            self.companyListbox.insert(tk.END, f"{company.name} (ID: {company.companyId})")

    def showCompanyJobs(self, event):
        selection = self.companyListbox.curselection()
        if selection:
            index = selection[0]
            if self.selected_company_index != index:
                self.selected_company_index = index
                self.selected_job_index = None
                self.jobListbox.delete(0, tk.END)
                self.candidateListbox.delete(0, tk.END)
                company = self.companies[index]
                for job in company.jobs:
                    self.jobListbox.insert(tk.END, f"{job.title} - {job.status}")

    def showJobCandidates(self, event):
        job_selection = self.jobListbox.curselection()
        if job_selection:
            self.selected_job_index = job_selection[0]
            company = self.companies[self.selected_company_index]
            job = company.jobs[self.selected_job_index]
            self.candidateListbox.delete(0, tk.END)
            for candidate in job.candidates:
                self.candidateListbox.insert(tk.END, str(candidate))

    def openAddCandidatePopup(self):
        if self.selected_company_index is None or self.selected_job_index is None:
            messagebox.showwarning("Warning!", "Please select a company and a job first.")
            return

        company = self.companies[self.selected_company_index]
        job = company.jobs[self.selected_job_index]

        popup = tk.Toplevel(self)
        popup.title("Add Candidate")

        tk.Label(popup, text="Name").pack()
        entry_name = tk.Entry(popup, width=40)
        entry_name.pack()

        tk.Label(popup, text="Status").pack()
        status_var = tk.StringVar(popup)
        status_var.set("Applied")
        options = ["Submitted", "Interviewing", "Offer Extended", "Hired", "Rejected"]
        dropdown_status = tk.OptionMenu(popup, status_var, *options)
        dropdown_status.pack()

        def addCandidate():
            name = entry_name.get()
            status = status_var.get()
            if name and status:
                candidate = Candidate(name, status)
                job.addCandidate(candidate)
                saveCompanies(self.companies)
                self.showJobCandidates(None)
                popup.destroy()
            else:
                messagebox.showwarning("Warning!", "Please fill in all fields.")

        tk.Button(popup, text="Add Candidate", command=addCandidate).pack(pady=10)
