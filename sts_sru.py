#!/usr/bin/python3
#
# sts-sru : Get a list of LP bugs with sts-sru tag
#
# Copyright (C) 2016 Louis bouchard <louis.bouchard@canonical.com>
#

from launchpadlib.launchpad import Launchpad as lp


class OneSru():
    """ One single SRU """
    def __init__(self):
        self.title = ''
        self.owners = []
        self.series = []


class Sru():
    """ The SRU class
    The class logs into Launchpad and query the tasks
    to find the sts_sru tagged tasks
    """
    def __init__(self):
        self.all_srus = {}
        self.valid_series = ['precise', 'trusty', 'xenial', 'yakkety']
        self.lp = None
        self.ubuntu = None
        self.tasks = None

    def login(self):
        """
        Log into the production Launchpad instance
        version='devel' is important, otherwise no
        task will be returned
        """

        self.lp = lp.login_anonymously('sts_sru',
                                       'production', version='devel')

    def get_tasks_for_serie(self, serie):
        """
        Get all tasks tagged with sts_sru from one single
        serie. Put tasks in a list indexed by bug number
        """
        self.ubuntu = self.lp.distributions['ubuntu'].getSeries(
            name_or_version=serie)
        self.tasks = self.ubuntu.searchTasks(tags='sts-sru',
                                             created_since='2016-01-01',
                                             order_by='id')
        for task in self.tasks:
            if task.bug.id not in self.all_srus.keys():
                self.all_srus[task.bug.id] = OneSru()
                self.all_srus[task.bug.id].title = task.bug.title
                print("%s" % serie[0], end='', flush=True),
            if serie not in self.all_srus[task.bug.id].series:
                self.all_srus[task.bug.id].series += [serie]
            if task.assignee is not None:
                if (task.assignee.display_name not in
                        self.all_srus[task.bug.id].owners):
                    self.all_srus[task.bug.id].owners += \
                        [task.assignee.display_name]
            else:
                self.all_srus[task.bug.id].owners += ['Unowned']

    def get_all_tasks(self):
        """
        Get the tasks for all valid series
        """
        for serie in self.valid_series:
            self.get_tasks_for_serie(serie)
        print()

    def display_report(self):
        """
        Format and display all the collected tasks
        """
        for bug in sorted(self.all_srus.keys()):
            print("LP: #%s - %s" % (bug, self.all_srus[bug].title))
            print("  - Series to SRU : %s" % ' '.
                  join(self.all_srus[bug].series))
            print("  - Owners : %s" % ' '.join(self.all_srus[bug].owners))
            print()


def main():
    sru = Sru()
    sru.login()
    sru.get_all_tasks()
    sru.display_report()

if __name__ == "__main__":
    main()
