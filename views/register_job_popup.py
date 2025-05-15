import tkinter as tk
from tkinter import messagebox
from utils.persistence import loadCompanies, saveAll, updateAll
from models.job import Job

class RegisterJobPopup(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.companies = loadCompanies()
        self.selected_company_index = None  # Adicionado aqui

        tk.Label(self, text="Select a Company").pack()
        self.companyListbox = tk.Listbox(self, width=50)
        self.companyListbox.pack()
        self.companyListbox.bind("<<ListboxSelect>>", self.showCompanyJobs)

        tk.Label(self, text="Jobs for Selected Company").pack()
        self.jobListbox = tk.Listbox(self, width=50)
        self.jobListbox.pack()

        btn_addJob = tk.Button(self, text="Add Job", command=self.openAddJobPopup)
        btn_addJob.pack(pady=10)

        self.updateCompanyList()

    def updateCompanyList(self):
        self.companyListbox.delete(0, tk.END)
        for company in self.companies:
            self.companyListbox.insert(tk.END, f"{company.name} (Job ID: {company.companyId})")

    def showCompanyJobs(self, event):
        selection = self.companyListbox.curselection()
        if selection:
            index = selection[0]
            if self.selected_company_index != index:  # Verifica se mudou
                self.selected_company_index = index
                self.jobListbox.delete(0, tk.END)
                company = self.companies[index]
                for job in company.jobs:
                    self.jobListbox.insert(tk.END, f"{job.title} - {job.status}")

    def openAddJobPopup(self):
        selection = self.companyListbox.curselection()
        if not selection:
            messagebox.showwarning("Warning!", "Please select a company first.")
            return

        index = selection[0]
        company = self.companies[index]

        popup = tk.Toplevel(self)
        popup.title("Add Job")

        tk.Label(popup, text="Title").pack()
        entry_title = tk.Entry(popup, width=40)
        entry_title.pack()

        tk.Label(popup, text="Status").pack()
        status_var = tk.StringVar(popup)
        status_var.set("Open")  # valor padrão
        options = ["Open", "On hold", "Closed"]
        dropdown_status = tk.OptionMenu(popup, status_var, *options)
        dropdown_status.pack()

        # Campo para coverage (somente números)
        tk.Label(popup, text="Coverage (only numbers)").pack()

        def validate_number(value):
            return value.isdigit() or value == ""

        vcmd = (popup.register(validate_number), "%P")
        entry_coverage = tk.Entry(popup, width=40, validate="key", validatecommand=vcmd)
        entry_coverage.pack()

        def addJob():
            title = entry_title.get()
            status = status_var.get()
            coverage = entry_coverage.get()

            if title and status and coverage:
                new_job = Job(title, status, int(coverage))
                company.jobs.append(new_job)
                saveAll(self.companies)
                self.selected_company_index = None  # força a atualização da lista
                self.showCompanyJobs(None)
                popup.destroy()
            else:
                messagebox.showwarning("Warning!", "Please fill in all fields.")

        tk.Button(popup, text="Add Job", command=addJob).pack(pady=10)
