#!/usr/bin/python3
#
# sponsors_backlog : Get a list of LP bugs with sts-sponsors tag
#
# Copyright (C) 2016 Louis bouchard <louis.bouchard@canonical.com>
#

import argparse
from BugTasks import BugTasks


def main(long):
    sponsors = BugTasks()
    sponsors.login()
    sponsors.get_all_tasks('sts-sponsor')
    sponsors.display_report(long)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--long', help='Display series and owners',
                        action='store_true')
    args = parser.parse_args()
    main(args.long)
