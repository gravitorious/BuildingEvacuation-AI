from collections import deque


def searchproblem(start_state, goal, method):
    """
    ** starts the problem
    """
    findsolution(makefront(start_state), makequeue(start_state), [], goal, method)


def findsolution(front, queue, closed, goal, method):
    """
    ** makes the search tree recursive
    """








def makefront(state):
    """
    ** initialize front
    """
    front = deque(state)


def expandfront():
    """
    ** expanding the front
    """
    pass

def makequeue(state):
    """
    ** initialize queue
    """
    queue = deque()

def extendqueue():
    """
    ** extending the queue with growpath
    """
    pass


def growpath():
    """
    ** growing path towards each different child of the selected parent node
    """
    pass

def findChildren():
    """
    ** returns all new states for one state
    """
    pass


#operators

def gotofloor1():
    """
    goes to first floor
    """
    pass

def gotofloor2():
    """
        goes to second floor
        """
    pass

def gotofloor3():
    """
        goes to third floor
        """
    pass

def gotofloor3():
    """
        goes to third floor
        """
    pass



"""
other functions
"""


if __name__ == '__main__':
    # search algorithm
    method = 'DFS'

    # init first state
    initialState = [0, 0, 4, 6, 2]

    # init goal state
    goalState = [0, 0, 0, 0, 0]

    #searchproblem(initialState, goalState, method)


