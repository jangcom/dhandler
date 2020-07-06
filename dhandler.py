#!/usr/bin/env python3
"""Directory handling assistant

Classes
-------
DHandler()
    A collection of methods that can facilitate directory handling
"""

__version__ = '1.0.0'
__author__ = 'Jaewoong Jang'

import os
import sys
import re
import argparse
from distutils.dir_util import copy_tree


class DHandler():
    """A collection of methods that can facilitate directory handling

    This class provides methods that can automate some mundane,
    repetitive directory handling tasks, such as copying a directory
    and its contents to another path.

    Attributes
    ----------
    cwd : str
        The working directory at the time of class instantiation
    border_len : int
        The number of symbols of a border line
    borders : dict
        Storage for border lines of different symbols
    funcs : dict
        Storage for the objects of directory handling methods

    Methods
    -------
    read_argv()
        Read in sys.argv using the argparse module.
    disp_func_run(msg, dfrom='', dto='', border_symb='-')
        Display a message that a function will be run.
    yn_prompt(msg='Continue? (y/n)> ')
        Invoke a y/n prompt.
    exam_exists(d, dflag='dfrom', action='exit', border_symb='*')
        Examine if the designated files exist.
    lst_subdirs(dfrom, ignore=None)
        Return the list of existing subdirectory names.
    deploy_dir(dfrom='', dto='')
        Deploy a directory, including its contents, to another path.
    deploy_empty_subdirs(dfrom='', dto='')
        Deploy empty subdirectories to another path.

    Notes
    -----
    When a directory handling method is newly defined, add the name and
    object of the method as a key-value pair to the funcs attribute;
    a user selects which directory handling method to use via the
    command line argument --func, which will then be used as a key of
    the funcs attribute.
    """

    def __init__(self):
        """Bind the objects of directory handling methods to a dict."""
        self.cwd = os.getcwd()
        self.border_len = 60
        self.borders = {s: s * self.border_len for s in ['-', '=', '+', '*']}
        self.funcs = {
            'deploy_dir': self.deploy_dir,
            'deploy_empty_subdirs': self.deploy_empty_subdirs,
            # ... Add new directory handling functions here.
        }

    def read_argv(self):
        """Read in sys.argv using the argparse module.

        Returns
        -------
        argparse.Namespace
            An object of argparse.Namespace
        """
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('--func',
                            default='deploy_dir',
                            choices=self.funcs.keys(),
                            help='directory handling function')
        parser.add_argument('--dfrom',
                            required=True,
                            help=('the directory from which'
                                  + ' information will be retrieved'))
        parser.add_argument('--dto',
                            required=True,
                            help=('the directory to which the retrieved'
                                  + ' information will be applied'))
        parser.add_argument('--nopause',
                            action='store_true',
                            help=('do not pause the shell'
                                  + ' at the end of the program'))
        return parser.parse_args()

    def disp_func_run(self, msg,
                      dfrom='', dto='', border_symb='-'):
        """Display a message that a function will be run.

        Arguments
        ---------
        msg : str
            The message to be displayed
        dfrom : str
            The original directory (default '')
        dto : str
            The target directory (default '')
        border_symb : str
            A key of the borders attribute (default '-')
        """
        print(self.borders[border_symb])
        print(msg)
        print('From: [{}]'.format(dfrom))
        print('To:   [{}]'.format(dto))
        print(self.borders[border_symb])

    def yn_prompt(self,
                  msg='Continue? (y/n)> '):
        """Invoke a y/n prompt.

        Arguments
        ---------
        msg : str
            The prompt message (default 'Continue? (y/n)> ')

        Returns
        -------
        bool
            True for y or Y, False for n or Y
        """
        while True:
            yn = input(msg)
            if re.match(r'\b[yY]\b', yn):
                return True
            if re.match(r'\b[nN]\b', yn):
                return False

    def exam_exists(self, d,
                    dflag='dfrom', action='exit', border_symb='*'):
        """Examine if the designated files exist.

        Arguments
        ---------
        d : str
            The directory to be examined whether exists
        dflag : str
            A flag differentiating between dfrom and dto
        action : str
            Actions for nonexisting files (default 'exit')
        border_symb : str
            A key of the borders attribute (default '*')

        Returns
        -------
        existing_files : list
            Files found to exist out of the designated files
        """
        if not os.path.exists(d):
            print(self.borders[border_symb])
            print(f'{dflag} [{d}] not found.', end='')
            if action == 'exit':
                print(' Terminating.')
                print(self.borders[border_symb])
                sys.exit()
            print('')  # For action != 'exit'
            print(self.borders[border_symb])
            if action == 'makedirs':
                y = self.yn_prompt(msg='Create? (y/n)> ')
                if y:
                    os.makedirs(d)
                else:
                    return

    def lst_subdirs(self, dfrom,
                    ignore=None):
        """Return the list of existing subdirectory names.

        Arguments
        ---------
        dfrom : str
            The original directory
        ignore : str or list
            Subdirectories to be ignored (default None)

        Returns
        -------
        subdirs : list
            The list of subdirectories found to exist
        """
        subdirs = []
        os.chdir(dfrom)
        for f in os.listdir(dfrom):
            if os.path.isdir(f) and f not in ignore:
                subdirs.append(f)
        os.chdir(self.cwd)
        return subdirs

    def deploy_dir(self,
                   dfrom='', dto=''):
        """Deploy a directory, including its contents, to another path.

        Arguments
        ---------
        dfrom : str
            The original directory (default '')
        dto : str
            The target directory (default '')
        """
        self.disp_func_run('deploy_dir():'
                           + ' Deploying dfrom to dto...',
                           dfrom=dfrom, dto=dto)
        copy_tree(dfrom, dto)
        print('Deployment completed.')

    def deploy_empty_subdirs(self,
                             dfrom='', dto=''):
        """Deploy empty subdirectories to another path.

        Arguments
        ---------
        dfrom : str
            The original directory (default '')
        dto : str
            The target directory (default '')
        """
        self.disp_func_run('deploy_empty_subdirs():'
                           + ' Deploying empty subdirectories...',
                           dfrom=dfrom, dto=dto)
        subdirs = self.lst_subdirs(dfrom, ignore=['__pycache__', '.git'])
        # In dfrom: Exit if dfrom has no subdirectory.
        if not subdirs:
            print('dfrom has no subdirectories. Terminating.')
            return
        # Deploy the subdirectories of dfrom to dto.
        os.chdir(dto)  # CWD --> dto
        for subdir in subdirs:
            if not os.path.isdir(subdir):
                os.mkdir(subdir)
                print('[{}] created.'.format(subdir))
        os.chdir(self.cwd)  # dto --> CWD


if __name__ == '__main__':
    dh = DHandler()

    # I/O
    argv = dh.read_argv()

    # Preprocessing
    dh.exam_exists(argv.dfrom,
                   dflag='dfrom', action='exit')
    dh.exam_exists(argv.dto,
                   dflag='dto', action='makedirs')
    dh.exam_exists(argv.dto,
                   dflag='dto', action='exit')
    argv.dfrom = os.path.abspath(argv.dfrom)
    argv.dto = os.path.abspath(argv.dto)

    # Run the user-requested directory handling method.
    dh.funcs[argv.func](dfrom=argv.dfrom,
                        dto=argv.dto)
    if not argv.nopause:
        input('Press enter to exit...')
