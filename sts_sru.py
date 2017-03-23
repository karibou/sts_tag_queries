#!/usr/bin/python3
#
# sts-sru : Get a list of LP bugs with sts-sru tag
#
# Copyright (C) 2016 Louis bouchard <louis.bouchard@canonical.com>
#

import argparse
from BugTasks import BugTasks


def main(long):
    sru = BugTasks()
    sru.login()
    sru.get_all_tasks('sts-sru-needed')
    sru.display_report(long, 'sts-sru-needed')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--long', help='Display series and owners',
                        action='store_true')
    args = parser.parse_args()
    main(args.long)
