from .job import Job
import random

class Company:
    def __init__(self, name, companyId):
        self.name = name
        self.companyId = companyId
        self.jobs = []

    def addJob(self, job):
        self.jobs.append(job)

    def listJobs(self):
        return self.jobs
    
    def to_dict(self):
        return{
            "name" : self.name,
            "companyId" : self.companyId,
            "jobs" : [job.to_dict() for job in self.jobs]
        }
    
    @staticmethod
    def from_dict(data):
        company = Company(data["name"], data.get("companyId"))
        for job_data in data.get("jobs", []):
            company.addJob(Job.from_dict(job_data))
        return company
    
    def __str__(self):
        return f"{self.name} [{self.companyId}] ({len(self.jobs)} jobs)"
        