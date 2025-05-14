import tkinter as tk
import random
from tkinter import messagebox
from utils.persistence import loadCompanies
from models.company import Company

class RegisterCompanyPopup(tk.Toplevel):
    def __init__(self, master, on_register_callback):
        super().__init__(master)
        self.title("Register Company")
        self.on_register_callback = on_register_callback

        tk.Label(self, text="Company Name").pack(pady=5)
        self.entry_name = tk.Entry(self, width=40)
        self.entry_name.pack(pady=5)

        tk.Button(self, text="Register", command=self.registerCompany).pack(pady=10)


    def registerCompany(self):
        name = self.entry_name.get()

        if name:
            companyId = self.generateUniqueId()
            company = Company(name="", companyId="")
            self.on_register_callback(name, companyId)
            self.destroy()
        else:
            messagebox.showwarning("Warning!", "Please fill all the blank spaces.")

    def updateList(self):
        self.listbox_companies.delete(0, tk.END)
        for company in self.companies:
            self.listbox_companies.insert(tk.END, f"{company.name} (Job ID: {company.jobId})")

    def generateUniqueId(self):
        existingIds = [company.companyId for company in loadCompanies()]
        while True:
            newId = f"COMP{random.randint(1000000, 9999999)}"
            if newId not in existingIds:
                return newId