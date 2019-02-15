import sys
import subprocess
import os
from os import listdir
from os.path import isdir, isfile, join
import csv
import re

def getIndex(str) :
    return re.findall('\d+', str)[0]

def make(target, suite, op, mutant, writer) :
    
    suitefile = open("../testplans.alt/testplans.cov/" + suite, 'r')
    
    exec_time = 0

    for test_index, line in enumerate(suitefile.readlines()) :

        if line.startswith("../inputs"):
            
            cmd = "timeout 3s "
            exe_file = mutant.rstrip()
            if(target == 'origin'):
                cmd += "{} {}\n".format("../mutant.music.{}/exe/".format(target) + op + "/" + exe_file, line.strip())
            elif(target == 'perf'):
                cmd += "{} {}\n".format("../mutant.music2.{}/exe/".format(target) + op + "/" + exe_file, line.strip())
            
            writer.write(cmd)   

if __name__ == '__main__': 

    SPACE_DIR = "../"

    EXE_ORIGIN_MUTANT_DIR = SPACE_DIR + "mutant.music.origin/exe/"
    EXE_PERF_MUTANT_DIR = SPACE_DIR + "mutant.music2.perf/exe/"

    reader = csv.reader(open("../testNum.csv", "r"))
    result_file = csv.writer(open("time.csv", "w", newline = ''))
    suitelist = list(reader)[0]

    operators = [op for op in listdir(EXE_ORIGIN_MUTANT_DIR) if isdir(join(EXE_ORIGIN_MUTANT_DIR,op))]

    for i, suite_index in enumerate(suitelist[1:]) :

        suite = "suite" + suite_index
        o_suite_writer = open(suite+"_o.sh", "w")
        p_suite_writer = open(suite+"_p.sh", "w")
        for op in operators:

            mutantlist = sorted([m for m in listdir(EXE_PERF_MUTANT_DIR + op) if isfile(join(EXE_PERF_MUTANT_DIR + op, m))])
            
            for mutantIndex, mutant in enumerate(mutantlist) :
                m_index = getIndex(mutant)

                # print("origin {} {} {}".format(suite, op, m_index))
                
                make("origin", suite, op, "space.MUT{}".format(m_index), o_suite_writer)
                make("perf", suite, op, "perf.space.MUT{}".format(m_index), p_suite_writer)

                # if mutantIndex == 0 : break
            
            # break
        # break
    
        # with open("timing.sh", 'w', newline = '') as f:
        #     f.write("millisecond-time sh {}_o.sh\n".format(suite))
        #     f.write("millisecond-time sh {}_p.sh\n".format(suite))


    # try:
    #     cmd = "millisecond-time sh suite55_o.sh"
    #     process = subprocess.Popen(cmd.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    #     out, err = process.communicate()
    #     print(out)
    #     # output = out.decode('ISO-8859-1').split('\n')
    #     # print(out.decode('ISO-8859-1'))
    #     # elapsed_time_ms = int(re.findall('\d+', output[-2])[-1])
    #     # print elapsed_time_ms

    # except subprocess.TimeoutExpired:
    #     process.kill()
    #     pass


