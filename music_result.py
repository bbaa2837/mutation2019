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

# SPACE_DIR = (r"/home/seahkim/code/space/")
SPACE_DIR = "../"
SUITE_DIR = SPACE_DIR + "testplans.alt/testplans.cov/"

EXE_ORIGIN_MUTANT_DIR = SPACE_DIR + "mutant.music.origin/exe/"
EXE_PERF_MUTANT_DIR = SPACE_DIR + "mutant.music2.perf/exe/"

OUTPUT_ORIGIN_MUSIC_DIR = SPACE_DIR + "outputs.origin.music/"
OUTPUT_PERF_MUSIC_DIR = SPACE_DIR + "outputs.perf.music/"

reader = csv.reader(open("../testNum.csv", "r"), delimiter = ",")
suitelist = list(reader)[0]

operators = [op for op in listdir(EXE_ORIGIN_MUTANT_DIR) if isdir(join(EXE_ORIGIN_MUTANT_DIR,op))]

origin_result_writer = csv.writer(open("../result/TestResult_origin.csv", 'w', newline = ''))
perf_result_writer = csv.writer(open("../result/TestResult_perf.csv", 'w', newline = ''))


for i, suite_index in enumerate(suitelist[1:]) :

	suite = "suite" + suite_index
			
	for op in operators:

		op_time = [0,0]

		mutantlist = sorted([m for m in listdir(EXE_PERF_MUTANT_DIR + op) if isfile(join(EXE_PERF_MUTANT_DIR + op, m))])
		
		for mutantIndex, mutant in enumerate(mutantlist) :
			
			m_index = measure.getIndex(mutant)
			mutant_time = [0,0] #[origin, perf]
				
			print("origin {} {} {}".format(suite, op, m_index))
			
			o_test_result = measure.exe("origin", suite, op, "space.MUT{}".format(m_index))
			p_test_result = measure.exe("perf", suite, op, "perf.space.MUT{}".format(m_index))

			origin_result_writer.writerow([suite, op, m_index, o_test_result])
			perf_result_writer.writerow([suite, op, m_index, p_test_result])

			# if mutantIndex == 0 : break
		


