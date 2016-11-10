#!/usr/bin/python3
#
# sts-sru : Get a list of LP bugs with sts-sru tag
#
# Copyright (C) 2016 Louis bouchard <louis.bouchard@canonical.com>
#

from launchpadlib.launchpad import Launchpad as lp

valid_series = ['precise', 'trusty', 'xenial', 'yakkety']

class one_sru():
    def __init__(self):
        self.title = ''
        self.owners = []
        self.series = []

class Sru():
    def __init__(self):
        self.all_srus = {}

    def login(self):
        self.launchpad = lp.login_anonymously('sts_sru', 'production', version='devel')

    def get_tasks_for_serie(self, serie):
        self.ubuntu = self.launchpad.distributions['ubuntu'].getSeries(name_or_version=serie)
        self.tasks = self.ubuntu.searchTasks(tags='sts-sru', created_since='2016-01-01',order_by='id')
        for task in self.tasks:
            if task.bug.id not in self.all_srus.keys():
                self.all_srus[task.bug.id] = one_sru()
                self.all_srus[task.bug.id].title = task.bug.title
                print("%s" % serie[0], end='',flush=True),
            if serie not in self.all_srus[task.bug.id].series:
                self.all_srus[task.bug.id].series += [serie]
            if task.assignee is not None:
                if task.assignee.display_name not in self.all_srus[task.bug.id].owners:
                    self.all_srus[task.bug.id].owners += [task.assignee.display_name]
            else:
                self.all_srus[task.bug.id].owners += ['Unowned']

    def get_all_tasks(self):
        for serie in valid_series:
            self.get_tasks_for_serie(serie)
        print()


def main():
    sru = Sru()
    sru.login()
    sru.get_all_tasks()

if __name__ == "__main__":
    main()
