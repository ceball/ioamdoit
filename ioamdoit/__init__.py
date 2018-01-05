from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from doit.cmd_base import TaskLoader

from . import tasks

class IOAMLoader(TaskLoader):
    cmd_options = ()

    def load_tasks(self, cmd, params, args):
        return self._load_from(cmd, tasks, self.cmd_names)
