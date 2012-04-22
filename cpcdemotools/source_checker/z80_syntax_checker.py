#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: z80_syntax_checker.py
Author: Romain Giot
Description: Quick'n dirty z80 syntax file checker
'''


"""simple Z80 syntax checker.

Quick and dirty tool to find small errors in z80 files, and detect them before
assembling a big project.
Syntax checking is not supposed to be perfect and efficient.
But it can quickly detect some errors.
"""
# TODO add: ex de, hl ; push sp ; add a
# TODO remove duplciate alert when set is used
# TODO raise errors when instructions use hl and ix together

# imports
import sys, os
import re

# Regex for macros
RE_OPEN_MACRO = re.compile('^\s*(macro|MACRO)\s+(\S+)' )
RE_CLOSE_MACRO = re.compile('^\s*(endm(acro)?|ENDM(ACRO))\s+' )

# Classic registers
STR_16_REGISTERS = '(hl|bc|de|ix|iy)'
STR_8_REGISTERS  = '(h|l|b|c|d|e|ixl|ixh|a)'
RE_LOAD_REGISTER_SYNTAX = re.compile('\s*ld\s+(%s|%s)\s*,?\s*(;.*)?$' \
                                     % (STR_8_REGISTERS, STR_16_REGISTERS)
                                    , re.IGNORECASE)

# Regex for labels
RE_LABELS = re.compile('^([A-Z_.][A-Z_0-9]+)', re.IGNORECASE)

def _get_all_lines(source):
    """Load all the lines of the file."""
    f = open(source)
    lines = f.readlines()
    f.close()

    return lines


class Z80_Parser(object):
    """Parse a z80 source file.
    The source file is not supposed to be assembled alone.
    """


    def __init__(self, fname):
        """Parse the source file."""

        lines = _get_all_lines(fname)
        self._fname = fname

        self.check_macros(lines)
        self.check_load_syntax(lines)
        self.check_labels(lines)



    def emit_error(self, line, col, message):
        """Emit an error (does not use the column value)"""
        sys.stderr.write("%s:%d Error %s\n" % (self._fname, line, message))

    def emit_warning(self, line, col, message):
        """Emit an error (does not use the column value)"""
        sys.stderr.write("%s:%d Warning %s\n" % (self._fname, line, message))


    def check_load_syntax(self, lines):
        """Check the syntax for loading registers"""

        for i, line in enumerate(lines):
            load_line = i+1
            load_from_mem = re.match(RE_LOAD_REGISTER_SYNTAX, line)
            
            if load_from_mem:
                register = load_from_mem.group(1)
                self.emit_error(load_line, max(line.find('LD'), line.find('ld')), 'Register %s not loaded' % register)


    def check_labels(self, lines, min_width=8, max_width=30):
        """Check the validity of labels.
          -  Duplicates
          - Size
        """

        latest_parent = ''
        labels = []
        for i, line in enumerate(lines):
            label_line = i +1
            label_res = re.match(RE_LABELS, line)

            if label_res:
                # Get the label value (manage internal labels)
                label = label_res.group(1)
                if label.startswith('.'):
                    real_label = latest_parent + label
                else:
                    real_label = label
                    latest_parent = label

                # Check if label already exists
                if real_label in labels:
                    self.emit_error(label_line, 1, 'Label %s already exists' \
                               % real_label)
                else:
                    labels.append(real_label)

                # Check size validity
                if len(label) < min_width and label[0]!='.': #do not test for local ones
                    self.emit_warning(label_line, 1, 'Label %s too short' % label)
                elif len(label) > max_width:
                    self.emit_warning(label_line, 1, 'Label %s too long' % label)

    def check_macros(self, lines):
        """Verify syntax macro"""

        opened_macro = 0
        macro_line = -1
        macro_names = []


        for i, line in enumerate(lines):
            macro_line = i+ 1

            # macro opening detection
            open_re = re.match(RE_OPEN_MACRO, line)
            if open_re:
                macro_name = open_re.group(2)

                # check for included macros
                if opened_macro:
                    self.emit_error(macro_line, -1,
                               'Macro %s opened inside another one (%s)' \
                                  %(macro_name, macro_names[-1]))

                # check for duplicated macros
                if macro_name in macro_names:
                    self.emit_error(macro_line, -1,
                               'Macro %s already defined' % macro_name)

                opened_macro = opened_macro + 1
                macro_names.append(macro_name)

            close_re = re.match(RE_CLOSE_MACRO, line)
            if close_re:
                if not opened_macro:
                    self.emit_error(macro_line, -1, 'Macro not previously defined')
                else:
                    opened_macro = opened_macro - 1


        if opened_macro:
            self.emit_error(macro_line, -1, 'Macro %s never closed' % macro_names[-1])

# code
if __name__ == '__main__':
    # Check parameters
    if len(sys.argv) != 2:
        sys.stderr.write("Usage\n\t%s source_file\n" % sys.argv[0])
        quit(-1)

    source = sys.argv[1]
    if not os.path.exists(source):
        sys.stderr.write("%s does not exist\n" % source)
        quit(-1)

    
    Z80_Parser(source)


# metadata
__author__ = 'Krusty/Benediction'
__copyright__ = 'Copyright 2012, Benediction'
__credits__ = ['Krusty/Benediction']
__licence__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Krusty/Benediction'
__email__ = 'krusty@cpcscene.fr'
__status__ = 'Prototype'

