# Author : Blake Leahy 

# PlayingPartitions - simulate a ferrers board partition game where the outcoe is to be determined by 
# the initial and goal partitions where players make a PathfindingPartitions Move until the initial 
# partition reaches a goal partition.

# Partitions represented as integers where each integer shows the num of tokens in a column 
# Moves - translations between partitions by moving tokens from columns to rows (or backward for backtrackig)
# Mood - Each partition is either: happy, sad or neutral. 
# A partition is SAD when a player will lose if the game reaches this partition 
# A partition is happy whe na player will win if the game reaches this partition 
# A game will result in neutral / draw if the game never reaches this partition

# Approach : 
# Parse input separating scenarios 
# For each of these scenarios parsed, get outcome of the game from starting position / initial partition
# use Ddepth first search to find happy and sad moods through game states 
# Need functions to go from ColumnToRow like in pathfindingPartitions, and additionally a RowToColumn to backtrack 
# Assisted w copilot  

# helper functions 

import sys


def SortPartition(line):
    nums = list(map(int, line.split()))
    sortedNums = sorted(nums, reverse=True)
    return tuple(sortedNums)

def isPartition(partition):
    if any(num <= 0 for num in partition):
        return False

    for i in range(1, len(partition)):
        if partition[i] > partition[i - 1]:
            return False

    return True

def isSeparator(line):
    return len(line.strip('-')) == 0 and line.count("-") >= 3

# col/row swappers 

def ColumnToRow(partition, col, row):

    newRow = 0 
    newPartition = list(partition)
    
    for i in range(len(partition)):

        if newPartition[i] >= (col + 1):
            newPartition[i] -= 1
            newRow += 1

    bottomRows = newPartition[row:]

    topRows = newPartition[:row]

    if newRow > 0:
        newPartition = topRows + [newRow] + bottomRows
    else:
        newPartition = topRows + bottomRows

    newPartition = [x for x in newPartition if x != 0]

    return tuple(newPartition)


def RowToColumn(partition, col, row):

    newPartition = list(partition)
    length = newPartition[row]

    del newPartition[row]

    for i in range(length):

        if i < len(newPartition):
            newPartition[i] += 1
        else:
            newPartition.append(1)

    return tuple(newPartition)

# PlayPartitions function searches possible game states with inner DFS function
def PlayPartitions(initialPartition, goalPartitions):

    moods = {} 

    for goalPartition in goalPartitions:

        moods[goalPartition] = "sad"

    def DFS(currentMove, moods):

        if currentMove in moods:

            if moods[currentMove] == "sad":

                for col in range(currentMove[0]):
                    for row in range(len(currentMove)):

                        newPartition = RowToColumn(currentMove, col, row)

                        if not isPartition(newPartition):
                            continue

                        if newPartition not in moods:
                            moods[newPartition] = "happy"
                            DFS(newPartition, moods)
            else:

                for col in range(currentMove[0]):
                    for row in range(len(currentMove)):

                        newPartition = RowToColumn(currentMove, col, row)

                        if not isPartition(newPartition):
                            continue

                        if newPartition not in moods:
                            
                            AllOutcomesHappy = True

                            for col in range(newPartition[0]):
                                for row in range(len(newPartition)):

                                    if len(newPartition) == 1 or row + 1 == len(newPartition):
                                        nextPartition = ColumnToRow(newPartition, col, row + 1)
                                    else:
                                        nextPartition = ColumnToRow(newPartition, col, row)
                                    if not isPartition(nextPartition):
                                        continue
                                    if moods.get(nextPartition) != "happy":
                                        AllOutcomesHappy = False
                                        break
                                if not AllOutcomesHappy:
                                    break

                            if AllOutcomesHappy:
                                moods[newPartition] = "sad"
                                DFS(newPartition, moods)

    for goalPartition in goalPartitions:
        DFS(goalPartition, moods)

    if moods.get(initialPartition) == "happy":
        return "# WIN"
    
    elif moods.get(initialPartition) == "sad":
        return "# LOSE"
    
    else:
        return "# DRAW"

# parse input     
def main():

    scenario = []
    scenarios = []

    for line in sys.stdin:

        line = line.rstrip('\n')

        if line.startswith("#"):
            continue
        if len(line.strip()) == 0:
            continue
        elif isSeparator(line):
            scenarios.append(scenario)
            scenario = []
        else:
            scenario.append(SortPartition(line))

    scenarios.append(scenario)

    for i, scenario in enumerate(scenarios):

        if i > 0:
            print('-' * 8) # end of scenario 

        initialPartition = scenario[0]
        goalPartitions = [partition for partition in scenario[1:]]

        print(" ".join(map(str, initialPartition)))

        print("")
        
        for goalPartition in goalPartitions:
            print(" ".join(map(str, goalPartition)))

        print(PlayPartitions(initialPartition, goalPartitions))

main()