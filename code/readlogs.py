import csv
import matplotlib.pyplot as plt


with open('logs/tdlruns.csv') as f:
    reader = csv.reader(f)

    numEpisodes = 60
    window = 10 # smoothing the graph- windowed average
    numEps_graph = 51

    runsAvg = [0 for x in range(numEpisodes)]
    countRuns = 0
    for row in reader:
        for i,v in enumerate(row):
        	runsAvg[i] += float(v)
        countRuns += 1
    print("TrueOnline- episodes:",len(runsAvg),", runs:",countRuns)
    for i,v in enumerate(runsAvg):
    	runsAvg[i] /= countRuns

    ra = []
    for z in range(0,numEps_graph,1):
    	ra.append(sum(runsAvg[z:z+window])/window)

    plt.plot(ra , color="blue")
    
    f2 = open('logs/approxruns.csv')

    reader = csv.reader(f2)
    runsAvg = [0 for x in range(numEpisodes)]
    countRuns = 0
    for row in reader:
        for i,v in enumerate(row):
            runsAvg[i] += float(v)
        countRuns += 1

    for i,v in enumerate(runsAvg):
        runsAvg[i] /= countRuns
    print("Approx- episodes:",len(runsAvg),", runs:",countRuns)
    ra = []
    for z in range(0,numEps_graph,1):
        ra.append(sum(runsAvg[z:z+window])/window)

    plt.plot(ra , color="red")
    plt.xlabel("Episode Number")
    plt.ylabel("Episode End Score")
    plt.show()
    
    # print("==========")
    # DQN openai gym takes a sliding window average of episode rewards
