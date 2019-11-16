from codecs import open as codecs_open
from difflib import SequenceMatcher
from logging import info
from os import walk, rmdir
from time import sleep

from format_byte import format_byte
from os.path import join
from send2trash import send2trash
from utility.logger import Logger
from utility.os_interface import depth_search_files, get_file_size, exists
from utility.path_str import get_clean_path
from utility.utilities import is_file_type


# from concurrent.futures import ProcessPoolExecutor


def delete_empty_directories(path):
    for f_path, sub_dirs, files in sorted(walk(path), key=lambda x: len(x[0]), reverse=True):
        if sub_dirs == [] and files == []:
            try:
                rmdir(get_clean_path(f_path))
            except Exception as e:
                info(e)


def show_dialog(s):
    for i in reversed(range(s)):
        sleep(1)
        info(str(i) + "...")


def read_file_data(path, name):
    with codecs_open(join(path, name), "rb") as f:
        data = f.read()
    info(data)
    return data


def is_similar_fit(a, b, limit=1.0):
    similarity = SequenceMatcher(None, a, b).ratio()
    if similarity >= limit:
        return True
    return False


def is_similar_size(o_file, d_file):
    # SIZE
    o_size = get_file_size(o_file[0], o_file[1])
    d_size = get_file_size(d_file[0], d_file[1])
    return abs(d_size - o_size) < (d_size * 0.1)


def is_duplicate(d_file, original_list, limit):
    if d_file[1] in original_list:
        info("Duplicat NAME:  " + d_file[1])
        info("Original NAME:  " + d_file[1] + '\n')
        return True
    if limit < 1.0:
        for o_file in original_list.keys():
            # NAME
            if is_similar_fit(o_file, d_file[1], limit):
                """# PATH not the same
                if original_list[o_file] != d_file[0]:"""
                info("Duplicat NAME:  " + d_file[1])
                info("Original NAME:  " + o_file + '\n')
                return True
    return False


def remove_duplicates(duplicate_list, original_list, limit):
    count_size = 0
    deleted_count = 0

    for d_file in duplicate_list:

        if is_duplicate(d_file, original_list, limit):
            d_size = get_file_size(d_file[0], d_file[1])

            full_path = join(*d_file).replace('/', '\\')
            # info(full_path)
            if exists(full_path):
                send2trash(full_path)
            else:
                raise OSError
            count_size += d_size
            deleted_count += 1

    info("TOTAL SIZE DELETE: " + format_byte(count_size))
    info("DELETE:  " + str(deleted_count) + " of " + str(len(duplicate_list)))


def depth_search_files_dict(path, types):
    result = {}
    for f_path, sub_dirs, files in walk(path):
        for file_name in files:
            if is_file_type(file_name=file_name, types=types):
                result[file_name] = f_path

    return result


def delete_duplicates(f_type, duplicate_path, original_path, warning_time=5, limit=1.0):
    deleted_count = 0
    count_size = 0
    duplicate_path, original_path = get_clean_path(duplicate_path), get_clean_path(original_path)
    delete_empty_directories(duplicate_path)

    if original_path.startswith(duplicate_path) or duplicate_path.startswith(original_path):
        raise NotImplementedError
        info("Both paths are the same")
        original_list = duplicate_list = depth_search_files(duplicate_path, f_type)

    else:
        original_list = depth_search_files_dict(original_path, f_type)
        duplicate_list = depth_search_files(duplicate_path, f_type)
        # original_list = sorted(original_list, key=lambda x: x[1])  # sort alphabet
        # original_list = sorted(original_list, key=lambda x: len(x[1]))  # sort lenght of file name
        # duplicate_list = sorted(duplicate_list, key=lambda x: x[1])
        # duplicate_list = sorted(duplicate_list, key=lambda x: len(x[1]))
    d_len = len(duplicate_list)

    info("DELETE FROM   " + duplicate_path)
    info("COMPARE TO    " + original_path)
    info("Duplicate Files: " + str(d_len))
    info("Original  Files: " + str(len(original_list)))
    info("Files: " + str(d_len + len(original_list)))
    show_dialog(warning_time)

    remove_duplicates(duplicate_list, original_list, limit)

    delete_empty_directories(duplicate_path)
    return
    # thread_max = 1
    # info("Threads: " + str(thread_max))
    # with ThreadPoolExecutor(max_workers=thread_max) as executor:
    #    for i in range(thread_max):
    #        executor.submit(remove_duplicates, duplicate_list[i:d_len:thread_max], original_list)


def continuously_delete_duplicates(f_type, duplicate_path, original_path, limit, warning_time=0):
    while True:
        # for t in [""]:  # [".mp3", ".jpg", ".m4a", ".flac", ".flv", ".avi", ".wma", ".ogg", ".wav"]:
        delete_duplicates(f_type=f_type, duplicate_path=duplicate_path, original_path=original_path,
                          warning_time=warning_time, limit=limit)


if __name__ == "__main__":
    with Logger():
        delete_duplicates(f_type=[""],
                          duplicate_path="",
                          original_path="",
                          warning_time=5,
                          limit=0.85)
