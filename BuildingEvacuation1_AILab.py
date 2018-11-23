"""
**  BuildingEvacuation1.AILab.py
**  BuildingEvacuation-AI
**
**  Created by Nikolaos Mavrogeneiadis - 161014 on 17/11/2018.
**  University of West Attica
**  Department of Informatics and Computer Engineering
**  Artificial Intelligence Lab
**  Copyright © 2018 Nikolaos Mavrogeneiadis. All rights reserved.
"""

from collections import deque
import sys


def search_problem(start_state, goal, mymethod):
    """
    Beginning the search algorithm
    """
    if mymethod != 'BFS' and mymethod != 'DFS':
        print("Sorry... we don't support this search algorithm!")
        return None
    else:
        return find_solution(make_front(start_state), make_queue(start_state), [], goal, mymethod)


def find_solution(front, queue, closed, goal, mymethod):
    """
    builds the search tree recursive
    """

    if not front:  #  if front list is empty we didn't find a solution
        return None
    first_state = front.popleft()  # pop the first state from search frontier
    first_path = queue.popleft()  #  pop the first path from queue
    if first_state in closed:  # check if the next state is on closed set
        final_state = find_solution(front, queue, closed, goal, mymethod)  # if it is, we continue with the next state
    else:
        if check_for_goal_state(first_state):  # if first state from search frontier is the goal state, we finish!
            return first_path  # the result is the path from parent node to goal node (first element of queue)
        else:
            """add the node we will make child nodes on closed set"""
            closed.append(first_state)

            """make the new states"""
            new_states = find_children(first_state)  # get new states

            """remove none objects"""
            final_states = remove_none_states(new_states)

            """
            let's expand search frontier
            We don't add the none states on search frontier. Also, we don't create new paths
            """
            expand_front(front, final_states, mymethod)


            """
            so, we are ready to extend the queue
            """
            extend_queue(queue, final_states, first_path, mymethod)

            """
            check the next state on search frontier recursively
            """
            final_state = find_solution(front, queue, closed, goal, mymethod)

    return final_state



def make_front(state):
    """
    initialize front
    """
    front = deque()
    front.append(state)
    return front


def expand_front(front, new_states, mymethod):
    """
    expanding the front
    if new_states are only None objects (so node hasn't any child) there is no problem
    cause we removed them, so we extend an empty list and there is no result
    We want to put each element (list object) of new_states (not the entire list) on left side (if DFS) or
    right side (if BFS) on front
    So, we reverse new_states (cause extendleft() put elements on the other way) and extend them on
    search frontier
    """
    if mymethod == 'DFS':
        front.extendleft(reversed(new_states.copy()))  # put all new states on start on search frontier
    elif mymethod == 'BFS':
        front.extend(new_states.copy())  # there is no need to reverse


def make_queue(state):
    """
    initialize queue
    """

    """init queue with first state"""
    queue = deque()

    """we put the first state on list"""
    list_for_initstate = [state]

    """put first state on queue"""
    queue.append(list_for_initstate)
    return queue


def extend_queue(queue, states, first_path, mymethod):
    """
    add new paths on queue recursively
    we finish when we don't have other states to add on queue
    """

    if mymethod == 'DFS':
        if not states:
            return None
        else:
            f_path = first_path.copy()
            """
            we pop the last element from states, append it on previous path, and append it
            left on queue, so the first path be first on queue
            e.g. Previous path: A
            D -> AD, C -> AC-AD, B -> AB-AC-AD
            """
            first_path.append(states.pop())  # pop last state and append it on previous path
            queue.appendleft(first_path)  # append path on left side
            extend_queue(queue, states, f_path, mymethod)  # continue with the next state
    elif mymethod == 'BFS':
        if not states:
            return None
        else:
            f_path = first_path.copy()
            """
            the operations are the same as previous with the only difference that
            we pop the first state and append it on the right side of queue
            e.g. Previous path: AB AC
            D -> AC ABD, E -> AC ABD ABE, F -> AC ABD ABE ABF
            """
            first_path.append(states.pop(0))
            queue.append(first_path)
            extend_queue(queue, states, f_path, mymethod)


def find_children(state):
    """
    returns all new states from one state as a list
    """
    return_list = [go_to_ground_floor(state), go_to_floor1(state), go_to_floor2(state), go_to_floor3(state)]
    return return_list


# transition operators

def go_to_floor1(state):
    """
    goes to first floor
    """
    new_state = modify_state(state, 1)  # send state and floor
    return new_state


def go_to_floor2(state):
    """
    goes to second floor
    """

    new_state = modify_state(state, 2)  # send state and floor
    return new_state


def go_to_floor3(state):
    """
    goes to third floor
    """
    new_state = modify_state(state, 3)  # send state and floor
    return new_state


def go_to_ground_floor(state):
    """
    goes to ground floor and empty the elevator
    """
    if controls_for_ground_floor(state):  # check if elevator is able to move on ground floor
        return_state = state.copy()
        return_state[0] = 0
        return_state[1] = 0
        return return_state
    else:
        return None


# other functions

def modify_state(state, floor):
    new_state = state.copy()
    if controls_for_change_floor(new_state, floor):  # if elevator is able to go on this floor
        new_state[0] = floor  # change floor
        if 5 - new_state[1] >= new_state[floor+1]:  # if the capacity of elevator is more than the capacity of floor
            take = new_state[floor+1]  # take all the tenants
        else:
            take = 5 - new_state[1]  # take only as many as you can
        new_state[1] += take  # new capacity of elevator
        new_state[floor+1] -= take  # remaining tenants on this floor
        return new_state
    else:
        return None


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


if __name__ == '__main__':
    def main(args):
        """
        declaration of initial state, final state, and ... begins the program!
        Structure of state
        (floor of elevator, capacity of elevator, capacity of 1st floor, capacity of 2nd floor, capacity of 3rd floor)
        """

        if len(args) == 1:
            """
            if you run it from IDE and you want other search algorithm, 
            change this variable
            """
            my_method = 'DFS'
        else:
            my_method = args[1]

        # init first state
        initial_state = [0, 0, 2, 6, 4]

        # init goal state
        goal_state = [0, 0, 0, 0, 0]

        result = search_problem(initial_state, goal_state, my_method)
        if result:
            print("Yay! We found a solution! With method:", my_method, "! The path is:\n", result)
        else:
            print("Oups... Sorry, there is no solution on this problem")


# program starts here
main(sys.argv)