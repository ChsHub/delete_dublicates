from logging import info, error
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from utility.logger import Logger
from utility.os_interface import depth_search_files, get_file_size, delete_file
from difflib import SequenceMatcher


def show_dialog(s):
    for i in reversed(range(s)):
        sleep(1)
        print(str(i) + "...")


def is_similar_fit(a, b):
    similarity = SequenceMatcher(None, a, b).ratio()
    if similarity >= 0.85:
        # info("#ACCEPT " + str(similarity))
        return True
    return False


def is_duplicate(d_file, original_list):
    for o_file in original_list:
        # NAME
        # :
        # if o_file[1] == d_file[1] or \
        if is_similar_fit(o_file[1], d_file[1]):
            # PATH
            if o_file[0] != d_file[0]:
                # SIZE TODO
                if get_file_size(o_file[0], o_file[1]) >= get_file_size(d_file[0], d_file[1]):
                    #  info("Original Path:  " + o_file[0])
                    info("Original NAME:  " + o_file[1])
                    # logging.info("Original Name:  " + o_file[1])
                    original_list.remove(o_file)
                    return True
    return False


def remove_duplicates(dublicate_list, original_list):
    count_size = 0
    deleted_count = 0
    for d_file in dublicate_list:

        try:
            # logging.info("TEST FILE:  " + d_file[1])
            # if d_file[1] != "Collection": TODO ????
            if is_duplicate(d_file, original_list):
                # info("Duplicat Path:  " + d_file[0])
                info("Duplicat NAME:  " + d_file[1])
                d_size = get_file_size(d_file[0], d_file[1])
                # info("Duplicat Size:  " + str(d_size))

                # show_dialog(4)
                if delete_file(d_file[0], d_file[1]):
                    count_size += d_size
                    #  info("TOTAL SIZE DELETE:  " + str(count_size))
                    deleted_count += 1
        except Exception as e:
            error(e)

    info("TOTAL SIZE DELETE:  " + str(count_size))
    info("DELETE:  " + str(deleted_count) + " of " + str(len(dublicate_list)))


def delete_dublicates(f_type, dublicate_path, original_path, warning_time=5):
    log = Logger()
    deleted_count = 0
    count_size = 0

    if original_path == dublicate_path:
        info("Both paths are the same")
        original_list = dublicate_list = depth_search_files(dublicate_path, f_type)

    else:
        original_list = depth_search_files(original_path, f_type)
        dublicate_list = depth_search_files(dublicate_path, f_type)
        original_list = sorted(original_list, key=lambda x: x[1])
        dublicate_list = sorted(dublicate_list, key=lambda x: x[1])
    d_len = len(dublicate_list)

    info("DELETE FROM   " + dublicate_path)
    info("COMPARE TO    " + original_path)
    info("Files: " + str(d_len + len(original_list)))
    show_dialog(warning_time)

    # remove_duplicates(dublicate_list, original_list, count_size,
    # deleted_count)
    thread_max = 4
    info("Threads: " + str(thread_max))
    with ThreadPoolExecutor(max_workers=thread_max) as executor:
        for i in range(thread_max):
            executor.submit(remove_duplicates, dublicate_list[i:d_len:thread_max], original_list)

    log.shutdown()


def continuously_delete_dublicates(dublicate_path, original_path):
    while True:
        for t in [""]:  # [".mp3", ".jpg", ".m4a", ".flac", ".flv", ".avi", ".wma", ".ogg", ".wav"]:
            delete_dublicates(f_type=t, dublicate_path=dublicate_path, original_path=original_path,
                              warning_time=0)
        #            delete_dublicates(f_type=t, dublicate_path=dublicate_path, original_path=original_path,
        #                             warning_time=0)


delete_dublicates(f_type=[""], dublicate_path="D:/Downloads/Handy Alt Merge/Anderes",
                  original_path="D:/Musik",
                  warning_time=5)
