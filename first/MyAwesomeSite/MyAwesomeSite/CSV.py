import csv

filename="C:\\Users\\LENOVO\\Desktop\\CSVFILE.csv"
rows=[]
with open(filename,"r") as csvfile:
    csvobject=csv.reader(csvfile)
    fields=csvobject.__next__
    print(str(fields))
    for row in csvobject:
        print(row)
        rows.append(row)
print(rows)