# -*- coding: utf-8 -*-
"""
**  BuildingEvacuation1.AILab.py
**  BuildingEvacuation-AI
**
**  Created by Nikolaos Mavrogeneiadis - 161014 on 7/12/2018.
**  University of West Attica
**  Department of Informatics and Computer Engineering
**  Artificial Intelligence Lab
**  Copyright © 2018 Nikolaos Mavrogeneiadis. All rights reserved.
"""

from collections import deque
from math import ceil
import sys

recursive_cycles = 0


def search_problem(start_state, goal, mymethod):
    """
    Beginning the search algorithm
    """
    if mymethod != 'BFS' and mymethod != 'DFS' and mymethod != 'A*':
        print("Sorry... we don't support this search algorithm!")
        return None
    else:
        return find_solution(make_front(start_state), make_queue(start_state), [], goal, mymethod)


def find_solution(front, queue, closed, goal, mymethod):
    """
    builds the search tree recursive
    """


    with open('trace_of_front.txt', 'a') as trace_of_front_file:
        trace_of_front_file.write(front.__str__() + "\n")
    with open('trace_of_queue.txt', 'a') as trace_of_queue_file:
        trace_of_queue_file.write(queue.__str__() + "\n")
    global recursive_cycles

    if not front:  #  if front list is empty we didn't find a solution
        return None
    first_state = front.popleft()  # pop the first state from search frontier
    first_path = queue.popleft()  #  pop the first path from queue
    if first_state in closed:  # check if the next state is on closed set
        final_state = find_solution(front, queue, closed, goal, mymethod)  # if it is, we continue with the next state
    else:
        if check_for_goal_state(first_state, goal):  # if first state from search frontier is the goal state, we finish!
            with open('results.txt', 'a') as results:  #write the number ofrecursive cycles
                results.write("Συνολικοί αναδρομικοί κύκλοι: " + recursive_cycles.__str__() + "\n")
            return first_path  # the result is the path from parent node to goal node (first element of queue)
        else:
            # add the node we will make child nodes on closed set
            closed.append(first_state)

            # make the new states
            new_states = find_children(first_state)  # get new states

            # remove none objects
            final_states = remove_none_states(new_states)

            """
            let's expand search frontier
            We don't add the none states on search frontier. Also, we don't create new paths
            """
            expand_front(front, final_states, mymethod)



            # so, we are ready to extend the queue
            extend_queue(queue, final_states, first_path, mymethod)

            # if method is A* we need to sort the front and queue by the heuristic value
            if mymethod == 'A*':
                front, queue = alan_sort(front, queue)


            # check the next state on search frontier recursively
            recursive_cycles += 1
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
    elif mymethod == 'BFS' or mymethod == 'A*':
        front.extend(new_states.copy())  # there is no need to reverse


def make_queue(state):
    """
    initialize queue
    """

    # init queue with first state
    queue = deque()

    # we put the first state on list
    list_for_initstate = [state]

    # put first state on queue"""
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
    elif mymethod == 'BFS' or mymethod == 'A*':
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



def check_for_goal_state(state, goal):
    """
    checks if state is the goal state
    If state contains only zeros, it means that state is the goal state
    so we return true
    """
    if state == goal:
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


def alan_sort(front, queue):

        z = list(queue)  #add queue on new list

        # sort this list by the heuristic value
        z.sort(key=lambda x: a_asterisk(x))

        # clear front and queue
        front = list()
        queue = list()

        # make front and queue again from the sorted list
        for i in range(len(z)):
            front.append(z[i][-1])
            queue.append(z[i])

        # return the sorted front and queue
        return deque(front), deque(queue)


def a_asterisk(mylist):

    g_value = len(mylist)-1

    return g_value + h(mylist[-1])


def h(state):

    el_residents = state[1]
    residents_on_first = state[2]
    residents_on_sec = state[3]
    residents_on_third = state[4]

    """times that the elevator goes to ground floor"""
    gr_floor = el_residents + residents_on_first + residents_on_sec + residents_on_third
    times_grfloor = ceil(gr_floor/5)


    """times are needed to take all the residents from floors"""
    times_to_firstfl = ceil(residents_on_first / 5)
    times_to_secfl = ceil(residents_on_sec / 5)
    times_to_thirdfl = ceil(residents_on_third / 5)

    h_value = times_grfloor + times_to_firstfl + times_to_secfl + times_to_thirdfl
    return h_value


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
            my_method = 'A*'
        else:
            my_method = args[1]

        # init first state
        initial_state = [0, 0, 2, 6, 4]

        # init goal state
        goal_state = [0, 0, 0, 0, 0]

        result = search_problem(initial_state, goal_state, my_method)

        if result:
            print("Yay! We found a solution! With method:", my_method, "! The path is:\n", result)
            print("Check Results on results.txt and trace on trace_of_front.txt & trace_of_queue.txt")
            with open('results.txt', 'a') as results:  # write the number ofrecursive cycles
                results.write("Αλγόριθμος: " + my_method.__str__() + "\n")
                results.write("Αρχική Κατάσταση: " + initial_state.__str__() + "\n")
                results.write("Τελική Κατάσταση: " + goal_state.__str__() + "\n")
                results.write("Μέγεθος τελικού path: " + (len(result) - 1).__str__() + "\n")
                results.write("Τελικό path: " + result.__str__() + "\n")
        else:
            print("Oups... Sorry, there is no solution to this problem")


""" 
program starts here
"""

# create files
with open('trace_of_front.txt', 'w') as trace_of_front_file:
    pass
with open('trace_of_queue.txt', 'w') as trace_of_queue_file:
    pass
with open('results.txt', 'w') as results:
    pass

# call main method
main(sys.argv)
