import tkinter as tk
from views.register_company_popup import RegisterCompanyPopup
from views.register_job_popup import RegisterJobPopup
from views.register_candidate_popup import RegisterCandidatePopup  # ✅ Importar popup do Candidate
from utils.persistence import saveCompanies, loadCompanies
from models.company import Company
from views.delete_job_popup import DeleteJobPopup

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Dashboard")
        self.geometry("1200x800")
        self.companies = loadCompanies()

        # Nav bar
        self.navbar = tk.Frame(self, bg="lightgray")
        self.navbar.pack(fill="x", side="top")

        # Nav buttons
        tk.Button(self.navbar, text="Register Company", command=self.show_register_company).pack(side="left", padx=5)
        tk.Button(self.navbar, text="Register Job", command=self.show_register_job).pack(side="left", padx=5)
        tk.Button(self.navbar, text="Delete Job", command=self.show_delete_job).pack(side="left", padx=5)
        tk.Button(self.navbar, text="Register Candidate", command=self.show_register_candidate).pack(side="left", padx=5)  # ✅ Novo botão

        # List of companies
        self.label = tk.Label(self, text="Registered Companies")
        self.label.pack(pady=(20, 5))

        self.companyListbox = tk.Listbox(self, width=50)
        self.companyListbox.pack(pady=10)

        self.updateCompanyList()

    def show_delete_job(self):
        self.companies = loadCompanies()
        DeleteJobPopup(self, self.companies, self.save_and_update)

    def save_and_update(self):
        saveCompanies(self.companies)
        self.updateCompanyList()

    def show_register_company(self):
        RegisterCompanyPopup(self, self.add_company_to_list)

    def add_company_to_list(self, name, companyId):
        newCompany = Company(name, companyId)
        self.companies.append(newCompany)
        saveCompanies(self.companies)
        self.updateCompanyList()

    def show_register_job(self):
        popup = tk.Toplevel(self)
        popup.title("Register Job")
        RegisterJobPopup(popup, self).pack(fill="both", expand=True)

    # ✅ Novo método
    def show_register_candidate(self):
        popup = tk.Toplevel(self)
        popup.title("Register Candidate")
        RegisterCandidatePopup(popup, self).pack(fill="both", expand=True)

    def updateCompanyList(self):
        self.companyListbox.delete(0, tk.END)
        for company in self.companies:
            self.companyListbox.insert(tk.END, f"{company.name} (ID: {company.companyId})")
