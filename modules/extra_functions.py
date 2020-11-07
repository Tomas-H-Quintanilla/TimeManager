
def transform_tasks_csv(tasks,lines=[]):
    for task in tasks:
        if task.date:
            task.date=task.date.strftime("%d/%m/%Y")
            if task.minutes:
                task.hours=int(task.minutes/60)
                task.minutes_used=int(task.minutes%60)
        lines.append(f'{task.project.project.name},{task.task_content},{task.date},{task.hours},{task.minutes_used},{task.project.project.manager.username} \n')
    return lines