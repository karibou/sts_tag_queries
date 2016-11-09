#!/usr/bin/python3
#
# sts-sru : Get a list of LP bugs that needs sponsership
#
# Copyright (C) 2016 Louis bouchard <louis.bouchard@canonical.com>
#

from launchpadlib.launchpad import Launchpad as lp

valid_series = ['precise', 'trusty', 'xenial', 'yakkety']
def get_sponsorship_requests():
    launchpad = lp.login_anonymously('sts_sponsor', 'production', version='devel')
    for serie in valid_series:
        print("Sponsorship request for %s" % serie)
        ubuntu = launchpad.distributions['ubuntu'].getSeries(name_or_version=serie)
        tasks = ubuntu.searchTasks(tags='sts-sponsor', created_since='2015-01-01',order_by='id')
        for task in tasks:
            print('  LP: #%d - %s %s' % (task.bug.id, task.bug_target_name, task.bug.title))
            if task.assignee is not None:
                print('  - Owner : %s\t status: %s' % (task.assignee.display_name, task.status))
            else:
                print('  - Owner : Unowned\t status: %s'% task.status)


def main():
    get_sponsorship_requests()

if __name__ == "__main__":
    main()
