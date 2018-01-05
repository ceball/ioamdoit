#! /usr/bin/env python

from setuptools import setup

import versioneer

setup(name = 'ioam-doit',
      description = 'common ioam doit tasks',
      version = versioneer.get_version(),
      cmdclass = versioneer.get_cmdclass(),
      license = 'MIT',
      url = 'http://github.com/ioam/ioam-doit',
      py_modules=['ioam_doit'],
      entry_points = {
          'doit.COMMAND': [
              'plug_sample = doit_sample_cmd:SampleCmd'
          ]
      },
      )
