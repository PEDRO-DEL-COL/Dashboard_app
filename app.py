import tkinter as tk
from views.register_company_popup import RegisterCompanyPopup
from views.register_job_popup import RegisterJobPopup
from views.register_candidate_popup import RegisterCandidatePopup
from utils.persistence import loadCompanies, saveAll, updateAll
from models.company import Company
from views.delete_job_popup import DeleteJobPopup
from utils.analytics import renderFillProgressChart, renderCandidateStatusChart
from views.delete_company_popup import DeleteCompanyPopup
from views.delete_candidate_popup import DeleteCandidatePopup
from views.edit_company_popup import EditCompanyPopup
from views.edit_job_popup import EditJobPopup
from views.edit_candidate_popup import EditCandidatePopup


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Dashboard")
        self.geometry("1600x800")

        # Load all companies from persistent storage
        self.companies = loadCompanies()

        # Navigation bar (currently empty)
        self.navbar = tk.Frame(self, bg="gray")
        self.navbar.pack(fill="x", side="top")

        # Main container for lists and charts
        list_frame = tk.Frame(self)
        list_frame.pack(fill="both", expand=True, pady=20)

        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack(fill="both", expand=False, pady=10)

        # Subframes para colocar os gráficos lado a lado
        self.graph_pie_frame = tk.Frame(self.graph_frame)
        self.graph_pie_frame.pack(side="left", padx=20)

        self.graph_bar_frame = tk.Frame(self.graph_frame)
        self.graph_bar_frame.pack(side="left", padx=20)

        # ====================== Company Section ======================
        company_frame = tk.Frame(list_frame)
        company_frame.pack(side="left", fill="both", expand=True)
        tk.Label(company_frame, text="Registered Companies").pack()
        self.companyListbox = tk.Listbox(company_frame, width=40)
        self.companyListbox.pack(pady=10)

        # Buttons for company operations
        company_buttons = tk.Frame(company_frame)
        company_buttons.pack()
        tk.Button(company_buttons, text="Register", command=self.show_register_company).pack(side="left", padx=5)
        tk.Button(company_buttons, text="Edit", command=self.edit_company).pack(side="left", padx=5)
        tk.Button(company_buttons, text="Delete", command=self.delete_company).pack(side="left", padx=5)

        # ====================== Job Section ======================
        job_frame = tk.Frame(list_frame)
        job_frame.pack(side="left", fill="both", expand=True)
        tk.Label(job_frame, text="Registered Jobs").pack()
        self.jobListbox = tk.Listbox(job_frame, width=100)
        self.jobListbox.pack(pady=10)

        # Buttons for job operations
        job_buttons = tk.Frame(job_frame)
        job_buttons.pack()
        tk.Button(job_buttons, text="Register", command=self.show_register_job).pack(side="left", padx=5)
        tk.Button(job_buttons, text="Edit", command=self.edit_job).pack(side="left", padx=5)
        tk.Button(job_buttons, text="Delete", command=self.show_delete_job).pack(side="left", padx=5)

        # ====================== Candidate Section ======================
        candidate_frame = tk.Frame(list_frame)
        candidate_frame.pack(side="left", fill="both", expand=True)
        tk.Label(candidate_frame, text="Registered Candidates").pack()
        self.candidateListbox = tk.Listbox(candidate_frame, width=100)
        self.candidateListbox.pack(pady=10)

        # Buttons for candidate operations
        candidate_buttons = tk.Frame(candidate_frame)
        candidate_buttons.pack()
        tk.Button(candidate_buttons, text="Register", command=self.show_register_candidate).pack(side="left", padx=5)
        tk.Button(candidate_buttons, text="Edit", command=self.edit_candidate).pack(side="left", padx=5)
        tk.Button(candidate_buttons, text="Delete", command=self.delete_candidate).pack(side="left", padx=5)

        # Initial render/update of data and charts
        self.save_and_update()

    def save_and_update(self):
        """Saves all current data and updates the UI (lists and chart)."""
        saveAll(self.companies)
        updateAll(self.companyListbox, self.jobListbox, self.candidateListbox, self.companies)

        # Clear old chart(s)
        for widget in self.graph_pie_frame.winfo_children():
            widget.destroy()
        for widget in self.graph_bar_frame.winfo_children():
            widget.destroy()

        # Render updated analytics chart
        renderFillProgressChart(self.graph_pie_frame, self.companies)
        renderCandidateStatusChart(self.graph_bar_frame, self.companies)


    def add_company_to_list(self, name, companyId):
        """Adds a new company and refreshes UI."""
        newCompany = Company(name, companyId)
        self.companies.append(newCompany)
        saveAll(self.companies)
        self.save_and_update()

    # ====================== Register Popups ======================

    def show_register_company(self):
        """Opens popup to register a new company."""
        RegisterCompanyPopup(self, self.add_company_to_list)

    def show_register_job(self):
        """Opens popup to register a new job."""
        popup = tk.Toplevel(self)
        popup.title("Register Job")
        RegisterJobPopup(popup, self).pack(fill="both", expand=True)

    def show_register_candidate(self):
        """Opens popup to register a new candidate."""
        popup = tk.Toplevel(self)
        popup.title("Register Candidate")
        RegisterCandidatePopup(popup, self).pack(fill="both", expand=True)

    # ====================== Edit & Delete Functions ======================

    def edit_company(self):
        """Opens popup to edit selected company."""
        EditCompanyPopup(self, self.companies, self.save_and_update)

    def delete_company(self):
        """Opens popup to delete selected company."""
        popup = tk.Toplevel(self)
        popup.title("Delete Company")
        DeleteCompanyPopup(popup, self.companies, self.save_and_update).pack(fill="both", expand=True)

    def edit_job(self):
        """Opens popup to edit selected job."""
        EditJobPopup(self, self.companies, self.save_and_update)

    def show_delete_job(self):
        """Reloads data and opens popup to delete a job."""
        self.companies = loadCompanies()
        DeleteJobPopup(self, self.companies, self.save_and_update)

    def edit_candidate(self):
        """Opens popup to edit selected candidate."""
        EditCandidatePopup(self, self.companies, self.save_and_update)

    def delete_candidate(self):
        """Opens popup to delete selected candidate."""
        DeleteCandidatePopup(self, self.companies, self.save_and_update)
