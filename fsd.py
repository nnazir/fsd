#!/usr/bin/env python3

import os
import sys
import bisect
import curses

size_buckets = [0,
                1,
                2,
                4,
                8,
                16,
                32,
                64,
                128,
                256,
                512,
                1024,
                2048,
                4096,
                8192,
                16384,
                32768,
                65536,
                131072,
                262144,
                524288,
                1048576,
                2097152,
                4194304,
                8388608,
                16777216,
                33554432,
                67108864,
                268435456,
                536870912, ]

distribution = [0] * len(size_buckets)

dir_count = 0
file_count = 0


def within_range(num):
    return bisect.bisect(size_buckets, num) - 1


def do_curses():

    root_dir = os.path.realpath(path)

    root_dir_banner = "Root directory: "

    screen = curses.initscr()

    curses.curs_set(0)

    processing_win = curses.newwin(2, curses.COLS - 1, 2, 17)

    screen.addstr(0, 0, "FSD: File Size Distribution")
    screen.addstr(1, 0, root_dir_banner)
    screen.addstr(2, 0, "Processing: ")
    screen.addstr(3, 0, "File Distribution:")
    screen.addstr(curses.LINES - 1, 0, "Files Processed: ")

    screen.addstr(1, len(root_dir_banner)+1, root_dir)

    count = 4
    for i in size_buckets:
        screen.addstr(count, 3, f"{i:12}: ")
        count += 1

    screen.refresh()

    dir_count = 0
    file_count = 0
    os.chdir(path)
    for root, dirs, files in os.walk('.'):
        for file_ in files:
            processing_win.clear()
            processing_win.addstr(0, 0, f"{root}/{file_}"[5:])
            processing_win.refresh()
            file_count += 1
            size = os.lstat(f'{root}/{file_}').st_size
            a = within_range(size)
            distribution[a] += 1
            screen.addstr(a+4, 18, str(distribution[a]))
            screen.addstr(curses.LINES - 1,
                          len("Files Processed: ") + 1, str(file_count))
            screen.refresh()
            curses.napms(1)
            screen.refresh()

        screen.refresh()

    processing_win.clear()
    processing_win.addstr(0, 0, "Done.")
    processing_win.refresh()
    screen.getch()
    curses.curs_set(1)
    curses.endwin()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        path = '.'
    else:
        path = sys.argv[1]

    do_curses()
