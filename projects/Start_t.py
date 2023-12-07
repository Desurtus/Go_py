import os
import shutil
import string
import zipfile
import datetime
import sys

def create_category_folders(root_folder):
    categories = ['images', 'video', 'documents', 'audio', 'programm', 'archives', 'extensions']
    for category in categories:
        category_path = os.path.join(root_folder, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        elif not os.path.isdir(category_path):
            print(f'Error: {category} is not a directory!')

def normalize(name):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'з': 'z', 'и': 'i', 'й': 'y',
        'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ъ': '', 'ы': 'y', 'э': 'e'
    }

    base, extension = os.path.splitext(name)
    translit_name = ''.join(translit_dict.get(char, char.lower()) if char.islower() else translit_dict.get(char.lower(), char) for char in base)
    valid_chars = f"{string.ascii_letters}{string.digits}_"
    normalized_name = ''.join(c if c in valid_chars else '_' for c in translit_name)

    # Сохранение верхнего регистра для расширения файла
    normalized_name_with_extension = normalized_name + extension

    return normalized_name_with_extension

def process_folder(folder_path, root_folder, ignored_categories):
    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path):
            if item not in ignored_categories:
                process_folder(item_path, root_folder, ignored_categories)
        else:
            process_file(item_path, root_folder)

    # Проверка, является ли папка пустой, и удаление ее
    if not os.listdir(folder_path):
        os.rmdir(folder_path)

def process_file(file_path, root_folder):
    _, extension = os.path.splitext(file_path)
    extension = extension[1:].upper()

    if extension in ('JPEG', 'PNG', 'JPG', 'SVG'):
        move_and_rename(file_path, 'images', root_folder)
    elif extension in ('AVI', 'MP4', 'MOV', 'MKV'):
        move_and_rename(file_path, 'video', root_folder)
    elif extension in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'XLSX', 'PPTX'):
        move_and_rename(file_path, 'documents', root_folder)
    elif extension in ('MP3', 'OGG', 'WAV', 'AMR'):
        move_and_rename(file_path, 'audio', root_folder)
    elif extension in ('PY', 'SLN'):
        move_and_rename(file_path, 'programm', root_folder)
    elif extension in ('ZIP', 'GZ', 'TAR'):
        try:
            extract_and_move(file_path, 'archives', root_folder)
        except zipfile.BadZipFile:
            print(f'Warning: Failed to extract {file_path}. Deleting the corrupted archive.')
            os.remove(file_path)
    else:
        move_and_rename(file_path, 'extensions', root_folder)

def move_and_rename(file_path, category, root_folder):
    normalized_name = normalize(os.path.basename(file_path))
    category_path = os.path.join(root_folder, category)

    # Проверка наличия подпапки внутри категории
    if not os.path.exists(category_path):
        os.makedirs(category_path)
    elif not os.path.isdir(category_path):
        print(f'Error: {category} is not a directory!')
        return

    new_path = os.path.join(category_path, normalized_name)
    shutil.move(file_path, new_path)
    print(f'Moved to {category}: {normalized_name}')

def extract_and_move(archive_path, category, root_folder):
    normalized_name = normalize(os.path.basename(archive_path))
    category_path = os.path.join(root_folder, category)

    # Проверка наличия подпапки внутри категории
    if not os.path.exists(category_path):
        os.makedirs(category_path)
    elif not os.path.isdir(category_path):
        print(f'Error: {category} is not a directory!')
        return

    try:
        # Проверка, является ли файл zip-архивом
        if zipfile.is_zipfile(archive_path):
            extracted_folder = os.path.join(category_path, os.path.splitext(normalized_name)[0])

            # Проверка наличия подпапки с именем архива
            if not os.path.exists(extracted_folder):
                os.makedirs(extracted_folder)

            shutil.unpack_archive(archive_path, extracted_folder)

            # Перемещение извлеченной папки с именем архива
            if os.path.exists(extracted_folder):
                extracted_folder_name = os.path.splitext(normalized_name)[0]
                extracted_folder_name = extracted_folder_name.replace('.', '_')
                # Используем относительные пути при перемещении
                shutil.move(extracted_folder, os.path.join(category_path, extracted_folder_name))
                print(f'Extracted and moved to {category}: {extracted_folder_name}')
            else:
                print(f'Error: Failed to extract {archive_path}. The extracted folder does not exist.')

            # Удаление распакованного архива
            os.remove(archive_path)

        else:
            print(f'Error: {archive_path} is not a valid zip archive.')
            os.remove(archive_path)

    except zipfile.BadZipFile:
        print(f'Warning: Failed to extract {archive_path}. Deleting the corrupted archive.')
        os.remove(archive_path)

def list_files_in_category(category_path):
    try:
        files = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
        return files
    except FileNotFoundError:
        return []

def list_known_extensions(root_folder):
    known_extensions = set()
    for category in ['images', 'video', 'documents', 'audio', 'programm', 'archives']:
        category_path = os.path.join(root_folder, category)
        files = list_files_in_category(category_path)
        extensions = {os.path.splitext(file)[1].upper().lstrip('.') for file in files}  # Убираем точку в начале расширения
        known_extensions.update(extensions)
    return known_extensions


def list_unknown_extensions(root_folder):
    unknown_extensions = set()
    for category in ['extensions']:
        category_path = os.path.join(root_folder, category)
        files = list_files_in_category(category_path)
        extensions = {os.path.splitext(file)[1].upper().lstrip('.') for file in files}  # Убираем точку в начале расширения
        unknown_extensions.update(extensions)
    return unknown_extensions

   

def write_results_to_file(root_folder, known_extensions, unknown_extensions, deleted_archives, processed_extensions):
    result_file_path = os.path.join(root_folder, 'results.txt')
    timestamp = None  # Инициализация переменной timestamp

    with open(result_file_path, 'w') as file:
        file.write("List of files in each category:\n")
        for category in ['images', 'video', 'documents', 'audio', 'programm', 'archives', 'extensions']:
            category_path = os.path.join(root_folder, category)
            try:
                files = list_files_in_category(category_path)
                if category == 'archives':
                    file.write(f"{category}: {', '.join(files)}\n")
                else:
                    file.write(f"{category}: {', '.join(files)}\n")
            except FileNotFoundError:
                print(f"Warning: Category {category} not found.")

        file.write("\nList of known extensions:\n")
        file.write(', '.join(processed_extensions))

        # Write List of unknown extensions to file
        file.write("\n\nList of unknown extensions:\n")
        file.write(', '.join(unknown_extensions))

        if deleted_archives:
            file.write("\n\nDeleted corrupted archives:\n")
            file.write(', '.join(deleted_archives))

        # Add timestamp to the end of the file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"\n\nProgram executed at: {timestamp}")

    print(f"Results written to: {result_file_path}")
    print(f"Program executed at: {timestamp}")

    return timestamp  # Вернуть timestamp после завершения функции

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    create_category_folders(folder_path)

    ignored_categories = ['archives', 'extensions']
    process_folder(folder_path, folder_path, ignored_categories)

    known_extensions = list_known_extensions(folder_path)
    unknown_extensions = list_unknown_extensions(folder_path)

    deleted_archives = []

    # Проверка и удаление поврежденных архивов
    for category in ['archives']:
        category_path = os.path.join(folder_path, category)
        try:
            files = list_files_in_category(category_path)
            for archive in files:
                archive_path = os.path.join(category_path, archive)
                try:
                    with zipfile.ZipFile(archive_path) as test_zip:
                        test_zip.extractall(os.path.join(folder_path, 'temp'))
                except zipfile.BadZipFile:
                    print(f'Warning: Deleting corrupted archive: {archive}')
                    deleted_archives.append(archive)
                    os.remove(archive_path)
        except FileNotFoundError:
            print(f"Warning: Category {category} not found.")

    # Write results to file
    processed_extensions = list_known_extensions(folder_path)
    timestamp = write_results_to_file(folder_path, known_extensions, unknown_extensions, deleted_archives, processed_extensions)

    # Print lists on the screen
    print("\nList of files in each category:")
    for category in ['images', 'video', 'documents', 'audio', 'programm', 'archives', 'extensions']:
        category_path = os.path.join(folder_path, category)
        try:
            files = list_files_in_category(category_path)
            print(f"{category}: {', '.join(files)}")
        except FileNotFoundError:
            print(f"Warning: Category {category} not found.")

    print("\nList of known extensions:")
    print(', '.join(known_extensions))

    print("\nList of unknown extensions:")
    print(', '.join(unknown_extensions))

    if deleted_archives:
        print("\nDeleted corrupted archives:")
        print(', '.join(deleted_archives))

    print("\nSorting completed.")
