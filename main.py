import tkinter as tk
from tkinter import messagebox
import pandas as pd
import json
from models.company import Company
from models.job import Job

PATH_JSON = "data.json"

def saveCompanies(companiesList):
    with open(PATH_JSON, 'w', encoding='utf-8') as f:
        json.dump([company.to_dict() for company in companiesList], f, indent=4)

def loadCompanies():
    try:
        with open(PATH_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Company.from_dict(comp) for comp in data]
    except FileNotFoundError:
        return []
    
class RegisterCompanyFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.companies = loadCompanies()

        tk.Label(self, text="Company's Name").pack()
        self.entry_name = tk.Entry(self, width=40)
        self.entry_name.pack()

        tk.Label(self, text="Job ID").pack()
        self.entry_jobId = tk.Entry(self, width=40)
        self.entry_jobId.pack()

        btn_register = tk.Button(self, text="Register", command=self.registerCompany)
        btn_register.pack(pady=10)

        self.listbox_companies =tk.Listbox(self, width=50)
        self.listbox_companies.pack()

        self.updateList()

    def registerCompany(self):
        name = self.entry_name.get()
        jobId = self.entry_jobId.get()

        if name and jobId:
            new_company = Company(name, jobId)
            self.companies.append(new_company)
            saveCompanies(self.companies)
            self.updateList()
            self.entry_name.delete(0, tk.END)
            self.entry_jobId.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning!", "Please fill all the blank spaces.")

    def updateList(self):
        self.listbox_companies.delete(0, tk.END)
        for company in self.companies:
            self.listbox_companies.insert(tk.END, f"{company.name} (Job ID: {company.jobId})")

class RegisterJobFrame(tk.Frame):
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
            self.companyListbox.insert(tk.END, f"{company.name} (Job ID: {company.jobId})")

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

        def addJob():
            title = entry_title.get()
            status = status_var.get()
            if title and status:
                new_job = Job(title, status)
                company.jobs.append(new_job)
                saveCompanies(self.companies)
                self.selected_company_index = None  # força a atualização da lista
                self.showCompanyJobs(None)
                popup.destroy()
            else:
                messagebox.showwarning("Warning!", "Please fill in all fields.")

        tk.Button(popup, text="Add Job", command=addJob).pack(pady=10)

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Dashboard")
        self.geometry("1200x800")

        # Nav bar
        self.navbar = tk.Frame(self, bg="lightgray")
        self.navbar.pack(fill="x", side="top")

        # Main container
        self.container = tk.Frame(self, bg="lightgray")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Nav buttons
        tk.Button(self.navbar, text="Register Company", command=self.show_register_company).pack(side="left")
        tk.Button(self.navbar, text="Register Job", command=self.show_register_job).pack(side="left")

        # Content frames
        self.frames = {}
        for F in (RegisterCompanyFrame, RegisterJobFrame):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_register_company()

    def show_register_company(self):
        self.frames[RegisterCompanyFrame].tkraise()

    def show_register_job(self):
        self.frames[RegisterJobFrame].tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
