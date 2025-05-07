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

def main():
    companies = loadCompanies()

    new = Company('Abrams', '1')
    new.addJob(Job('Picker', 'Active'))
    new.addJob(Job('Java Developer', 'Closed'))

    companies.append(new)

    saveCompanies(companies)

    for comp in companies:
        print(comp)
        for job in comp.jobs:
            print(' -', job)

if __name__ == "__main__":
    main()
