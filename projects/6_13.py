from pathlib import Path
import shutil

def create_backup(path, file_name, employee_residence):
    # folder_path = Path(path)
    # file_path = Path(file_name)
    # full_path = folder_path / file_path
    with open(path + '/' + file_name, 'wb') as fh:
        for name, country in employee_residence.items():
            result = f'{name} {country}\n'
            result_byte = result.encode() # bytes(result, 'utf-8')
            fh.write(result_byte)
    return shutil.make_archive('backup_folder', 'zip', path)