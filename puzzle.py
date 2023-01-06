import copy

def create(puzzle):
    for i in range(3):
        puzzle[i] = input().split()
        puzzle[i] = [int(j) for j in puzzle[i]]
    
def checkValid(puzzle):
    all = []
    for i in puzzle:
        x = set(i)
        if len(x)!=len(i):
            print("not valid!(duplicate number)")
            return False
        for j in i:
            all.append(j)
            if j>8 or j<0:
                print("not valid!(unvalid number)")
                return False
    setall = set(all)
    if len(setall)!=len(all):
        print("not valid!(duplicate number)")
        return False
    return True
    
def createGoal(goal):
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

class node:

    def __init__(self, problem, parent, action):
        if parent is None:
            self.state = copy.deepcopy(problem.initialState)
            self.pathCost = 0
        else:
            self.state = problem.result(parent.state,action)
            self.pathCost = parent.pathCost + problem.stepCost(parent.state,action)
        self.parent = parent
        self.action = action


class problem:

    def __init__(self, initialState, goalState):
        self.initialState = initialState
        self.goalState = goalState
    
    def actions(self, state):
        listOfActions = ["right", "left" , "up", "down"]
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 0:
                    if i == 0:
                        listOfActions.remove("up")
                    if i == 2:
                        listOfActions.remove("down")
                    if j == 0:
                        listOfActions.remove("left")
                    if j == 2:
                        listOfActions.remove("right")
                    break
        return listOfActions

    def result(self, state, action):
        newState = copy.deepcopy(state)
        if action == "right":
            for i in range(3):
                for j in range(3):
                    if state[i][j] == 0:
                        newState[i][j], newState[i][j+1] = newState[i][j+1], newState[i][j]
        if action == "left":
            for i in range(3):
                for j in range(3):
                    if state[i][j] == 0:
                        newState[i][j], newState[i][j-1] = newState[i][j-1], newState[i][j] 
        if action == "up":
            for i in range(3):
                for j in range(3):
                    if state[i][j] == 0:
                        newState[i][j], newState[i-1][j] = newState[i-1][j], newState[i][j] 
        if action == "down":
            for i in range(3):
                for j in range(3):
                    if state[i][j] == 0:
                        newState[i][j], newState[i+1][j] = newState[i+1][j], newState[i][j] 
        return newState

    def stepCost(self, state, action):
        return 1

    def goalTest(self, state):
        return state == self.goalState


def solution(node):
    puzzles = []
    actions = []
    while node.parent:
        actions.append(node.action)
        puzzles.append(node.state)
        node = node.parent
    puzzles.append(node.state)
    return puzzles, actions


def Bidirectional(problem1, problem2):
    node1 = node(problem1, None, None)
    node2 = node(problem2, None, None)
    if node1.state == node2.state:
        return solution(node1)
    frontier1 = [node1]
    frontier2 = [node2]
    explored1 = []
    explored2 = []
    while True:
        if not(frontier1 and frontier2):
            print("fail :(")
            return [] , []
        node1 = frontier1[0]
        node2 = frontier2[0]
        frontier1.remove(node1)
        frontier2.remove(node2)
        explored1.append(node1)
        explored2.append(node2)
        for action in problem1.actions(node1.state):
            child1 = node(problem1, node1, action)
            notVisite = True
            if explored1:
                for explored in explored1:
                    if child1.state == explored.state:
                        notVisite = False
            if frontier1:
                for frontier in frontier1:
                    if child1.state == frontier.state:
                        notVisite = False
            if notVisite:
                for explored in explored2:
                    if explored.state == child1.state:
                        puzzles1, actions1 = solution(child1)
                        puzzles2, actions2 = solution(explored)
                        puzzles2.reverse()
                        puzzles2.pop()
                        actions2.reverse()
                        for i in range(len(actions2)):
                            if actions2[i] == "up":
                                actions2[i] = "down"
                            elif actions2[i] == "down":
                                actions2[i] = "up"
                            elif actions2[i] == "left":
                                actions2[i] = "right"
                            elif actions2[i] == "right":
                                actions2[i] = "left"
                        puzzles = puzzles2 + puzzles1
                        actions = actions2 + actions1
                        x = len(explored1) + len(explored2)
                        print("explored nodes:",end="")
                        print(x)
                        return puzzles , actions
                frontier1.append(child1)
        for action in problem2.actions(node2.state):
            child2 = node(problem2, node2, action)
            notVisite = True
            if explored2:
                for explored in explored2:
                    if child2.state == explored.state:
                        notVisite = False
            if frontier2:
                for frontier in frontier2:
                    if child2.state == frontier.state:
                        notVisite = False
            if notVisite:
                for explored in explored1:
                    if explored.state == child2.state:
                        puzzles2, actions2 = solution(child2)
                        puzzles1, actions1 = solution(explored)
                        puzzles1.reverse()
                        puzzles1.pop()
                        actions1.reverse()
                        for i in range(len(actions1)):
                            if actions1[i] == "up":
                                actions1[i] = "down"
                            elif actions1[i] == "down":
                                actions1[i] = "up"
                            elif actions1[i] == "left":
                                actions1[i] = "right"
                            elif actions1[i] == "right":
                                actions1[i] = "left"
                        puzzles = puzzles1 + puzzles2
                        actions = actions1 + actions2
                        x = len(explored1) + len(explored2)
                        print("explored nodes:",end="")
                        print(x)
                        puzzles.reverse()
                        actions.reverse()
                        for i in range(len(actions)):
                            if actions[i] == "up":
                                actions[i] = "down"
                            elif actions[i] == "down":
                                actions[i] = "up"
                            elif actions[i] == "left":
                                actions[i] = "right"
                            elif actions[i] == "right":
                                actions[i] = "left"
                        return puzzles , actions
                frontier2.append(child2)



def h1(state, goal):
    h = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                continue
            if not (goal[i][j] == state[i][j]):
                h+=1
    return h


def h2(state, goal):
    h = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                continue
            for n in range(3):
                for m in range(3):
                    if state[i][j] == goal[n][m]:
                        h+=(abs(i-n)+abs(j-m))
    return h

def Astar(problem, selecthHeuristic):
    initial = node(problem, None, None)
    frontier = [initial]
    explored = []
    if selecthHeuristic == 1:
        h = h1(initial.state, problem.goalState)
    else:
        h = h2(initial.state, problem.goalState)
    g = initial.pathCost
    f = g + h
    listOfF = [f]
    while True:
        if not (frontier):
            print("fail :(")
            return [], []
        priority = frontier[listOfF.index(min(listOfF))]
        if priority.state == problem.goalState:
            p , a = solution(priority)
            print("explored nodes:",end="")
            print(len(explored))
            return p , a
        explored.append(priority)
        for action in problem.actions(priority.state):
            child = node(problem, priority, action)
            notVisite = True
            if explored:
                for e in explored:
                    if child.state == e.state:
                        notVisite = False
            if frontier:
                for f in frontier:
                    if child.state == f.state:
                        notVisite = False
            if notVisite:
                frontier.append(child)
                if selecthHeuristic == 1:
                    h = h1(child.state, problem.goalState)
                else:
                    h = h2(child.state, problem.goalState)
                g = child.pathCost
                f = g + h
                listOfF.append(f)
        listOfF.remove(listOfF[frontier.index(priority)])
        frontier.remove(priority)

        

print("set your puzzle:")
while True:
    puzzle = [[],[],[]]
    create(puzzle)
    if checkValid(puzzle):
        break
goal = [[0, 1, 2]
       ,[3, 4, 5]
       ,[6, 7, 8]]
print("")

startPuzzle = problem(puzzle, goal)
endPuzzle = problem(goal, puzzle)

print("select your search algoritm:")
print("1-Bidirectional")
print("2-Manhatan")
print("3-Misplase")
algoritm = input()
print("")
if algoritm == "1":
    p , a = Bidirectional(startPuzzle, endPuzzle)
elif algoritm == "2":
    p , a = Astar(startPuzzle, 2)
else:
    p , a = Astar(startPuzzle, 1)

p.reverse()
a.reverse()

print("")
k = 0
for i in p:
    for j in i:
        print(j)
    if (k<len(a)):
        print("")
        print(a[k])
        k+=1
    print("")
print("number of actions:",len(a))