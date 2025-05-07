from .job import Job

class Company:
    def __init__(self, name, jobId):
        self.name = name
        self.jobId = jobId
        self.jobs = []

    def addJob(self, job):
        self.jobs.append(job)

    def listJobs(self):
        return self.jobs
    
    def to_dict(self):
        return{
            "name" : self.name,
            "jobId" : self.jobId,
            "jobs" : [job.to_dict() for job in self.jobs]
        }
    
    @staticmethod
    def from_dict(data):
        company = Company(data["name"], data.get("jobId"))
        for job_data in data.get("jobs", []):
            company.addJob(Job.from_dict(job_data))
        return company
    
    def __str__(self):
        return f"{self.name} ({len(self.jobs)} jobs)"