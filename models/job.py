from models.candidate import Candidate

class Job:
    def __init__(self, title, status, coverage):
        self.title = title
        self.status = status
        self.coverage = coverage
        self.candidates = []

    def addCandidate(self, candidate):
        self.candidates.append(candidate)

    def listCandidates(self):
        return self.candidates

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "coverage": self.coverage,
            "candidates": [c.to_dict() for c in self.candidates]
    }

    @staticmethod
    def from_dict(data):
        coverage = data.get("coverage", 0)  # <-- Aqui usamos .get() com valor padrão
        job = Job(data["title"], data["status"], coverage)
        for cand_data in data.get("candidates", []):
            job.addCandidate(Candidate.from_dict(cand_data))
        return job


