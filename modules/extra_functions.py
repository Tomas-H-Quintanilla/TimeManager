

from datetime import datetime
import time

def transform_tasks_csv(tasks,lines=[]):
    for task in tasks:
        if task.date:
            task.date=task.date.strftime("%d-%m-%Y")
            if task.minutes:
                task.hours=int(task.minutes/60)
                task.minutes_used=int(task.minutes%60)
        lines.append(f'{task.project.project.name},{task.task_content},{task.date},{task.hours},{task.minutes_used},{task.project.project.manager.username} \n')
    return lines

def getDataFilter(date_str):
    filter_date=datetime.fromtimestamp(0)
    if date_str=="today":
        today = datetime.today()
        d1 = today.strftime("%d/%m/%Y")
        filter_date = datetime.strptime(d1, "%d/%m/%Y")
    elif date_str=="week":
        filter_date=datetime.fromtimestamp(time.time()-3600*7*24)
    elif date_str=="month":
        filter_date=datetime.fromtimestamp(time.time()-3600*24*30)
    elif date_str=="year":
        filter_date=datetime.fromtimestamp(time.time()-3600*7*24*365)
    
    return filter_date