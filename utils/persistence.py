import json
import tkinter as tk
from models.company import Company

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

def saveAll(companies):
    with open(PATH_JSON, "w", encoding="utf-8") as f:
        json.dump([company.to_dict() for company in companies], f, indent=4)

def updateCompanyList(companyListbox, companies):
    companyListbox.delete(0, tk.END)
    for company in companies:
        companyListbox.insert(tk.END, f"{company.name} (ID: {company.companyId})")

def updateJobList(jobListbox, companies):
    jobListbox.delete(0, tk.END)
    for company in companies:
        for job in company.jobs:
            jobListbox.insert(
                tk.END,
                f"{job.title} (Status: {job.status}, Coverage: {job.coverage}) - Company: {company.name}"
            )

def updateCandidateList(candidateListbox, companies):
    candidateListbox.delete(0, tk.END)
    for company in companies:
        for job in company.jobs:
            for candidate in job.candidates:
                candidateListbox.insert(
                    tk.END,
                    f"{candidate.name} ({candidate.status}) - Job: {job.title} - Company: {company.name}"
                )

def updateAll(companyListbox, jobListbox, candidateListbox, companies):
    updateCompanyList(companyListbox, companies)
    updateJobList(jobListbox, companies)
    updateCandidateList(candidateListbox, companies)
