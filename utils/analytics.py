from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.pyplot as plt
from collections import Counter

def getCoverageFillStatus(companies):
    totalCoverage = 0
    totalFilled = 0

    for company in companies:
        for job in company.jobs:
            if job.status.lower() != "open":
                continue

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
    ax.set_title("Coverage %")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def renderCandidateStatusChart(frame, companies):
    # LIMPA qualquer gráfico anterior
    for widget in frame.winfo_children():
        widget.destroy()

    # Calcula dados
    status_count = {}
    for company in companies:
        for job in company.jobs:
            for candidate in job.candidates:
                status = candidate.status
                status_count[status] = status_count.get(status, 0) + 1

    statuses = list(status_count.keys())
    counts = list(status_count.values())

    # Cria gráfico
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(range(len(statuses)), counts, color='skyblue')
    ax.set_title("Candidates per Status")
    ax.set_ylabel("Count")
    ax.set_xlabel("Status")
    ax.set_xticks(range(len(statuses)))
    ax.set_xticklabels(statuses, rotation=45, ha='right', fontsize=9)

    fig.tight_layout(pad=1.0)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
