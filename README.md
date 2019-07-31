What we do here: 
1) take a user activity log
2) execute the script that trains a Markov Chain and outputs it as a .gefx file
3) open the file

More details:
# Markov Chain definition
We have a set of states, S = {s[1], s[2], ..., s[N]} (these states may represent some events in user logs). The process starts in one of these states and moves successively from one state to another. Each move is called a step. If the chain is currently in state s[i] , then it moves to state s[j] at the next step with a probability denoted by p[i][j], and this probability does not depend upon which states the chain was in before the current.
Markov chain is defined by its “Transition matrix” P (containing p[i][j]) of size NxN, where N – is the quantity of nodes in the chain.
In our particular case we built a chain to visualize user activity in some MOOC. Each node - is a certain kind of event that happened to users. Each line in the data file - is a specific event that happened to a specific user in a specific time

# Data format
The data of user activity should include identification of a user, name of a "step" committed by a user and the time of that step – so that for each user it would be possible to represent his activity as sequence of state-nodes, following one another. The nodes of the chain, in the essence, represent events happening to our user.
The data format should be as in the file **worklist.csv** in the repo. First column - *user id*, second - *event name*, third - *time* in excel-like format represented as a number - but the table should have **no header**

# How to launch 
Run the script **MarkovChain.py** in any Python 3 IDE having your user activity log in a format described earlier in your working directory. By default the data file should be named **worklist.csv**. The script will create a **Graph.gexf** - a graph file representing the trained Markov Chain. 

# Visualize
Use Gephi or any other graph visualization tool that supports the **.gefx** format to open the resulting file. After some customization within Gephi project you may obtain something like **General.gephi** file in the repo (also saved as **.pdf** picture in the repo for the sake of clarity). 

For more details read comments in the code in **MarkovChain.py**
