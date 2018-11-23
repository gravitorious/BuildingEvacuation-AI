"""
**  BuildingEvacuation1.AILab.py
**  BuildingEvacuation-AI
**
**  Created by Nikolaos Mavrogeneiadis - 161014 on 17/11/2018.
**  Copyright © 2018 Nikolaos Mavrogeneiadis. All rights reserved.
"""

from collections import deque


def search_problem(start_state, goal, mymethod):
    """
    **starts the problem
    """
    return find_solution(make_front(start_state), make_queue(start_state), [], goal, mymethod)


def find_solution(front, queue, closed, goal, mymethod):
    """
    **makes the search tree recursive
    """
    print(front, queue, closed)
    if not front:  #  if front list is empty we didn't find a solution
        return None
    first_state = front.popleft()  # pop the first state from search frontier
    first_path = queue.popleft()  #  pop the first path from queue
    if first_state in closed:  # check if the next state is on closed set
        final_state = find_solution(front, queue, closed, goal, mymethod)  # if it is, we continue with the next state
    else:
        if check_for_goal_state(first_state):  # if first state from search frontier is the goal state, we finish!
            return first_path  # the result is the path from parent node to goal node
        else:
            """add the node we will visit to closed set"""
            closed.append(first_state)

            """make the new states"""
            new_states = find_children(first_state)  # get new states

            """remove none objects"""
            final_states = remove_none_states(new_states)

            """we don't add the none states on search frontier. Also, we don't create new paths"""
            expand_front(front, final_states)


            """
            so, we are ready to extend the queue
            """
            extend_queue(queue, final_states, first_path)

            final_state = find_solution(front, queue, closed, goal, mymethod)


    return final_state



def make_front(state):
    """
    **initialize front
    """
    front = deque()
    front.append(state)
    return front


def expand_front(front, new_states):
    """
    ** expanding the front
    """

    """
    if states were only None objects (so node hasn't any child) there is no problem
    cause we removed them, so we extend an empty list
    """

    front.extendleft(reversed(new_states.copy()))  # put all new states on start on search frontier


def make_queue(state):
    """
    **initialize queue
    """

    """init queue with first state"""
    queue = deque()
    """we put the first state on list"""
    list_for_initstate = [state]
    """put first state on queue"""
    queue.append(list_for_initstate)
    return queue


def extend_queue(queue, states, first_path):
    """
    **extending the queue with growpath
    """

    """we finish when we don't have other states to add on queue"""

    if not states:
        return None
    else:
        f_path = first_path.copy()
        first_path.append(states.pop(len(states)-1))
        queue.appendleft(first_path)
        extend_queue(queue, states, f_path)


def grow_path():
    """
    **growing path towards each different child of the selected parent node
    """
    pass


def find_children(state):
    """
    **returns all new states from one state
    """
    return_list = [go_to_ground_floor(state), go_to_floor1(state), go_to_floor2(state), go_to_floor3(state)]
    return return_list


# transition operators

def go_to_floor1(state):
    """
    goes to first floor
    """
    new_state = state.copy()
    if controls_for_change_floor(new_state, 1):
        new_state[0] = 1
        if 5 - new_state[1] >= new_state[2]:
            take = new_state[2]
        else:
            take = 5 - new_state[1]
        new_state[1] += take
        new_state[2] -= take
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
        if 5 - new_state[1] >= new_state[3]:
            take = new_state[3]
        else:
            take = 5 - new_state[1]
        new_state[1] += take
        new_state[3] -= take
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
        if 5 - new_state[1] >= new_state[4]:
            take = new_state[4]
        else:
            take = 5 - new_state[1]
        new_state[1] += take
        new_state[4] -= take
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


def remove_none_states(new_states):
    """ remove None objects from list """
    ls = [x for x in new_states if x is not None]
    return ls


# program starts here

if __name__ == '__main__':

    """
    Structure of state
    (floor of elevator, capacity of elevator, capacity of 1st floor, capacity of 2nd floor, capacity of 3rd floor)
    """
    # search algorithm
    mymethod = 'DFS'

    # init first state
    initialState = [0, 0, 2, 6, 4]

    # init goal state
    goalState = [0, 0, 0, 0, 0]

    result = search_problem(initialState, goalState, mymethod)
    if result:
        print("Yay! We found a solution! The path is:\n", result)

