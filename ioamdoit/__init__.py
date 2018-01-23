from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


import glob
import platform
import os
import sys
import zipfile
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

from doit import get_var

miniconda_url = {
    "Windows": "https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe",
    "Linux": "https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh",
    "Darwin": "https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
}


# Download & install miniconda...Requires python already, so it might
# seem odd to have this. But many systems (including generic
# (non-python) travis and appveyor images) now include at least some
# system python, in which case this command can be used. But generally
# people will have installed python themselves, so the download and
# install miniconda tasks can be ignored.

def task_download_miniconda():
    url = miniconda_url[platform.system()]
    miniconda_installer = url.split('/')[-1]

    def download_miniconda(targets):
        urlretrieve(url,miniconda_installer)

    return {'targets': [miniconda_installer],
            'uptodate': [True], # (as has no deps)
            'actions': [download_miniconda]}


def task_install_miniconda():
    location = {
        'name':'location',
        'long':'location',
        'short':'l',
        'type':str,
        'default':os.path.abspath(os.path.expanduser('~/miniconda'))}

    miniconda_installer = miniconda_url[platform.system()].split('/')[-1]
    return {
        'file_dep': [miniconda_installer],
        'uptodate': [False], # will always run (could instead set target to file at installation location?)
        'params': [location],
        'actions': [
            'START /WAIT %s'%miniconda_installer + " /S /AddToPath=0 /D=%(location)s"] if platform.system() == "Windows" else ["bash %s"%miniconda_installer + " -b -p %(location)s"]
        }


def task_update_conda_and_conda_build():
    return {'actions':['conda install -y "conda-build>=3.2" "conda>=4.4"']}


def task_create_env():

    def _create_env(env_name,path_to_recipe):
        if path_to_recipe is None:
            raise ValueError("Must supply path to conda recipe")
        
        from conda_build import api
        from conda_build.environ import create_env
        from conda.cli.main_info import get_info_dict

        metadata = api.render(path_to_recipe)[0][0]
        deps = metadata.get_value('requirements/run') + metadata.get_value('test/requires') #and maybe look at what people have tried to put in extra etc

        create_env(get_info_dict()['envs_dirs'][0]+"/"+env_name, deps, env='run', config=metadata.config, subdir=metadata.config.subdir)

    env_name = get_var('env_name','test-environment')
    path_to_recipe = get_var('conda_recipe',None)

    return {'actions': [(_create_env,(env_name,path_to_recipe))],
            'task_dep': ['update_conda_and_conda_build']}


def task_capture_conda_env():
    return {'actions':["conda info","conda list","conda env export"]}

def task_develop_install():
    return {'actions':["pip install -e ."]}
