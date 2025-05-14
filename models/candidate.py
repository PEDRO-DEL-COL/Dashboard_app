class Candidate:
    def __init__(self, name, status):
        self.name = name
        self.status = status

    def to_dict(self):
        return {
            "name": self.name,
            "status": self.status
        }
    
    @staticmethod
    def from_dict(data):
        return Candidate(data["name"], data["status"])

    def __str__(self):
        return f"{self.name} ({self.status})"