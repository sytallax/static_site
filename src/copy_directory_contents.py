import os
import shutil


def copy_directory_contents(directory_to_search: str, destination_directory: str):
    if not os.path.exists(directory_to_search):
        raise Exception("Attempted to search directory that doesn't exist")

    if os.path.exists(destination_directory):
        print(f"Clearing destination directory '{destination_directory}' for new files")
        shutil.rmtree(destination_directory)

    print(f"Creating destination directory '{destination_directory}'")
    os.mkdir(destination_directory)

    directory_contents = os.listdir(directory_to_search)
    for item in directory_contents:
        item_path = os.path.join(directory_to_search, item)
        if os.path.isfile(item_path):
            print(f"Copying file '{item_path}, to '{destination_directory}'")
            shutil.copy(item_path, destination_directory)
        else:
            new_destination_directory = os.path.join(destination_directory, item)
            copy_directory_contents(item_path, new_destination_directory)
