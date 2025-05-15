import tkinter as tk
from views.register_company_popup import RegisterCompanyPopup
from views.register_job_popup import RegisterJobPopup
from views.register_candidate_popup import RegisterCandidatePopup
from utils.persistence import loadCompanies, saveAll, updateAll
from models.company import Company
from views.delete_job_popup import DeleteJobPopup
from utils.analytics import renderFillProgressChart


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

        # Container para as 3 listas lado a lado
        list_frame = tk.Frame(self, bg="lightgray")
        list_frame.pack(fill="both", expand=True, pady=20)

        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack(fill="both", expand=False, pady=10)

        # Company List
        company_frame = tk.Frame(list_frame)
        company_frame.pack(side="left", fill="both", expand=True)
        tk.Label(company_frame, text="Registered Companies").pack()
        self.companyListbox = tk.Listbox(company_frame, width=40)
        self.companyListbox.pack(pady=10)

        # Job List
        job_frame = tk.Frame(list_frame)
        job_frame.pack(side="left", fill="both", expand=True)
        tk.Label(job_frame, text="Registered Jobs").pack()
        self.jobListbox = tk.Listbox(job_frame, width=70)
        self.jobListbox.pack(pady=10)

        # Candidate List
        candidate_frame = tk.Frame(list_frame)
        candidate_frame.pack(side="left", fill="both", expand=True)
        tk.Label(candidate_frame, text="Registered Candidates").pack()
        self.candidateListbox = tk.Listbox(candidate_frame, width=100)
        self.candidateListbox.pack(pady=10)

        # Call the update methods initially
        self.save_and_update()

    def show_delete_job(self):
        self.companies = loadCompanies()
        DeleteJobPopup(self, self.companies, self.save_and_update)

    def save_and_update(self):
        saveAll(self.companies)
        updateAll(self.companyListbox, self.jobListbox, self.candidateListbox, self.companies)

        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        renderFillProgressChart(self.graph_frame, self.companies)



    def add_company_to_list(self, name, companyId):
        newCompany = Company(name, companyId)
        self.companies.append(newCompany)
        saveAll(self.companies)
        self.save_and_update()

    def show_register_company(self):
        RegisterCompanyPopup(self, self.add_company_to_list)

    def show_register_job(self):
        popup = tk.Toplevel(self)
        popup.title("Register Job")
        RegisterJobPopup(popup, self).pack(fill="both", expand=True)

    def show_register_candidate(self):
        popup = tk.Toplevel(self)
        popup.title("Register Candidate")
        RegisterCandidatePopup(popup, self).pack(fill="both", expand=True)