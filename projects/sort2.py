import os
import shutil
import string

def normalize(name):
    translit = str.maketrans("абвгдеёзийклмнопрстуфхъыэ", "abvgdeezijklmnoprstufh'y'e")
    name = name.lower().translate(translit)
    valid_chars = f"{string.ascii_lowercase}{string.digits}_"
    name = ''.join(c if c in valid_chars else '_' for c in name)
    return name

def process_folder(folder_path):
    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path):
            process_folder(item_path)
        else:
            process_file(item_path)

def process_file(file_path):
    _, extension = os.path.splitext(file_path)
    extension = extension[1:].upper()

    if extension in ('JPEG', 'PNG', 'JPG', 'SVG'):
        move_and_rename(file_path, 'images')
    elif extension in ('AVI', 'MP4', 'MOV', 'MKV'):
        move_and_rename(file_path, 'video')
    elif extension in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
        move_and_rename(file_path, 'documents')
    elif extension in ('MP3', 'OGG', 'WAV', 'AMR'):
        move_and_rename(file_path, 'audio')
    elif extension in ('ZIP', 'GZ', 'TAR'):
        extract_and_move(file_path, 'archives')
    else:
        pass

def move_and_rename(file_path, category):
    normalized_name = normalize(os.path.basename(file_path))
    category_path = os.path.join(os.getcwd(), category)
    os.makedirs(category_path, exist_ok=True)
    new_path = os.path.join(category_path, normalized_name)
    shutil.move(file_path, new_path)
    print(f'Moved to {category}: {normalized_name}')

def extract_and_move(archive_path, category):
    normalized_name = normalize(os.path.basename(archive_path))
    category_path = os.path.join(os.getcwd(), category)
    os.makedirs(category_path, exist_ok=True)
    shutil.unpack_archive(archive_path, category_path)
    extracted_folder = os.path.join(category_path, os.path.splitext(normalized_name)[0])
    os.rename(os.path.join(category_path, os.path.splitext(os.path.basename(archive_path))[0]), extracted_folder)
    print(f'Extracted and moved to {category}: {normalized_name}')

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    process_folder(folder_path)

    print("\nSorting completed.")
