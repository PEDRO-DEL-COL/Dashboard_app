import json
import random
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