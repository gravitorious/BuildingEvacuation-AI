"""
**  BuildingEvacuation1.AILab.py
**  BuildingEvacuation-AI
**
**  Created by Nikolaos Mavrogeneiadis - 161014 on 17/11/2018.
**  Copyright © 2018 Nikolaos Mavrogeneiadis. All rights reserved.
"""

from collections import deque


def search_problem(start_state, goal, method):
    """
    **starts the problem
    """
    find_solution(make_front(start_state), make_queue(start_state), [], goal, method)


def find_solution(front, queue, closed, goal, method):
    """
    **makes the search tree recursive
    """


def make_front(state):
    """
    **initialize front
    """
    front = deque(state)
    front.insert(0, state)

def expand_front():
    """
    ** expanding the front
    """
    pass


def make_queue(state):
    """
    **initialize queue
    """
    queue = deque()
    queue.insert(0, state)


def extend_queue():
    """
    **extending the queue with growpath
    """
    pass


def grow_path():
    """
    **growing path towards each different child of the selected parent node
    """
    pass


def find_children(state):
    """
    **returns all new states from one state
    """
    return_list = [go_to_floor1(state), go_to_floor2(state), go_to_floor3(state)]
    return return_list


# transition operators

def go_to_floor1(state):
    """
    goes to first floor
    """
    new_state = state.copy()
    if controls_for_change_floor(new_state, 1):
        new_state[0] = 1
        if 5 - new_state[1] >= new_state[3]:
            take = state[1]
        else:
            take = 5 - new_state[1]
        new_state[1] += take
        new_state[3] -= take
        return new_state
    else:
        return None


def go_to_floor2(state):
    """
    **goes to second floor
    """
    new_state = state.copy()
    if controls_for_change_floor(new_state, 2):
        new_state[0] = 2
        if 5 - new_state[1] >= new_state[4]:
            take = state[1]
        else:
            take = 5 - new_state[1]
        new_state[1] += take
        new_state[4] -= take
        return new_state
    else:
        return None


def go_to_floor3(state):
    """
    **goes to third floor
    """
    new_state = state.copy()
    if controls_for_change_floor(new_state, 3):
        new_state[0] = 3
        if 5 - new_state[1] >= new_state[5]:
            take = state[1]
        else:
            take = 5 - new_state[1]
        new_state[1] += take
        new_state[5] -= take
        return new_state
    else:
        return None



def go_to_ground_floor(state):
    """
    goes to ground floor and empty the elevator
    """
    if controls_for_ground_floor(state):
        return_state = state.copy()
        return_state[0] = 0
        return_state[1] = 0
        return return_state
    else:
        return None


# other functions

def controls_for_ground_floor(state):
    """
    Checks if the elevator can go to the ground floor
    """
    if check_if_elevator_is_full(state) or check_if_floors_are_empty(state):
        return True
    else:
        return False



def check_if_elevator_is_full(state):
    """
    Checks if elevator is full (5/5)
    """
    if state[1] == 5:
        return True
    else:
        return False


def check_if_floors_are_empty(state):
    """
    Checks if floors are empty. It returns True if third, fourth, and fifth elements are zero.
    """

    if state[2] == 0 and state[3] == 0 and state[4] == 0:
        return True
    else:
        return False




def check_for_goal_state(state):
    """
    checks if state is the goal state
    If state contains only zeros, it means that state is the goal state
    so we return true
    """
    if all(s == 0 for s in state):
        return True
    else:
        return False


def controls_for_change_floor(state, floor):
    """
    If elevator is already on the floor, it can't go again on this floor
    If elevator is full, it cant go on this floor
    If floor is empty, there is no need to visit it
    """
    if state[0] == floor:
        return False
    elif state[1] == 5:
        return False
    elif state[floor+1] == 0:
        return False
    return True


# program starts here

if __name__ == '__main__':

    """
    Structure of state
    (floor of elevator, capacity of elevator, capacity of 1st floor, capacity of 2nd floor, capacity of 3rd floor)
    """

    # search algorithm
    method = 'DFS'

    # init first state
    initialState = [0, 0, 4, 6, 2]

    # init goal state
    goalState = [0, 0, 0, 0, 0]

    #searchproblem(initialState, goalState, method)

