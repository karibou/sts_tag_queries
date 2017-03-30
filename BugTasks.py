#!/usr/bin/python3
#
# BugTasks class : Get a list of LP bugs with a given tag
#
# Copyright (C) 2016 Louis bouchard <louis.bouchard@canonical.com>
#

import distro_info
from launchpadlib.launchpad import Launchpad as lp


class BugTasks():
    """ The BugTasks class
    The class logs into Launchpad and query the tasks
    to find the tagged tasks
    """
    valid_series = distro_info.UbuntuDistroInfo().supported()
    start_date = '2015-01-01'

    def __init__(self):
        self.tag = None
        self.all_tasks = {}
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

    def add_one_task(self, one_task, serie):
        OneBug = self.all_tasks.setdefault(one_task.bug.id, {})
        OneBug['title'] = one_task.bug.title
        OneBug.setdefault('series', set()).add(serie)
        OneBug.setdefault('pkg', set()).add(
                          one_task.bug_target_name.split()[0])
        assignee = one_task.assignee.display_name if one_task.assignee else 'None'
        OneBug.setdefault('owners', set()).add(assignee)
        OneBug['verification'] = [vers for vers in one_task.bug.tags
                               if vers.startswith('verification')]

    def get_openstack_tasks(self, tag):
        """
        Get all openstack tasks tagged with tag
        Add each task found to the all_task list
        """
        print('Fetching openstack projects.\nThis will take some time...''',
              end="")
        self.openstack = self.lp.project_groups['openstack']
        self.oprojects = [(proj, proj.series)
                          for proj in self.openstack.projects]
        print('Got all %d openstack projects' % len(self.oprojects))
        print('Scanning through all project''series to find tagged bugs\n\
                This is a long process...', end='')
        for (project, series) in self.oprojects:
            for serie in series:
                tasks = serie.searchTasks(tags=tag)
                for task in tasks:
                    self.add_one_task(task, serie.name)
        print('\n')

    def get_ubuntu_tasks_for_serie(self, tag, serie):
        """
        Get all tasks tagged with tag from one single
        serie. Put tasks in a list indexed by bug number
        """
        self.ubuntu = self.lp.distributions['ubuntu'].getSeries(
            name_or_version=serie)
        self.tasks = self.ubuntu.searchTasks(tags=tag,
                                             created_since=self.start_date,
                                             order_by='id')
        for task in self.tasks:
            self.add_one_task(task, serie)
            print("%s" % serie[0], end='', flush=True)

    def get_all_tasks(self, tag):
        """
        Get the tasks for all valid series
        """
        for serie in self.valid_series:
            self.get_ubuntu_tasks_for_serie(tag, serie)
        print()

    def display_report(self, long_display, tag):
        """
        Format and display all the collected tasks
        """

        PkgList = {}
        for bug in sorted(self.all_tasks.keys()):
            PkgList.setdefault('pkg', set()).add(
                               ' '.join(self.all_tasks[bug]['pkg']))
            print("LP: #%s - (%s) %s" % (bug,
                                         ' '.join(self.all_tasks[bug]['pkg']),
                                         self.all_tasks[bug]['title']))
            if long_display:
                print("  - Series to SRU : %s" % ' '.
                      join(self.all_tasks[bug]['series']))
                if self.all_tasks[bug]['verification']:
                    print("  - Verification : %s" % ' '.join(
                           self.all_tasks[bug]['verification']))
                print("  - Owners : %s" % ' '.join(
                       self.all_tasks[bug]['owners']) + '\n')
                if tag == 'sts-sru-needed':
                    print("#info SRU are pending for : %s" % ', '.join(PkgList['pkg']))
