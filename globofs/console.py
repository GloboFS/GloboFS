#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

import argparse
import gettext

t = gettext.translation('globofs', os.path.join(os.path.dirname(__file__), 'locale'), fallback=True)
_ = t.ugettext

def run():

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help=_('Commands'), dest='command')

    # A list command
    list_parser = subparsers.add_parser(
        name='list', help=_('List contents')
    )

    list_parser.add_argument(
        'dirname',
        action='store',
        help=_('Directory to list'))

    # A create command
    create_parser = subparsers.add_parser(
        name='create', help=_('Create a directory'))

    create_parser.add_argument(
        'dirname',
        action='store',
        help=_('New directory to create'))

    create_parser.add_argument(
        '--read-only', default=False, action='store_true',
        help=_('Set permissions to prevent writing to the directory')
    )

    # A delete command
    delete_parser = subparsers.add_parser(
        name='delete',
        help=_('Remove a directory'))
    delete_parser.add_argument(
        'dirname',
        action='store',
        help=_('The directory to remove'))
    delete_parser.add_argument(
        '--recursive', '-r', default=False, action='store_true',
        help=_('Remove the contents of the directory, too'),
    )

    print parser.parse_args()

if __name__ == "__main__":
    run()
