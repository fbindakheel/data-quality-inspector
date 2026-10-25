import csv

def csv_loader():
    reader_data = []
    with open("D:/python-practice/Data_quality_website/data/data_quality_inspector_10000.csv", "r", encoding="utf-8", newline='') as file:
        reader = csv.DictReader(file)
        for r in reader:
            reader_data.append(r)
    return reader_data