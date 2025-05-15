from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def getCoverageFillStatus(companies):
    totalCoverage = 0
    totalFilled = 0

    for company in companies:
        for job in company.jobs:
            totalCoverage += job.coverage
            for candidate in job.candidates:
                status = candidate.status.lower()
                if status == "submitted" or "interview" in status:
                    totalFilled += 1

    return totalCoverage, totalFilled


def renderFillProgressChart(frame, companies):
    totalCoverage, totalFilled = getCoverageFillStatus(companies)
    remaining = max(totalCoverage - totalFilled, 0)
    fig, ax = plt.subplots(figsize=(5, 4))

    ax.pie(
        [totalFilled, remaining],
        labels=["Filled", "Available"],
        colors=["green", "grey"],
        autopct='%1.1f%%',
        startangle=90
    )
    ax.set_title("Total coverage VS Current coverage")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()