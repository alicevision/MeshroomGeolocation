import os
from py7zr import unpack_7zarchive
import shutil

def unzip(ArchiveToUnzip, OutputFolder):
    # Convert the path to the right format
    dir_unzip = ArchiveToUnzip
    # dir_unzip = ArchiveToUnzip.replace('/', '\\')

    # Unzip the archive
    shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
    shutil.unpack_archive(dir_unzip, OutputFolder)

    # Rename the folder
    with os.scandir(OutputFolder) as itr:
        for entry in itr:
            if entry.is_dir():
                old_name = entry.name
                os.rename(OutputFolder+r'/'+old_name, OutputFolder+'/unzip')

    return OutputFolder+'/unzip'
