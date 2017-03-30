#!/usr/bin/python3
#
# sts-sru : Get a list of LP bugs with sts-sru tag
#
# Copyright (C) 2016 Louis bouchard <louis.bouchard@canonical.com>
#

import argparse
import sys
from BugTasks import BugTasks

tag = None

def main(arguments):
    sru = BugTasks()
    sru.login()
    if arguments.sru:
        tag = 'sts-sru-needed'
    if arguments.sponsor:
        tag = 'sts-sponsor'

    if arguments.ubuntu:
        sru.get_ubuntu_tasks(tag)
    if arguments.uca:

        sru.get_uca_tasks(tag)
    if arguments.openstack:
        sru.get_openstack_tasks(tag)

    sru.display_report(arguments.long, tag)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--long', help='Display series and owners',
                        action='store_true')
    parser.add_argument('-o', '--openstack', help='Display openstack bugs\
                        this can be a lengthy process as it needs to scan\
                        all openstack projects', action='store_true')
    parser.add_argument('-u', '--ubuntu', help='Display Ubuntu bugs',
                        action='store_true')
    parser.add_argument('-U', '--uca', help='Display Ubuntu Cloud Archive\
                        bugs', action='store_true')
    parser.add_argument('-s', '--sru', help='Display bugs with sts-sru-needed\
                        tag', action='store_true')
    parser.add_argument('-S', '--sponsor', help='Display bugs with sts-sponsor\
                        tag', action='store_true')

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()
    args = parser.parse_args()

    main(args)
