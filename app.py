from flask import Flask, request, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

def estimate_task_time(task):
    task = task.lower()
    if "cook" in task or "lunch" in task or "dinner" in task:
        return 60
    elif "study" in task or "review" in task:
        return 90
    elif "email" in task or "check" in task:
        return 20
    elif "exercise" in task or "workout" in task:
        return 45
    elif "nap" in task or "sleep" in task:
        return 30
    elif "wash" in task or "clean" in task:
        return 30
    elif "meeting" in task or "call" in task:
        return 60
    elif "write" in task or "blog" in task or "report" in task:
        return 75
    else:
        return 30  # Default fallback

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/schedule', methods=['POST'])
def schedule_tasks():
    tasks = request.form.getlist('task')
    start_time = request.form.get('start_time', '08:00')
    end_time = request.form.get('end_time', '20:00')

    fmt = "%H:%M"
    start = datetime.strptime(start_time, fmt)
    end = datetime.strptime(end_time, fmt)
    total_minutes = (end - start).seconds // 60

    # Estimate and sort tasks by duration (descending)
    task_durations = [(task, estimate_task_time(task)) for task in tasks]
    task_durations.sort(key=lambda x: -x[1])  # Highest duration = highest priority

    schedule = {}
    current = start
    for task, duration in task_durations:
        if (current + timedelta(minutes=duration)) > end:
            break  # Skip tasks that don’t fit
        end_block = current + timedelta(minutes=duration)
        block = f"{current.strftime(fmt)} - {end_block.strftime(fmt)}"
        schedule[block] = f"{task} ({duration} min)"
        current = end_block

    return render_template("index.html", schedule=schedule)

if __name__ == '__main__':
    app.run(debug=True)
