import sys
import subprocess
import os
from os import listdir
from os.path import isdir, isfile, join
import csv
import re

def getIndex(str) :
    return re.findall('\d+', str)[0]


if __name__ == '__main__': 

    SPACE_DIR = "../"

    reader = csv.reader(open("../testNum.csv", "r"))
    result_file = csv.writer(open("time.csv", "w", newline = ''))
    suitelist = list(reader)[0]

    # for i, suite_index in enumerate(suitelist[1:]) :

    #     suite = "suite" + suite_index
    #     o_suite_writer = open(suite+"_o.sh", "w")
    #     p_suite_writer = open(suite+"_p.sh", "w")



    try:
        cmd = "millisecond-time sh suite55_bin_o.sh"
        process = subprocess.Popen(cmd.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        out, err = process.communicate()
        print(out)
        # output = out.decode('ISO-8859-1').split('\n')
        # print(out.decode('ISO-8859-1'))
        # elapsed_time_ms = int(re.findall('\d+', output[-2])[-1])
        # print elapsed_time_ms

    except subprocess.TimeoutExpired:
        process.kill()
        pass


