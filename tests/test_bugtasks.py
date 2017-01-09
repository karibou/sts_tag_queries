import unittest
import sys
import tempfile
import os
import shutil
from mock import patch, mock
import launchpadlib
from BugTasks import BugTasks

liblaunchpad = mock.MagicMock()
sys.modules['liblaunchpad'] = liblaunchpad
sys.modules['liblaunchpad.launchpad'] = liblaunchpad.launchpad
sys.modules['liblaunchpad.launchpad.Launchpad'] = liblaunchpad.launchpad.Launchpad

class BugtasksTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.workdir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.workdir)

    def patch(self, obj, attr, return_value=None):
        mocked = mock.patch.object(obj, attr)
        started = mocked.start()
        started.return_value = return_value
        setattr(self, attr, started)
        self.addCleanup(mocked.stop)

    def test_get_task_for_serie(self):
