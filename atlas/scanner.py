
""" This module is used for scanning and indexing streamable media

Typical usage:
    run_scanner("/home/test/media","/usr/var/Loki/loki.db")
"""

import os
import sqlite3

def _tree(start_dir):
    """ Lists all files in start_dir and its subdirectories

    Args:
        start_dir: path of dir to be scanned for files.

    Returns:
        A list of paths, all leading to a file
        example:
        [
            "foo/bar/car.txt",
            "foo/bar/dar.mp3",
            "foo/mar.avi",
        ]
    """
    parent_path = os.path.abspath(start_dir)
    files_in_dir = os.listdir(start_dir)
    files = []
    for entry in files_in_dir:
        full_path = os.path.join(parent_path, entry)
        if os.path.isdir(full_path):
            files = files + _tree(full_path)
        else:
            files.append(full_path)

    return files


def _is_media_file(file):
    """ Checks if file is a supported file type

    Args:
        file: path to file

    Returns:
        A boolean value, True if the suffix of the file
        matches one of the supported suffixes
    """
    supported_formats = (".mkv", ".avi", ".mp4")
    return file.endswith(supported_formats)

def run_scanner(start_dir, media_type, db_loc):
    """
    Scanns start_dir for media files and creates an index of them
    in a database located in db_loc

    Args:
        start_dir: A path to the folder containing media files
        media_type: A string describing the type of media for
                   helping in choosing the right scrapper later
        db_loc: The location for the database
    """
    conn = sqlite3.connect(db_loc)
    count = 0
    dupplicates = 0

    all_media = filter(_is_media_file, _tree(start_dir))
    for path in all_media:
        try:
            with conn:
                conn.execute('INSERT INTO res_index(file_path,media_type) VALUES (?,?);', [path,media_type])
                count += 1
        except sqlite3.IntegrityError:
            dupplicates += 1

    conn.close()
    return (count,dupplicates)
    