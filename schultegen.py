#!/usr/bin/env python3
#
# Copyright 2021 Nikita Zlobin <nick87720z@gmail.com>
#
#    Schultegen is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from random   import shuffle
from sys      import argv, stderr, stdout
from getopt   import getopt 
from os.path  import realpath, basename
from markdown import markdown
from io       import open

size = int(5)
v_min = int(1)
f_out = None # String

# Argument parsing

opts, trail = getopt (argv[1:], 'hs:m:', ['help', 'size=', 'min=', 'html='])
for opt, val in opts:
    if opt in ['--size', '-s']:
        size = int( val )
        if size < 3:
            print ('Minimum size 3 is required')
            exit ()
        if size % 2 == 0:
            print ('Size must be odd')
            exit ()
    elif opt in ['--min', '-m']:
        v_min = int( val )
    elif opt in ['--html']:
        f_out = val
    elif opt in ['--help', '-h']:
        print ('Usage:', basename(argv[0]), '[--size INT | -s INT] [--min INT | -m INT] [--html STR]')
        exit ()

if not f_out:
    f_out = 'schulte-output.html'
if f_out != '-':
    f_out = realpath (f_out)

print ('size:', size,  file=stderr)
print ('min: ', v_min, file=stderr)
print ('file:', 'standard output' if f_out == '-' else f_out, file=stderr)

v_max = size * size + v_min - 1

text = '''<style>
        :root {
            --corner-radius: calc(1vmin * 100 / (8 * ''' + str(size) + '''));
        }

        * {
                border-collapse: separate;
                border-spacing: 1px;
        }
        thead { display: none; }
        table {
                background: rgba(255, 255, 255, 20%);
                border-radius: calc(var(--corner-radius) + 1px);
                width: 100%;
                height: 100%;
        }
        td {
                background: hsla(30, 50%, 50%, 50%);
                font-size: ''' + str(100 / size * 3 / 8) + '''vw;
                width: ''' + str(100 / size) + '''%;
        }

        @media (prefers-color-scheme: dark) {
                * {
                        background: #121212;
                        color: rgb(255, 255, 205);
                }
                table {
                        background: rgba(0, 0, 0, 40%);
                }
        }

        tr:first-child >
        td:first-child {
                border-top-left-radius: var(--corner-radius);
        }
        tr:first-child >
        td:last-child {
                border-top-right-radius: var(--corner-radius);
        }
        tr:last-child >
        td:first-child {
                border-bottom-left-radius: var(--corner-radius);
        }
        tr:last-child >
        td:last-child {
                border-bottom-right-radius: var(--corner-radius);
        }
</style>\n'''

for n in range(0, size):
    text += '| <!-- --> '
text += '|\n'

for n in range(0, size):
    text += '| :---: '
text += '|\n'

nums = list(range(v_min, v_max + 1))
shuffle (nums)

col = int(0)
for n in nums:
    text += '| ' + str(n) + ' '
    col = (col + 1) % size
    if not col:
        text += '|\n'

f_stream = stdout if f_out == '-' else open (f_out, mode='wt')
print (markdown(text, extensions=['tables']), file=f_stream)
