#-------------------------------------------------------------------------------
#   This file is part of University of Python
#   Foobar is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Foobar is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Name:        util.py
# Purpose:
#
# Author:      MuychivTaing
#
# Created:     19/02/2012
# Copyright:   (c) MuychivTaing 2012
# Licence:     GPL v3
#-------------------------------------------------------------------------------

#!/usr/bin/env python

def decode_base64(in_str):
    """
    Decodes a base64 string and returns it.

    :Parameters:
        in_str : string
            base64 encoded string

    :returns: decoded string
    """
    import base64
    return base64.decodestring(in_str.encode('latin-1'))

def decompress_zlib(in_str):
    """
    Uncompresses a zlib string and returns it.

    :Parameters:
        in_str : string
            zlib compressed string

    :returns: uncompressed string
    """
    import zlib
    content = zlib.decompress(in_str)
    return content

#==================================================================================
def special_round(value):
    """
    For negative numbers it returns the value floored,
    for positive numbers it returns the value ceiled.
    """
    # same as:  math.copysign(math.ceil(abs(x)), x)
    # OR:
    # ## versus this, which could save many function calls
    # import math
    # ceil_or_floor = { True : math.ceil, False : math.floor, }
    # # usage
    # x = floor_or_ceil[val<0.0](val)

    if value < 0:
        return math.floor(value)
    return math.ceil(value)

#==================================================================================

def main():
    pass

if __name__ == '__main__':
    main()
