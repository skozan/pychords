#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vi:expandtab:tabstop=4 shiftwidth=4 textwidth=79
# Copyright (c) 2017 Stefanos Kozanis <S.Kozanis@gmail.com>

"""
A Python library that perform chord recognition from notes. Test script
"""

import sys

from pychords import get_winner_inversion, get_base_generation, check_notes

if __name__=='__main__':
    if len(sys.argv)<2:
        sys.stderr.write('Specify at least one note\n')
        sys.exit(1)
    check_notes(sys.argv[1:])
    winner = get_winner_inversion(sys.argv[1:])
    print '{}: {}'.format(
        winner,
        get_base_generation(winner))
