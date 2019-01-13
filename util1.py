import os
import re
import subprocess
import numpy as np
import filecmp
import csv
import time

def createDirSH(path) :
    if os.path.exists(os.path.abspath(path)):
	    print("rm -rf {}".format(path))
    print("mkdir  {}".format(path))

def createDirPY(path) :
	if os.path.exists(os.path.abspath(path)):
		cmd1 = "rm -rf {}".format(path)
		subprocess.call(cmd1.split(), stderr = subprocess.STDOUT, timeout = 30)
	cmd2 = "mkdir {}".format(path)
	subprocess.call(cmd2.split(), stderr = subprocess.STDOUT)

def getIndex(str) :
    return re.findall('\d+', str)[0]

def exePY(mutant_output_file, origin_mpath, EXE_MUTANT_DIR, test_index, line, mutant, op) :
    
    mutant_output_file = origin_mpath + "/test_{}".format(test_index)
    
    if line.startswith("../inputs/") :
        exe_file = mutant.rstrip()
        cmd = "{} {}".format(EXE_MUTANT_DIR + op + "/" +  exe_file, line.strip())
               
        try:
            with open(mutant_output_file, 'wb') as out_stream:
                process = subprocess.call(cmd.split(), stdout = out_stream, stderr = subprocess.STDOUT, timeout = 5)
                if process == -11 :
                    subprocess.call("mv {} {}".format(mutant_output_file, origin_mpath+"/_segfault_{}".format(test_index)).split(), stderr = subprocess.STDOUT)
        except subprocess.TimeoutExpired:
            subprocess.call("mv {} {}".format(mutant_output_file, origin_mpath+"/_timeout_test_{}".format(test_index)).split(), stderr = subprocess.STDOUT)
            pass

def exe(target, suite, op, mutant) :
    
    #[same output, diff output, timeout, segfault, stacksmash, kill/alive(binary)]
    result =[0,0,0,0,0,0] # result per MUT
    
    suitefile = open("../testplans.alt/testplans.cov/" + suite, 'r')
    suite_result = open("../result/suiteResult.csv", 'a', newline = '')
    csv_writer = csv.writer(suite_result)

    CORRECT_OUTPUT_DIR = "../outputs.{}/".format(target) + suite
    MUSIC_OUTPUT_DIR = "../outputs.{}.music/".format(target) + suite
    
    r = [suite, op]

    for test_index, line in enumerate(suitefile.readlines()) :

        space_result_file = CORRECT_OUTPUT_DIR + "/test_{}".format(test_index)
        r.append("test_{}".format(test_index))
        mutant_result_file = "output_file2"
        # mutant_result_file = MUSIC_OUTPUT_DIR + "/test_{}".format(test_index)

        if line.startswith("../inputs"):
            
            exe_file = mutant.rstrip()
            cmd = "{} {}".format("../mutant.music.{}/exe/".format(target) + op + "/" + exe_file, line.strip())
            
            start_time = time.time()
            try:
                with open(mutant_result_file, 'wb') as out_stream:
                    process = subprocess.call(cmd.split(), stdout = out_stream, stderr = subprocess.STDOUT, timeout = 3)
                    if process == -11 :
                        result[3] += 1 
                        result[5] = 1
                        r.append(-11)
                    elif process == -6 :
                        r.append(-6)
                        result[4] += 1
                        result[5] = 1
                    else :
                        if not filecmp.cmp(mutant_result_file, space_result_file) : # diff output
                            result[1] += 1
                            r.append(1)
                        else :
                            result[0] += 1
                            r.append(0)
            except subprocess.TimeoutExpired:
                r.append(2)
                result[2] += 1
                result[5] =1
                pass
            exec_time = time.time()-start_time
            # if os.path.isfile(mutant_result_file):
            #     subprocess.call("rm {}".format(mutant_result_file).split(), stderr = subprocess.STDOUT)
    
    csv_writer.writerow(r)
    if(sum(result[1:5]) > 0) :
        result[5] = 1
    
    return result, exec_time

def writeResult(suite_result, suite, suite_time, result_writer) :

	# killnum_per_op = sum(list(n[0] for n in list(suite_result.values())))
	# totalnum_per_op = sum([n[1] for n in list(suite_result.values())])
    
	mutation_score = []
	
	for n in list(suite_result.values()): # for each operator(kill, total, mutationscore)
        
        ms = [n[0],n[1]]
		killnum_per_op += n[0]
        totalnum_per_op += n[1]

        try:
			ms.append(n[0]/n[1])
            
		except ZeroDivisionError:
			ms.append(0)

        mutation_score.append(ms)

	result = [suite , suite_time, killnum_per_op, totalnum_per_op]
	for s in mutation_score:
		result.append(s)
	
	cw = csv.writer(result_writer)
	# if i == 0:
	# 	cw.writerow(suite_result.keys())
	cw.writerow(result)
    # print("killed mutants by {} : {} / {} ".format(suite, killnum_per_op, totalnum_per_op))

