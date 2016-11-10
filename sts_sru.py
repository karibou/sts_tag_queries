#!/usr/bin/python3
#
# sts-sru : Get a list of LP bugs with sts-sru tag
#
# Copyright (C) 2016 Louis bouchard <louis.bouchard@canonical.com>
#

from BugTasks import BugTasks


def main():
    sru = BugTasks()
    sru.login()
    sru.get_all_tasks('sts-sru')
    sru.display_report()

if __name__ == "__main__":
    main()
