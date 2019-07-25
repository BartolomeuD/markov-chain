# -*- coding: utf-8 -*-
import os
import numpy as np #For matrix multiplication
import networkx as nx  # For the chain building 

wd = 'C:\\PythonCode' #Your working directory with the data set file in it
os.chdir(wd) 
filename = 'worklist.csv' #file name
sep1 = ';' #separator in the file
start_state = 'start General course' #name of the start node
end_states = ['Finished course', 'Dropped General', 'fell asleep'] #list of end nodes
steps = 1000 # Number of steps in the random walk in the chain


fhand = open(filename, 'r')
i = 0
data01 = []
states = []

#just a sorting key to sort the array by first student_id and then event time
def sort_key (line):
    result = int(line[0]) * 1000000 + float(line[2])
    return(result)

for line in fhand:
    data01.append(line.rstrip().replace(',', '.').split(sep = sep1))
    states.append(line.rstrip().replace(',', '.').split(sep = sep1)[1])
fhand.close()

data01.sort(key = sort_key)
states = list(set(states))

calc_matrix = []
for i in range(len(states)):
    calc_matrix.append([])
    for j in range(len(states)):
        calc_matrix[i].append(0) 
    
for i in range (len(data01) - 1):
    if data01[i][0] == data01[i+1][0]: #if the student is the same
        calc_matrix[states.index(data01[i][1])][states.index(data01[i+1][1])] += 1

for i in range(len(calc_matrix)):
    if states[i] in end_states:
        for j in range(len(calc_matrix[i])):
            calc_matrix[i][j] = 0

TransitionMatrix = [] 
for i in range(len(calc_matrix)):
    TransitionMatrix.append([])
    for j in range(len(calc_matrix)):
        if sum(calc_matrix[i]) != 0:
            TransitionMatrix[i].append(float(calc_matrix[i][j]) / sum(calc_matrix[i]))
        else:
            TransitionMatrix[i].append(0)

#the graph
G = nx.MultiDiGraph()

for i in range(len(TransitionMatrix)):
    for j in range(len(TransitionMatrix)):
        if round(TransitionMatrix[i][j], 2) != 0:
            G.add_edge(states[i], states[j], weight=round(TransitionMatrix[i][j], 2), label="{:.02f}".format(TransitionMatrix[i][j]))
#nx.drawing.nx_pydot.write_dot(G, 'MarkovChain.dot') #dot file with the graph

#to make the end node probability calculation we have to make sure the matrix multiplication stays valid
#for that the nodes without out-connections are given the self-connecting edge
for i in range(len(TransitionMatrix)):
    if sum(TransitionMatrix[i]) == 0:
        TransitionMatrix[i][i] = 1
    
#Initial position
InitialVector = []
for state in states:
    if state == start_state:
        InitialVector.append(1)
    else:
        InitialVector.append(0)

#ProbabilityMatrix
ProbabilityMatrix = np.linalg.matrix_power(TransitionMatrix, steps)

#ProbabilityVector
ProbabilityVector = np.matmul(InitialVector, ProbabilityMatrix)
for i in range(len(ProbabilityVector)):
    ProbabilityVector[i] = round(ProbabilityVector[i], 2)
Result = dict(zip(states, ProbabilityVector))
print('\nProbability Vector:\n', Result)

#adding sizes (probabilities) to the graph nodes
for i in range(len(TransitionMatrix)):
    G.add_node(states[i], size = int(ProbabilityVector[i]*100))

#the gef file of the graph. You can use Gephi to open
nx.write_gexf(G, "Graph.gexf")
