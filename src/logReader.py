# Maracatronics Robotics
#  Federal University of Pernambuco (UFPE) at Recife
#  http://www.maracatronics.com/
#
#  This file is part of Armorial project.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import os


class Reader:
    def resolve_path(filepath):
        folder = filepath.split("/")[0]
        name = filepath.split("/")[1]
        return folder, name

    def read(filepath):
        lines = []
        folder, name = Reader.resolve_path(filepath)
        if name in os.listdir(folder):
            file = open(filepath)
            lines = file.readlines()

        print("File opened. {} lines had been read.".format(len(lines)))
        return lines

    def get_pid_log(filepath):
        print("Start processing: {}.".format(filepath))
        lines = Reader.read(filepath)
        pid_log = []
        constants = []
        for line in lines:
            if "PID Test" in line:
                pid_log.append(line)
            elif "Constants used" in line:
                constants.append(line)

        print("From {} lines, got {} of PID Test".format(len(lines), len(pid_log)))
        return [constants, pid_log]
