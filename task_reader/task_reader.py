import csv


def csv_data(file):
    """Converts the data in the csv into an array.

    Args:
        file (string) --- Address of the file, literal is the best option.

    Returns:
        list --- Fields of the csv into a list of lists
    """
    
    with open(file,"r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        return list(csv_reader)
    
def read_data(file_csv,headers=False):
    
    data_csv=csv_data(file_csv)
    if headers==True:
        headers=data_csv.pop(0)
    
    objects=[]
    for dataset in data_csv:
        count=0
        objectData={}
        for data in dataset:
            objectData[headers[count].lower().replace(" ","_")]=data.capitalize()
            count=count+1
        
        objects.append(objectData)
    
    return objects
    

print(read_data('task_title_h.csv',True))
print(read_data('task_title_h.csv',headers=['task_content','project_name','date','hours','minutes']))