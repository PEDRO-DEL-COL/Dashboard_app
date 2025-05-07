class Job:
    def __init__(self, title, status):
        self.title = title
        self.status = status

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Job(data["title"], data["status"])

    def __str__(self):
        return f"{self.title} ({self.status})"

