import tkinter as tk
from views.register_company_popup import RegisterCompanyPopup
from views.register_job_popup import RegisterJobPopup
from views.register_candidate_popup import RegisterCandidatePopup
from utils.persistence import loadCompanies, saveAll, updateAll
from models.company import Company
from views.delete_job_popup import DeleteJobPopup
from utils.analytics import renderFillProgressChart
from views.delete_company_popup import DeleteCompanyPopup
from views.delete_candidate_popup import DeleteCandidatePopup
from views.edit_company_popup import EditCompanyPopup
from views.edit_job_popup import EditJobPopup



class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Dashboard")
        self.geometry("1920x1080")
        self.companies = loadCompanies()

        # Nav bar (vazia por enquanto)
        self.navbar = tk.Frame(self, bg="gray")
        self.navbar.pack(fill="x", side="top")

        # Container principal
        list_frame = tk.Frame(self)
        list_frame.pack(fill="both", expand=True, pady=20)

        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack(fill="both", expand=False, pady=10)

        # Company List
        company_frame = tk.Frame(list_frame)
        company_frame.pack(side="left", fill="both", expand=True)
        tk.Label(company_frame, text="Registered Companies").pack()
        self.companyListbox = tk.Listbox(company_frame, width=40)
        self.companyListbox.pack(pady=10)
        company_buttons = tk.Frame(company_frame)
        company_buttons.pack()
        tk.Button(company_buttons, text="Register", command=self.show_register_company).pack(side="left", padx=5)
        tk.Button(company_buttons, text="Edit", command=self.edit_company).pack(side="left", padx=5)
        tk.Button(company_buttons, text="Delete", command=self.delete_company).pack(side="left", padx=5)

        # Job List
        job_frame = tk.Frame(list_frame)
        job_frame.pack(side="left", fill="both", expand=True)
        tk.Label(job_frame, text="Registered Jobs").pack()
        self.jobListbox = tk.Listbox(job_frame, width=70)
        self.jobListbox.pack(pady=10)
        job_buttons = tk.Frame(job_frame)
        job_buttons.pack()
        tk.Button(job_buttons, text="Register", command=self.show_register_job).pack(side="left", padx=5)
        tk.Button(job_buttons, text="Edit", command=self.edit_job).pack(side="left", padx=5)
        tk.Button(job_buttons, text="Delete", command=self.show_delete_job).pack(side="left", padx=5)

        # Candidate List
        candidate_frame = tk.Frame(list_frame)
        candidate_frame.pack(side="left", fill="both", expand=True)
        tk.Label(candidate_frame, text="Registered Candidates").pack()
        self.candidateListbox = tk.Listbox(candidate_frame, width=100)
        self.candidateListbox.pack(pady=10)
        candidate_buttons = tk.Frame(candidate_frame)
        candidate_buttons.pack()
        tk.Button(candidate_buttons, text="Register", command=self.show_register_candidate).pack(side="left", padx=5)
        tk.Button(candidate_buttons, text="Edit", command=self.edit_candidate).pack(side="left", padx=5)
        tk.Button(candidate_buttons, text="Delete", command=self.delete_candidate).pack(side="left", padx=5)

        # Inicializar
        self.save_and_update()

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

    # Placeholders para editar e deletar (próximos passos)
    def edit_company(self):
        EditCompanyPopup(self, self.companies, self.save_and_update)

    def delete_company(self):
        popup = tk.Toplevel(self)
        popup.title("Delete Company")
        DeleteCompanyPopup(popup, self.companies, self.save_and_update).pack(fill="both", expand=True)

    def edit_job(self):
        EditJobPopup(self, self.jobs, self.save_and_update)

    def show_delete_job(self):
        self.companies = loadCompanies()
        DeleteJobPopup(self, self.companies, self.save_and_update)

    def edit_candidate(self):
        print("Edit candidate clicked")

    def delete_candidate(self):
        DeleteCandidatePopup(self, self.companies, self.save_and_update)


