import tkinter as tk
from tkinter import filedialog
import os
import datetime
import re
import pandas as pd

def parse_files_in_directory(directory_path):
    parsed_data = {'Date': [], 'Balance': [], 'Currency': []}
    for filename in os.listdir(directory_path):
        if "DataLog" in filename and filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            result = parse_file(file_path)
            if isinstance(result, list):
                for entry in result:
                    parsed_data['Date'].append(entry['Date'])
                    parsed_data['Balance'].append(entry['Balance'])
                    parsed_data['Currency'].append(entry['Currency'])

    return parsed_data

def parse_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            parsed_data = []
            current_date = None
            for line in lines:
                match = re.search(r'(\d{8}-\d{2}:\d{2}:\d{2}.\d{3}).*USD Margin Bal: ([\d ]+) USD', line)
                if match:
                    date_time_str, value = match.groups()
                    date_time_obj = datetime.datetime.strptime(date_time_str, "%Y%m%d-%H:%M:%S.%f")

                    if datetime.time(12, 0, 0) <= date_time_obj.time() <= datetime.time(12, 1, 0):
                        if current_date != date_time_obj.date():
                            current_date = date_time_obj.date()
                            parsed_data.append({
                                'Date': date_time_obj.strftime('%Y%m%d'),
                                'Balance': ' '.join(value.split()),  # Удаляем лишние пробелы
                                'Currency': 'USD'
                            })

            return parsed_data
    except Exception as e:
        return str(e)

def start_parsing(directory_path):
    result = parse_files_in_directory(directory_path)

    if isinstance(result, dict):
        output_file_path = os.path.join(directory_path, "pars.xlsx")
        df = pd.DataFrame(result)
        df.to_excel(output_file_path, index=False)
        print(f"Parsing complete. Results saved in 'pars.xlsx' in the selected directory.")
    else:
        print("Error:", result)

def select_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        start_parsing(directory_path)

root = tk.Tk()
root.title("Directory Parser")

directory_button = tk.Button(root, text="Выбрать директорию", command=select_directory)
directory_button.pack(pady=20)

root.mainloop()
