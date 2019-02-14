import sys
import subprocess
import os
from os import listdir
from os.path import isdir, isfile, join
import csv
import time
import filecmp
import difflib
import measure

def getIndex(str):

  return re.findall('\d+', str)[0]

def make(target, suite, writer):

  suitefile = open("../testplans.alt/testplan.cov" + suite, 'r')

  for test_index, line in enumerate(suitefile.readlines()) :

    if line.startswith("../inputs") :

      cmd = "timeout 3s"
      
      if(target == 'origin') :
        cmd += "{} {}\n".format("../source/space", line.strip())
      elif(target == 'perf') :
        cmd += "{} {}\n".format("../source/space.perf", line.strip())

      writer.write(cmd)


if __name__ == "__main__" :

  reader = csv.reader(open("../testNum.csv", "r"))
  result_file = csv.writer(open("time.csv", "w", newline = ''))
  suitelist = list(reader)[0]

  for i, suite_index in enumerate(suitelist[1:2]) :

    suite = "suite" + suite_index
    o_suite_writer = open(suite+"_bin_o.sh", "w")
    p_suite_writer = open(suite+"_bin_p.sh", "w")

    make("origin", suite, o_suite_writer)
    make("perf", suite, p_suite_writer)
