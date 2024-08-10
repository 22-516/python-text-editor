import os
from print_color import print

from PyQt6.QtCore import *  # temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from filescontroller import *


def confirm_history_files_exist():  # make sure the file exists and all recent files exist before reading/writing
    create_file_directories()

    removed_file_paths_list = []  # remove all links that are no longer valid
    # with open(get_recent_file_path(), "r") as temp_recent_file_list:
    #     file_content = temp_recent_file_list.readlines()
    #     for line in file_content:
    #         line.strip()
    #         #print(line.strip(), os.path.exists(line.strip()), color="green")
    #         if not os.path.exists(line):
    #             removed_file_paths_list.append(line)
    #             print(line, " does not exist")
    for line in fetch_recent_file_list():
        if not os.path.exists(line):
            removed_file_paths_list.append(line)
            print(line, " does not exist")

    print(
        "removing files from recent file list", removed_file_paths_list, color="purple"
    )
    for removed_file_path in removed_file_paths_list:
        remove_path_from_recent_file_list(removed_file_path)


def fetch_recent_file_list():
    file_list = []
    with open(get_recent_file_path(), "r") as recent_file_list:
        while line := recent_file_list.readline():
            file_list.append(line.strip())

    return file_list


def prepend_recent_file_list(new_file_path=""):
    remove_path_from_recent_file_list(new_file_path)  # remove previous entry

    recent_file_list = fetch_recent_file_list()
    recent_file_list.insert(0, new_file_path)

    with open(get_recent_file_path(), "wt") as file_list:
        file_list.write("\n".join(str(line) for line in recent_file_list))


def remove_path_from_recent_file_list(removed_file_path=""):
    print(
        "removing from recent file list",
        removed_file_path,
        tag="history",
        tag_color="yellow",
        color="white",
    )
    removed_file_path.strip()

    file_list = fetch_recent_file_list()
    # print(removed_file_path in file_list, removed_file_path, file_list)
    if removed_file_path in file_list:  # remove the path from file array
        file_list.remove(removed_file_path)
        print(
            "successfully removed",
            removed_file_path,
            tag="history",
            tag_color="yellow",
            color="white",
        )

    with open(
        get_recent_file_path(), "w"
    ) as new_file_list:  # write array to recent file list
        new_file_list.write("\n".join(str(line) for line in file_list))

    # print(fetch_recent_file_list(), color="red")

    # with open(os.path.join("data", "recent.txt"), "r+") as recent_file_list:
    #     file_content = recent_file_list.readlines()
    #     recent_file_list.seek(0)
    #     recent_file_list.truncate()
    #     for line in file_content:
    #         if line.strip() != removed_file_path:
    #             recent_file_list.write(line.strip())

    # print(fetch_recent_file_list(), color="red")
