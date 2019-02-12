import csv

if __name__ == "__main__":
    
    origin_result = list(csv.reader(open("../result/TestResult_origin_55.csv", 'r'), delimiter = ","))
    perf_result = list(csv.reader(open("../result/TestResult_perf_55.csv", 'r'), delimiter = ","))

    result = [] # (kill-kill), (kill-alive), (alive-kill), (alive-alive)
    for i in range(len(origin_result)):

        mutant_result = [origin_result[i], perf_result[i]]
        mutant_check = [0,0]
        
        mutant_result[0][3] = mutant_result[0][3].strip('"[]').split(',')
        mutant_result[1][3] = mutant_result[1][3].strip('"[]').split(',')

        for t in mutant_result[0][3]:
            t = int(t)
            if t==-1 or t==-2 or t==-11 or t==-6 :
                mutant_check[0] = 1
                print(t)
                break
        for t in mutant_result[1][3]:
            t = int(t)
            if t==-1 or t==-2 or t==-11 or t==-6:
                mutant_check[1] = 1
                break

        print(mutant_check)

        if mutant_check[0] == mutant_check[1] :
            if mutant_check[0] == 1: # kill, kill

            else :
                
        else :
            if mutant_check[0] == 1:
        break


        
