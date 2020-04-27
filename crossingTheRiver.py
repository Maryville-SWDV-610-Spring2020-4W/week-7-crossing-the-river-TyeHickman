#Tye Hickman
#Week 7
#Crossing the River

class StateNode:
    def __init__(self,state,parent = None):
        self.state = state
        self.parent = parent
    
#We need a queue for Breadth-First Search so I just grabbed my implementation from week 4
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []
    
    # Queues are First in First out so we can add to them just like a stack (enqueue)
    # But need to ensure that dequeue is only removing from the "rear" of the queue

    def enqueue(self,item):
        self.items.insert(0,item)

    def dequeue(self):
        if self.isEmpty():
            return "Queue is empty"
        else:
            # self.items.pop()
            return self.items.pop()
            # pop() takes an option position parameter. If left blank, it defaults to -1
            # whish is the last item in a list, which is the FIRST IN for the queue

    def size(self):
        return len(self.items)

    def printQueue(self):
        if self.isEmpty():
            print("Queue is empty")
        else:
            for item in self.items:
                print(str(self.items.index(item)) + " " +str(item))
                # print(item)

MAX_PEOPLE = 3
class State:
    def __init__(self, missionaries, cannibals, boat):
        self.key = tuple([missionaries,cannibals,boat])
        self.stM = missionaries #Missionaries on starting bank
        self.stC = cannibals #Cannibals on starting bank
        self.destM = MAX_PEOPLE - self.stM #Missionaries on destination bank
        self.destC = MAX_PEOPLE - self.stC #Cannibals on destination bank
        self.boat = boat #True = starting bank; False = destination bank

    def isValid(self):
        if self.stM < self.stC and self.stM > 0:
            return False
        if self.destM < self.destC and self.destM > 0:
            return False
        return True

    def isGoalState(self):
        return self.isValid and self.destM == MAX_PEOPLE and self.destC == MAX_PEOPLE

    def successors(self):
        successorList = []
        if self.boat: #Starting Bank
            if self.stM > 1:
                successorList.append(State(self.stM -2, self.stC,not self.boat))
            if self.stM > 0:
                successorList.append(State(self.stM -1, self.stC, not self.boat))
            if self.stC > 1:
                successorList.append(State(self.stM, self.stC -2, not self.boat))
            if self.stC > 0:
                successorList.append(State(self.stM, self.stC -1, not self.boat))
            if (self.stC > 0) and (self.stM > 0):
                successorList.append(State(self.stM -1, self.stC -1, not self.boat))
        else: # boat is at destination bank
            if self.destM > 1:
                successorList.append(State(self.stM +2, self.stC, not self.boat))
            if self.destM > 0:
                successorList.append(State(self.stM +1, self.stC, not self.boat))
            if self.destC > 1:
                successorList.append(State(self.stM, self.stC +2, not self.boat))
            if self.destC > 0:
                successorList.append(State(self.stM, self.stC +1, not self.boat))
            if (self.destC > 0) and (self.destM > 0):
                successorList.append(State(self.stM + 1, self.stC +1, not self.boat))
        return [x for x in successorList if x.isValid()]

    def __str__(self):
        return ("Starting bank has {} Missionaries and {} Cannibals.\n"
                "Destination bank has {} Missionaries and {} Cannibals.\n"
                "The boat in on the {} side."
                .format(self.stM,self.stC,self.destM,self.destC,("Starting" if self.boat else "Destination")))

def dispalyOutcome(stateList):
    if len(stateList) == 0:
        return
    
    old = stateList[0]
    print(old)
    for current in stateList[1:]:
        if current.boat:
            print("Moved {} Missionaries and {} Cannibals to Starting bank"
                    .format(old.stM - current.stM, old.stC - current.stC))
        else:
            print("Moved {} Missionaries and {} Cannibals to Destination bank"
                    .format(old.destM - current.destM, old.destC - current.destC))
        print(current)
        old = current

def bfs(initialState):
    #Queue initial state to start exploration
    unexplored = Queue()
    unexplored.enqueue(StateNode(initialState,None))

    # Sets are immutable and cannot contain duplicates 
    # makes sense to use for what we've already looked at
    exploredStates = set()
    exploredKeys = set()
    exploredStates.add(StateNode(initialState))
    exploredKeys.add(initialState.key)

    while not unexplored.isEmpty():
        currentNode = unexplored.dequeue()
        # print(currentNode.state)
        currentState = currentNode.state

        # for child in stateSuccessors(currentState):
        for child in currentState.successors():
            if child.key in exploredKeys:
                # print("This child exists: " + str(child))
                continue
            # print(child)
            else:
                # exploredStates.add(StateNode(child,currentState))
                exploredKeys.add(child.key)
                unexplored.enqueue(StateNode(child,currentState))
        # if goalTest:
        if currentState.isGoalState():
            return currentNode
    return None

def nodePath(stNode):
    path = [stNode.state]

    while stNode.parent is not None:
        stNode = stNode.parent
        path.append(stNode)
    path.reverse()
    return path

def main():
    start = State(MAX_PEOPLE,MAX_PEOPLE,True)
    solution = bfs(start)
    if solution is None:
        print("No Solution Found")
    else: 
        print("Solution was found: " + str(solution.state) + " " + str(solution.parent))
        # pathList = nodePath(solution)
        # dispalyOutcome(pathList)
main()