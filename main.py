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
import pandas as pd
import matplotlib.pyplot as plt
import argparse

from src.logReader import Reader

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="File path")
ds = {
    'P': [],
    'I': [],
    'D': [],
    'RampRate': [],
    'SetPointRange': [],
    'Timestamp': [],
    'PlayerSpd': [],
    'PlayerAcc': []
}

def add_to_ds(config):
    ds['P'].append(config['P'])
    ds['I'].append(config['I'])
    ds['D'].append(config['D'])
    ds['RampRate'].append(config['RampRate'])
    ds['SetPointRange'].append(config['SetPointRange'])
    ds['Timestamp'].append(config['Timestamp'])
    ds['PlayerSpd'].append(config['PlayerSpd'])
    ds['PlayerAcc'].append(config['PlayerAcc'])


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
    data_instant["playerX"] = words[7].translate({ord(w): None for w in '(,'})
    data_instant["playerY"] = words[8].translate({ord(w): None for w in ');'})
    data_instant["playerSpd"] = words[10]
    data_instant["playerAcc"] = words[12].replace('\n', '')
    return data_instant


def config_constants(const):
    const_list = {
        "P": "",
        "I": "",
        "D": "",
        "rampRate": "",
        "setPointRange": ""
    }
    words = const.split(" ")
    const_list["P"] = words[5].translate({ord(w): None for w in 'P:,'})
    const_list["I"] = words[6].translate({ord(w): None for w in 'I:,'})
    const_list["D"] = words[7].translate({ord(w): None for w in 'D:,'})
    const_list["rampRate"] = words[8].translate({ord(w): None for w in 'Ramp:,'})
    const_list["setPointRange"] = words[9].translate({ord(w): None for w in 'SetPoint:\n'})
    return const_list


def config_array(array):
    result = []
    for it in array:
        result.append(float(it))

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
    config = {
        'P': '',
        'I': '',
        'D': '',
        'RampRate': '',
        'SetPointRange': '',
        'Timestamp': [],
        'PlayerSpd': [],
        'PlayerAcc': []
    }

    #args = parser.parse_args()
    for P in range(50):
        for I in range(10):
            for D in range(10):
                for Ramp in [0, 1, 3]:
                    for SetPoint in [0, 5, 10]:
                        filename = "logs/suassuna_log_{0}_{1}_{2}_{3}_{4}.txt".format(P, I, D, Ramp, SetPoint)
                        [constants, pid_log] = Reader.get_pid_log(filename)
                        if len(constants) < 1:
                            continue

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

                        for const_line in constants:
                            constants = config_constants(const_line)

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

                        x = np.array(player_x)
                        spd = np.array(player_spd)
                        acc = np.array(player_acc)
                        tmp = np.array(instants_tempo)

                        config['P'] = constants["P"]
                        config['I'] = constants["I"]
                        config['D'] = constants["D"]
                        config['RampRate'] = constants["rampRate"]
                        config['SetPointRange'] = constants["setPointRange"]
                        config['Timestamp'] = instants_tempo
                        config['PlayerSpd'] = player_spd
                        config['PlayerAcc'] = player_acc

                        config['P'] = float(config['P'])
                        config['I'] = float(config['I'])
                        config['D'] = float(config['D'])
                        config['RampRate'] = float(config['RampRate'])
                        config['SetPointRange'] = float(config['SetPointRange'])
                        add_to_ds(config)

                        # print(x)
                        # print(spd)
                        filename = filename.split("/")[1]

                        fig, ax = plt.subplots()
                        print("Plotting graphs")
                        ax.plot(tmp, spd, linewidth=2.0,
                                label='Vx(t)\nP: {0}\nI: {1}\nD: {2}\n Ramp rate: {3}\n SetPointRange{4}'.format(
                                    constants["P"],
                                    constants["I"],
                                    constants["D"],
                                    constants["rampRate"],
                                    constants["setPointRange"]
                                ))

                        ax.set(xlim=(0, 11), xticks=np.arange(0, 11),
                               ylim=(0, 2), yticks=np.arange(0, 2))

                        plt.legend()
                        plt.savefig('graphs/Vx/' + filename.split(".")[0] + '_Vx', bbox_inches='tight')

                        ax.plot(tmp, acc, linewidth=2.0,
                                label='Ax(t)\nP: {0}\nI: {1}\nD: {2}\n Ramp rate: {3}\n SetPointRange{4}'.format(
                                    constants["P"],
                                    constants["I"],
                                    constants["D"],
                                    constants["rampRate"],
                                    constants["setPointRange"]
                                ))

                        ax.set(xlim=(0, 11), xticks=np.arange(0, 11),
                               ylim=(-6, 6), yticks=np.arange(-6, 6))

                        plt.legend()
                        plt.savefig('graphs/' + filename.split(".")[0], bbox_inches='tight')

    df = pd.DataFrame(ds)
    df.to_csv('dataset/grSim_data.csv')
    #plt.show()
