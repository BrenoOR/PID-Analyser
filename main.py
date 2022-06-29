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

# This code is a Python Script for read Armorial-Suassuna PID logs in order
# to make data analysis, and generate data visualization, as well as, in the
# future, recommend new constants for PID improvement.

import numpy as np
import matplotlib.pyplot as plt
import argparse

from src.logReader import Reader

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="File path")


def config_data(data_log):
    data_instant = {
        "timestamp": "",
        "playerX": "",
        "playerY": "",
        "playerSpd": "",
        "playerAcc": ""
    }

    words = data_log.split(" ")
    data_instant["timestamp"] = words[1].replace(']', '')
    data_instant["playerX"] = words[7].translate({ord(i): None for i in '(,'})
    data_instant["playerY"] = words[8].translate({ord(i): None for i in ');'})
    data_instant["playerSpd"] = words[10]
    data_instant["playerAcc"] = words[12].replace('\n', '')
    return data_instant


def config_array(array):
    result = []
    for i in array:
        result.append(float(i))

    return result


def get_base_time(tempo):
    print("Getting start time")
    hora = float(tempo[0][0])
    minuto = float(tempo[0][1])
    segundo = float(tempo[0][2])
    return [hora, minuto, segundo]


def setup_timestamp(tempo):
    result = []
    tempo_base = get_base_time(tempo)
    print("Setting up timestamp to better measures")
    for tem in tempo:
        tempo_actual = ((float(tem[0]) - tempo_base[0]) * 3600)\
                      + ((float(tem[1]) - tempo_base[1]) * 60)\
                      + (float(tem[2]) - tempo_base[2])
        result.append(tempo_actual)

    return result


if __name__ == '__main__':
    args = parser.parse_args()

    filename = args.file
    [constants, pid_log] = Reader.get_pid_log(filename)
    data = []
    player_x = []
    player_spd = []
    player_acc = []
    timestamp = []
    times = []
    print("Organizing data")
    print("Removing spaces and organizing data in sections")
    for log in pid_log:
        data.append(config_data(log))

    for d in data:
        player_x.append(d.get("playerX"))
        player_spd.append(d.get("playerSpd"))
        player_acc.append(d.get("playerAcc"))
        timestamp.append(d.get("timestamp"))

    for t in timestamp:
        times.append(t.split(":"))

    print("Transforming data to numbers")
    player_x = config_array(player_x)
    player_spd = config_array(player_spd)
    player_acc = config_array(player_acc)
    instants_tempo = setup_timestamp(times)

    min_spd = 1000
    max_spd = -1
    for s in player_spd:
        if s <= min_spd:
            min_spd = s
        if s >= max_spd:
            max_spd = s

    min_acc = 1000
    max_acc = -1
    for a in player_acc:
        if a <= min_acc:
            min_acc = a
        if a >= max_acc:
            max_acc = a

    x = np.array(player_x)
    spd = np.array(player_spd)
    acc = np.array(player_acc)
    tmp = np.array(instants_tempo)
    #print(x)
    #print(spd)
    filename = filename.split("/")[1]

    fig, ax = plt.subplots()
    print("Plotting graphs")
    ax.plot(tmp, spd, linewidth=2.0, label='Vx(t)\nP: {0}\nI: {1}\nD: {2}'.format(constants[0],
                                                                                  constants[1],
                                                                                  constants[2]))

    ax.set(xlim=(0, 11), xticks=np.arange(0, 11),
           ylim=(0, 2), yticks=np.arange(0, 2))

    plt.legend()
    plt.savefig('results/' + filename.split(".")[0] + '_Vx', bbox_inches='tight')

    ax.plot(tmp, acc, linewidth=2.0, label='Ax(t)\nP: {0}\nI: {1}\nD: {2}'.format(constants[0],
                                                                                  constants[1],
                                                                                  constants[2]))

    ax.set(xlim=(0, 11), xticks=np.arange(0, 11),
           ylim=(-6, 6), yticks=np.arange(-6, 6))

    plt.legend()
    plt.savefig('results/' + filename.split(".")[0], bbox_inches='tight')
    plt.show()
