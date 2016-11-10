#!/usr/bin/python3
#
# BugTasks class : Get a list of LP bugs with a given tag
#
# Copyright (C) 2016 Louis bouchard <louis.bouchard@canonical.com>
#

from launchpadlib.launchpad import Launchpad as lp


class OneBugTask():
    """ One single BugTask """
    def __init__(self):
        self.title = ''
        self.owners = []
        self.series = []


class BugTasks():
    """ The BugTasks class
    The class logs into Launchpad and query the tasks
    to find the tagged tasks
    """
    def __init__(self):
        self.tag = None
        self.all_tasks = {}
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

        self.lp = lp.login_anonymously('sts_tags',
                                       'production', version='devel')

    def get_tasks_for_serie(self, tag, serie):
        """
        Get all tasks tagged with tag from one single
        serie. Put tasks in a list indexed by bug number
        """
        self.ubuntu = self.lp.distributions['ubuntu'].getSeries(
            name_or_version=serie)
        self.tasks = self.ubuntu.searchTasks(tags=tag,
                                             created_since='2016-01-01',
                                             order_by='id')
        for task in self.tasks:
            if task.bug.id not in self.all_tasks.keys():
                self.all_tasks[task.bug.id] = OneBugTask()
                self.all_tasks[task.bug.id].title = task.bug.title
                print("%s" % serie[0], end='', flush=True),
            if serie not in self.all_tasks[task.bug.id].series:
                self.all_tasks[task.bug.id].series += [serie]
            if task.assignee is not None:
                if (task.assignee.display_name not in
                        self.all_tasks[task.bug.id].owners):
                    self.all_tasks[task.bug.id].owners += \
                        [task.assignee.display_name]
            else:
                self.all_tasks[task.bug.id].owners += ['Unowned']

    def get_all_tasks(self, tag):
        """
        Get the tasks for all valid series
        """
        for serie in self.valid_series:
            self.get_tasks_for_serie(tag, serie)
        print()

    def display_report(self):
        """
        Format and display all the collected tasks
        """
        for bug in sorted(self.all_tasks.keys()):
            print("LP: #%s - %s" % (bug, self.all_tasks[bug].title))
            print("  - Series to SRU : %s" % ' '.
                  join(self.all_tasks[bug].series))
            print("  - Owners : %s" % ' '.join(self.all_tasks[bug].owners))
            print()
