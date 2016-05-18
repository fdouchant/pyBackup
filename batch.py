#!/usr/bin/python

import sys

from myPyApps import myargparse
from pyBatch.pybatch import PyBatch

parser = myargparse.MyArgumentParser()
parser.add_argument("-s", "--section", required=True, help="Specify which configuation section should be run")
parser.add_argument("--dry-run", action="store_true", default=False, help="Does not run command neither send email")
args = parser.parse_args()

status = PyBatch(config_default='batch', options=args).run()
if status is None:
    sys.exit(0)
else:
    sys.exit(status)
