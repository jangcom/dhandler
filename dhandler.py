#!/usr/bin/env python3
import os
import sys
import re
import argparse


class DHandler():
    def __init__(self):
        self.cwd = os.getcwd()
        self.funcs = {
            'deploy_empty_dirs': self.deploy_empty_dirs,
            # ... Add new directory handling functions here.
        }
        self.border_len = 60
        self.borders = {s: s * self.border_len for s in ['-', '=', '+', '*']}

    def read_argv(self):
        """Read in sys.argv."""
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('--func',
                            default='deploy_empty_dirs',
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

    def exam_exists(self, d,
                    action='exit'):
        """Examine if a directory exists and take action if asked."""
        flags = {
            'exit': 'dfrom ',
            'mkdir': 'dto ',
        }
        flag = flags[action]
        if not os.path.exists(d):
            if action == 'exit':
                print(f'{flag}[{d}] not found. Terminating.')
                sys.exit()
            if action == 'mkdir':
                msg = f'{flag}[{d}] not found. Create? (y/n)> '
                y = self.yn_prompt(msg=msg)
                if y:
                    os.mkdir(d)
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

    def deploy_empty_dirs(self,
                          dfrom=None, dto=None):
        """Deploy empty directories from dfrom to dto."""
        # Gateways
        if not dfrom and not dto:
            return
        if not os.path.exists(dto):
            return
        # Proceed only if the first subdirectory of dfrom
        # does not exist in dto.
        subdirs = self.lst_subdirs(dfrom)
        os.chdir(dto)
        if not os.path.isdir(subdirs[0]):
            self.disp_func_run('deploy_empty_dirs():'
                               + ' Deploying empty subdirectories...',
                               dfrom=dfrom, dto=dto)
        else:
            return
        # Deploy the subdirectories of dfrom to dto.
        for subdir in subdirs:
            if not os.path.isdir(subdir):
                os.mkdir(subdir)
                print('[{}] created.'.format(subdir))
        os.chdir(self.cwd)


if __name__ == '__main__':
    """dhandler - Directory handling assistant"""
    import dhandler
    dh = dhandler.DHandler()

    # I/O
    args = dh.read_argv()

    # Preprocessing
    dh.exam_exists(args.dfrom, action='exit')
    dh.exam_exists(args.dto, action='mkdir')
    args.dfrom = os.path.abspath(args.dfrom)
    args.dto = os.path.abspath(args.dto)

    # Run the user-requested directory handling function.
    dh.funcs[args.func](dfrom=args.dfrom,
                        dto=args.dto)
