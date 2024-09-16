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
import os

from model import Piece


def import_score(filename):
    resource_path = os.path.join(os.path.dirname(__file__), filename)
    with open(resource_path) as file:
        file_contents = file.read()
        piece = Piece.parse(file_contents)
    return piece

#fileout = import_score(file_path)
    # TO-DO Now, the MEI structure has to be created and exported

