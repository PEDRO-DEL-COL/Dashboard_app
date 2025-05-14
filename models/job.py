from models.candidate import Candidate

class Job:
    def __init__(self, title, status):
        self.title = title
        self.status = status
        self.candidates = []

    def addCandidate(self, candidate):
        self.candidates.append(candidate)

    def listCandidates(self):
        return self.candidates

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "candidates": [c.to_dict() for c in self.candidates]
    }

    @staticmethod
    def from_dict(data):
        job = Job(data["title"], data["status"])
        for cand_data in data.get("candidates", []):
            job.addCandidate(Candidate.from_dict(cand_data))
        return job

