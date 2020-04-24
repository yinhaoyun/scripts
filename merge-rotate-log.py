#!/usr/bin/python3
# coding=utf-8

import os
import re
import sys
import time

FILE_PREFIX = 'logcat'
COLUMNS, LINES = os.get_terminal_size()
if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")


def is_log_file_name(name):
    if name == FILE_PREFIX:
        return True
    elif re.match('^' + FILE_PREFIX + '\.\d+$', name):
        return True
    else:
        return False


def human_readable_byte_count(size, si=True, point=1):
    unit = 1024 if si else 1000
    readable = 'KMGTPEZ'
    i = -1
    while size // unit > 0:
        size /= unit
        i += 1
    if i == -1:
        return str(size) + ' bytes'
    format_string = '{:.%df} {}B' % point
    return format_string.format(size, readable[i])


def read_in_chunks(infile, chunk_size=1024*64):
    while True:
        chunk = infile.read(chunk_size)
        if chunk:
            yield chunk
        else:
            return


all_files = os.listdir('.')
log_files = [file for file in all_files if is_log_file_name(file)]
log_files.sort()
log_files.reverse()
total_size = sum([os.stat(file).st_size for file in log_files])
total_count = len(log_files)

answer = ''
while answer[:1].lower() != 'y' and answer[:1].lower() != 'n':
    print('Files to be merge: {} ~ {}, total {} files'.format(log_files[0], log_files[-1], len(log_files)))
    print('Merge file size: %s' % human_readable_byte_count(total_size))
    answer = input('Merge? (Y/n): ')
    if answer == '':
        answer = 'y'

if answer[:1].lower() == 'n':
    exit(1)

if len(log_files) == 0:
    print('No log files?', file=sys.stderr)
    exit(1)

merged_count = 0
bytes_written = 0

start_time = time.time()
with open('merge.log', 'wb') as out_file:
    for log in log_files:
        print('[%3d%%, %s, %d/%d] Appending %s...       ' % (bytes_written*100//total_size,
                                                             human_readable_byte_count(bytes_written),
                                                             merged_count,
                                                             total_count,
                                                             log))
        with open(log, 'rb') as infile:
            bytes_written_file = 0
            for chunk in read_in_chunks(infile):
                length = out_file.write(chunk)
                bytes_written += length
                bytes_written_file += length
            merged_count += 1

end_time = time.time()

print('[%3d%%, %s, %d/%d] Complete! (%f seconds)' % (bytes_written*100//total_size,
                                                     human_readable_byte_count(bytes_written),
                                                     merged_count,
                                                     total_count,
                                                     end_time - start_time))

answer = ''
while answer[:1].lower() != 'y' and answer[:1].lower() != 'n':
    answer = input("Delete unmerged logcat files? (Y/n): ")
    if answer == '':
        answer = 'y'

if answer[:1].lower() == 'y':
    for f in log_files:
        os.remove(f)
