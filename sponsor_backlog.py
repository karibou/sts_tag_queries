#!/usr/bin/python3
#
# sponsor_backlog : Get a list of LP bugs with sts-sponsor tag
#
# Copyright (C) 2016 Louis bouchard <louis.bouchard@canonical.com>
#

from BugTasks import BugTasks


def main():
    sponsors = BugTasks()
    sponsors.login()
    sponsors.get_all_tasks('sts-sponsor')
    sponsors.display_report()

if __name__ == "__main__":
    main()
