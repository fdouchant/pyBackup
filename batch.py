#!/usr/bin/python

import sys

from myPyApps import myargparse
from pyBatch.pybatch import PyBatch

parser = myargparse.MyArgumentParser()
parser.add_argument("--dry-run", action="store_true", default=False, help="Does not run command neither send email")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-s", "--section", help="Specify which configuation section should be run")
group.add_argument("-l", "--list", action="store_true", help="List configuation sections")
args = parser.parse_args()

status = PyBatch(config_default='batch', options=args).run()
if status is None:
    sys.exit(0)
else:
    sys.exit(status)
