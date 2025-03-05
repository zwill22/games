#!/usr/bin/env python3
# by Zack M. Williams
import os

# # GPLv3
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PIL import Image
import os


def image_size(image_file: str) -> tuple:
    return Image.open(image_file).size


def main():
    path = 'images'

    for pic in os.listdir(path):

        size = image_size(os.path.join(path, pic))

        print(pic, ":", size)


if __name__ == '__main__':
    main()
