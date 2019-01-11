import sys
import subprocess
import os
from os import listdir
from os.path import isdir, isfile, join
import util1
import csv
import time
import filecmp
import difflib

# SPACE_DIR = (r"/home/seahkim/code/space/")
SPACE_DIR = "../"
SUITE_DIR = SPACE_DIR + "testplans.alt/testplans.cov/"

EXE_ORIGIN_MUTANT_DIR = SPACE_DIR + "mutant.music.origin/exe/"
EXE_PERF_MUTANT_DIR = SPACE_DIR + "mutant.music.perf/exe/"

OUTPUT_ORIGIN_MUSIC_DIR = SPACE_DIR + "outputs.origin.music/"
OUTPUT_PERF_MUSIC_DIR = SPACE_DIR + "outputs.perf.music/"


reader = csv.reader(open("../testNum.csv", "r"), delimiter = ",")
suitelist = list(reader)[0]


# suitelist = [f for f in listdir(SUITE_DIR) if isfile(join(SUITE_DIR, f))]

operators = [op for op in listdir(EXE_ORIGIN_MUTANT_DIR) if isdir(join(EXE_ORIGIN_MUTANT_DIR,op))]

origin = open('space.c','r', encoding="ISO-8859-1").read()
perf = open('space.perf.c', 'r', encoding="ISO-8859-1").read()

difference = difflib.unified_diff(origin.splitlines(True), perf.splitlines(True), lineterm = '\n')
difference = ".".join(difference)

origin_result_writer = open("../mutationScore_origin3.csv", 'w', newline = '')
perf_result_writer = open("../mutationScore_perf3.csv", 'w', newline = '')

#util.createDirPY(OUTPUT_ORIGIN_MUSIC_DIR)
#util.createDirPY(OUTPUT_PERF_MUSIC_DIR)

test = 0
exeTime = []
totalResult = []
diff_op = set()

for i, suite_index in enumerate(suitelist) :

	suite = "suite" + suite_index

#####origin#####
	
	suite_result = {}
	suite_time = 0
	start_time = time.time()

	OUTPUT_ORIGIN_SUITE_DIR = OUTPUT_ORIGIN_MUSIC_DIR + suite
	OUTPUT_PERF_SUITE_DIR = OUTPUT_PERF_MUSIC_DIR + suite
	
	# util.createDirPY(OUTPUT_ORIGIN_SUITE_DIR)
	# util.createDirPY(OUTPUT_PERF_SUITE_DIR)
			
	for op in operators:
		
		print("origin {} {}".format(suite, op))
		# util.createDirPY(OUTPUT_ORIGIN_SUITE_DIR + "/" + op)
		# util.createDirPY(OUTPUT_PERF_SUITE_DIR + "/" + op)
		# print(op)
		op_result = []
		op_time = 0

		origin_mutantlist = sorted([m for m in listdir(EXE_ORIGIN_MUTANT_DIR + op) if isfile(join(EXE_ORIGIN_MUTANT_DIR + op, m))])

		for mutantIndex, mutant in enumerate(origin_mutantlist) :
			
			o = open('../mutant.music.origin/source/{}/space.MUT{}.c'.format(op, util1.getIndex(mutant) ), 'r', encoding="ISO-8859-1").read()
			try:
				p = open('../mutant.music.perf/source/{}/space.perf.MUT{}.c'.format(op, util1.getIndex(mutant) ), 'r', encoding="ISO-8859-1").read()
			except FileNotFoundError:
				continue

			d = difflib.unified_diff(o.splitlines(True), p.splitlines(True), lineterm = '\n')
			d = ".".join(d)

			if (difference != d) : 
				print("diff : MUT{} by {}".format(util1.getIndex(mutant), op))
				diff_op.add(op)
				continue

			origin_mpath = OUTPUT_ORIGIN_SUITE_DIR + "/" + op + "/MUT" + util1.getIndex(mutant)
			# perf_mpath = OUTPUT_PERF_SUITE_DIR + "/" + op + "/MUT" + util.getIndex(mutant)

			# util.createDirPY(origin_mpath)
			# # util.createDirPY(perf_mpath)
			
			mutant_time = time.time()
			mutant_result = util1.exe("origin", suite, op, mutant)
			op_time += time.time() - mutant_time
			#print(op_time)
			op_result.append(mutant_result)
			
			if mutantIndex == 19 : 
				break

		suite_time += op_time
		#print(suite_time)	
		_sum = 0
		for mutant_result in op_result:
			_sum += mutant_result[5]
		tem = [_sum, len(op_result)]
		suite_result.update({op : tem})
	
	execute_time = time.time() - start_time	
	
	util1.writeResult(suite_result, suite, suite_time, origin_result_writer)

	print("---%s seconds ---" %(execute_time))

	totalResult.append(suite_result)
#####perf#####

	suite_result = {}
	suite_time = 0
	start_time = 0

	for op in operators:
		
		print(" perf {} {}".format(suite, op))

		op_result = []
		op_time = 0

		perf_mutantlist = sorted([m for m in listdir(EXE_PERF_MUTANT_DIR + op) if isfile(join(EXE_PERF_MUTANT_DIR + op, m))])

		for mutantIndex, mutant in enumerate(perf_mutantlist) :
			
			p = open('../mutant.music.perf/source/{}/space.perf.MUT{}.c'.format(op, util1.getIndex(mutant) ), 'r', encoding="ISO-8859-1").read()
			try:
				o = open('../mutant.music.origin/source/{}/space.MUT{}.c'.format(op, util1.getIndex(mutant) ), 'r', encoding="ISO-8859-1").read()
			except FileNotFoundError:
				continue

			d = difflib.unified_diff(o.splitlines(True), p.splitlines(True), lineterm = '\n')
			d = ".".join(d)

			if (difference != d) : 
				print("diff : MUT{} by {}".format(util1.getIndex(mutant), op))
				diff_op.add(op)
				continue	

			# origin_mpath = OUTPUT_ORIGIN_SUITE_DIR + "/" + op + "/MUT" + util.getIndex(mutant)
			perf_mpath = OUTPUT_PERF_SUITE_DIR + "/" + op + "/MUT" + util1.getIndex(mutant)

			# util.createDirPY(origin_mpath)
			# util.createDirPY(perf_mpath)

			mutant_time = time.time()
			mutant_result = util1.exe("perf", suite, op, mutant)
			op_time += time.time() - mutant_time
			op_result.append(mutant_result)

			if mutantIndex == 19 : 
				break
		
		suite_time += op_time

		_sum = 0
		for mutant_result in op_result:
			_sum += mutant_result[5]
		tem = [_sum, len(op_result)]
		suite_result.update({op : tem})	

	execute_time = time.time() - start_time	
		
	util1.writeResult(suite_result, suite, suite_time, perf_result_writer)

	print("---%s seconds ---" %(execute_time))
	print("different operator : {}".format(len(diff_op)))
	
	totalResult.append(suite_result)

print(totalResult)


	
