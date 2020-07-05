#!/usr/bin/env python3
import os
import sys
import re
import argparse
from distutils.dir_util import copy_tree


class DHandler():
    def __init__(self):
        self.cwd = os.getcwd()
        self.funcs = {
            'deploy_dir': self.deploy_dir,
            'deploy_empty_subdirs': self.deploy_empty_subdirs,
            # ... Add new directory handling functions here.
        }
        self.border_len = 60
        self.borders = {s: s * self.border_len for s in ['-', '=', '+', '*']}

    def read_argv(self):
        """Read in sys.argv."""
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
        """Display a message that a function will be run."""
        print(self.borders[border_symb])
        print(msg)
        print('From: [{}]'.format(dfrom))
        print('To:   [{}]'.format(dto))
        print(self.borders[border_symb])

    def yn_prompt(self,
                  msg='Continue? (y/n)> '):
        """Invoke a y/n prompt."""
        while True:
            yn = input(msg)
            if re.match(r'\b[yY]\b', yn):
                return True
            if re.match(r'\b[nN]\b', yn):
                return False

    def exam_exists(self, d, dflag='dfrom',
                    action='exit'):
        """Examine if a directory exists and take action if asked."""
        if not os.path.exists(d):
            if action == 'exit':
                print(f'{dflag} [{d}] not found. Terminating.')
                sys.exit()
            if action == 'makedirs':
                msg = f'{dflag} [{d}] not found. Create? (y/n)> '
                y = self.yn_prompt(msg=msg)
                if y:
                    os.makedirs(d)
                else:
                    return

    def lst_subdirs(self, dfrom,
                    ignore=['__pycache__']):
        """Return the list of subdir names in the dir of interest."""
        subdirs = []
        os.chdir(dfrom)
        for f in os.listdir(dfrom):
            if os.path.isdir(f) and f not in ignore:
                subdirs.append(f)
        os.chdir(self.cwd)
        return subdirs

    def deploy_dir(self,
                   dfrom=None, dto=None):
        """Deploy dfrom, including its contents, to dto."""
        self.disp_func_run('deploy_dir():'
                           + ' Deploying dfrom to dto...',
                           dfrom=dfrom, dto=dto)
        copy_tree(dfrom, dto)
        print('Deployment completed.')

    def deploy_empty_subdirs(self,
                             dfrom=None, dto=None):
        """Deploy subdirectories of dfrom, excluding their contents, to dto."""
        self.disp_func_run('deploy_empty_subdirs():'
                           + ' Deploying empty subdirectories...',
                           dfrom=dfrom, dto=dto)
        subdirs = self.lst_subdirs(dfrom)
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
    """dhandler - Directory handling assistant"""
    import dhandler
    dh = dhandler.DHandler()

    # I/O
    args = dh.read_argv()

    # Preprocessing
    dh.exam_exists(args.dfrom,
                   dflag='dfrom', action='exit')
    dh.exam_exists(args.dto,
                   dflag='dto', action='makedirs')
    dh.exam_exists(args.dto,
                   dflag='dto', action='exit')
    args.dfrom = os.path.abspath(args.dfrom)
    args.dto = os.path.abspath(args.dto)

    # Run the user-requested directory handling function.
    dh.funcs[args.func](dfrom=args.dfrom,
                        dto=args.dto)
    if not args.nopause:
        input('Press enter to exit...')
