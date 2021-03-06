"""
Run the `pihsm` unit tests.
"""

import sys
import os
from os import path
import stat
from unittest import TestLoader, TextTestRunner
from doctest import DocTestSuite

import pihsm


packagedir = path.dirname(path.abspath(pihsm.__file__))


def pynames_iter(pkdir=packagedir, pkname=None):
    """
    Recursively yield dotted names for *.py files in directory *pydir*.
    """
    if not path.isfile(path.join(pkdir, '__init__.py')):
        return
    if pkname is None:
        pkname = path.basename(pkdir)
    yield pkname
    dirs = []
    for name in sorted(os.listdir(pkdir)):
        if name in ('__init__.py', '__pycache__'):
            continue
        if name.startswith('.') or name.endswith('~'):
            continue
        fullname = path.join(pkdir, name)
        st = os.lstat(fullname)
        if stat.S_ISREG(st.st_mode) and name.endswith('.py'):
            parts = name.split('.')
            if len(parts) == 2:
                yield '.'.join([pkname, parts[0]])
        elif stat.S_ISDIR(st.st_mode):
            dirs.append((fullname, name))
    for (fullname, name) in dirs:
        subpkg = '.'.join([pkname, name])
        for n in pynames_iter(fullname, subpkg):
            yield n


def run_tests():
    pynames = tuple(pynames_iter())

    # Add unit-tests:
    loader = TestLoader()
    suite = loader.loadTestsFromNames(pynames)

    # Add doc-tests:
    for name in pynames:
        suite.addTest(DocTestSuite(name))

    # Run the tests:
    runner = TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print(
        'pihsm: {!r}'.format(path.abspath(pihsm.__file__)),
        file=sys.stderr
    )
    print('-' * 70, file=sys.stderr)
    return result.wasSuccessful()


if __name__ == '__main__':
    if not run_tests():
        raise SystemExit(2)

