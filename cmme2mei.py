"""
Author: David Rizo
Original Java Code Author: David Rizo (drizo@dlsi.ua.es)
Python Conversion Date: 14/09/2024
Last Modified By: David Rizo
Version: 1.0.0

Changelog:
    Version 1.0.0 - Initial conversion from Java to Python.
    - Implemented XML parsing using ElementTree. Not all tested, just some basic tests.
    - MEI export missing

Contributors:
    - [Contributor 1 Name], [Date], Changes: [Description of changes]
    - [Contributor 2 Name], [Date], Changes: [Description of changes]
"""

from cmme_parser import PieceParser


def cmme2mei(file_path):
    parser = PieceParser()
    piece = parser.parse_piece(file_path)
    print(piece)
