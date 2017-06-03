#!/usr/bin/python
# Copyright (c) 2017 Stefanos Kozanis <S.Kozanis@gmail.com>

import copy
import sys

"""
A Python library that perform chord recognition from notes
"""

NOTES = {
    'c': 0, 'b#': 0, 'c#': 1, 'db': 1, 'd': 2, 'd#':3,
    'eb': 3, 'e': 4, 'fb': 4, 'e#': 5, 'f': 5,
    'f#': 6, 'gb': 6, 'g': 7, 'g#': 8, 'ab': 8,
    'a': 9, 'a#': 10, 'bb': 10, 'b': 11, 'cb': 11}

INTERVALS = {
    0: [{'base': 'octave', 'subspecies': None}],
    1: [{'base': 'ninth', 'subspecies': 'flat'}],
    2: [{'base': 'ninth', 'subspecies': None}],
    3: [{'base': 'third', 'subspecies': 'minor'},
        {'base': 'ninth', 'subspecies': 'sharp'}],
    4: [{'base': 'third', 'subspecies': 'major'},], 
    5: [{'base': 'eleventh', 'subspecies': None}],
    6: [{'base': 'fifth', 'subspecies': 'diminished'}, 
        {'base': 'eleventh', 'subspecies': 'sharp'},],
    7: [{'base': 'fifth', 'subspecies': None}],
    8: [{'base': 'fifth', 'subspecies': 'augmented'},
        {'base': 'thirteenth', 'subspecies': 'flat'}],
    9: [{'base': 'thirteenth', 'subspecies': None}],
    10: [{'base': 'seventh', 'subspecies': 'minor'}],
    11: [{'base': 'seventh', 'subspecies': 'major'}],
}

IMPORTANT_INTERVALS = [
    INTERVALS[3][0],   # minor third
    INTERVALS[4][0],   # major third
    INTERVALS[6][0],   # diminished fifth
    INTERVALS[7][0],   # perfect fifth
    INTERVALS[10][0],  # minor seventh
    INTERVALS[11][0]]  # major seventh


def get_interval(note1, note2):
    interval = NOTES[note2.lower()] - NOTES[note1.lower()]
    if interval<0:
        interval += 12
    return interval

def get_intervals(notes):
    intervals = []
    for note in notes[1:]:
        intervals.append(get_interval(notes[0], note))
    return intervals

def get_base_intervals_verbal(notes):
    intervals = get_intervals(notes)
    intervals_verbal = []
    for interval in intervals:
        intervals_verbal.append(INTERVALS[interval][0])
    return intervals_verbal

def check_notes(notes):
    for note in notes:
        if note.lower() not in NOTES:
            sys.stderr.write('Note {} is note a valid note\n'.format(
                    note))
            sys.exit(1)

def get_inversions(notes):
    inversion = copy.copy(notes)
    count = 0
    while True:
        yield inversion
        if count==min(3, len(notes)-1):
            break
        inversion = copy.copy(inversion)
        inversion.append(inversion.pop(0))
        count += 1

def get_inversion_score(intervals):
    score = 0
    found = set([])
    for interval in intervals:
        if (interval in IMPORTANT_INTERVALS) and \
                interval['base'] not in found:
            score += 1
            found.add(interval['base'])
    return score

def get_winner_inversion(notes):
    inversions = []
    for idx, inversion in enumerate(get_inversions(notes)):
        inversions.append((
            get_inversion_score(get_base_intervals_verbal(inversion)),
            idx,
            inversion))
    inversions = sorted(inversions, key=lambda x: -x[0]*10+idx)
    return inversions[0][2]

def get_base_generation(notes):
    s = ''
    base_intervals = get_base_intervals_verbal(notes)
    s = notes[0][0].upper()+(notes[0][1:] or '')
    is_major_minor = False
    has_dim_fifth = False
    for interval in base_intervals:
        if interval['base'] == 'third':
            if interval ['subspecies'] == 'minor':
                s += '-'
            is_major_minor = True
        elif interval['base'] == 'eleventh' and not is_major_minor:
            s += 'sus4 '
        elif interval['base'] == 'fifth' and \
                interval['subspecies'] == 'diminished':
            has_dim_fifth = True
        elif interval['base'] == 'fifth' and \
                interval['subspecies'] == 'augmented':
            s += '+ '
        elif interval['base'] == 'seventh':
            if has_dim_fifth:
                s += 'b5 '
                has_dim_fifth = False
            if interval['subspecies'] == 'major':
                s +=  'Maj7 '
            else:
                s += '7 '
    if has_dim_fifth:
        s += 'dim '
    return s

