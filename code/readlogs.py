import csv
import matplotlib.pyplot as plt


with open('logs/runs2.csv') as f:
    reader = csv.reader(f)

    runsAvg = [0 for x in range(50)]
    countRuns = 0
    for row in f:
        run = [float(x) for x in row.split(",")]
        for i,v in enumerate(run):
        	runsAvg[i] += v
        countRuns += 1

    for i,v in enumerate(runsAvg):
    	runsAvg[i] /= countRuns
    

    for i,v in enumerate(runsAvg):
    	print(v,end=',')
    
