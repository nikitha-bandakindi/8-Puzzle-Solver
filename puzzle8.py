import heapq
import copy

# step-1: initializing goal state and initial state (We can also use input to give initial states)
goal_state =   [[1, 2, 3],
[8, 0, 4],
[7, 6, 5]]

initial_state = [[2, 8, 3],
[1, 6, 4],
[7, 0, 5]]




print("Goal State:")
print(*goal_state, sep="\n")
print("Initial state:")
print(*initial_state, sep="\n")

# Below is a function to get index of an element from a nested list
def getindex(my_list, number):
    for sublist in my_list:
        if number in sublist:
            return (my_list.index(sublist), sublist.index(number))
        
#Step-2 defining a heuristic function which returns the total manhattan distance h(n) i.e., it measures the number of steps 
# required for a tile to reach the correct position as in the goal state from the current position in the current state. This distance is checked for
#  all the misplaced tiles and added to return the overall manhattan distance of a particular state
def get_manhattan_distance(selected_state):
    distance_sum = 0
    for line in selected_state:
        for element in line:
            distance = 0
            current_index = getindex(selected_state, element)
            goal_index = getindex(goal_state, element)
            if current_index != goal_index:
                distance += abs(goal_index[0]-current_index[0]) + abs(goal_index[1]-current_index[1])
                distance_sum += distance
    return distance_sum

# step-3: creating a priority queue data structure - T
open_list = []

# initializing a data structure to keep track of all the states our agent has already seen so that we don't come across duplicate states 
# which leads to additional unnecessary steps. We are adding initial state to seen_states list
seen_states = set()
seen_states.add(str(initial_state))

#step-4: adding initial state to the priority queue (open_list in this case)
heapq.heappush(open_list, (0, initial_state, "i", 0)) 

# The calculate_priority() function returns the priority of a particular state (priority = Manhattan distance, h(n) + cost i.e.., number of
#  steps taken by initial state to reach current position, g(n) )
def calculate_priority(state, g_n_value):
    manhattan_distance = get_manhattan_distance(state)
    priority = manhattan_distance + g_n_value
    return priority

# step-5 defining a successor_states() function which is core of this agent

# This valid moves list helps in detecting all the possible moves for '0' based on its position in the current state
valid_moves = [["RD", "LRD", "LD"],
               ["URD", "URDL", "ULD"],
               ["UR", "URL", "UL"]]

def successor_states():
    successor_states = []
    successor_directions = []
    successor_g_n = []
    solution = []
    # seen_states = set()

    # While open_list has an element, we pop a state with highest priority and move forward in that direction.
    while open_list:
        pop_state = heapq.heappop(open_list) #when open_list has a state, we pop a state with highest priority
        state, direction, g_n = pop_state[1], pop_state[2], pop_state[3]
        cost = g_n                           #This is to keep track of number of steps taken so that we can calculate the priority in the manhattan_distance() function
        
        if direction != "i":                  #This displays the path flow of states
            print(f"Move: {cost} - Next move in {direction} direction")
            print(*state, sep="\n")

        solution.append(direction)
        if state == goal_state:                 #if we pop a state which is equal to goal state, we return the solution
            return (f"Number of steps: {cost}, Path direction: {solution[1:]}")
        else:                                   #else we move on to find the successor states and this is repeated until we find the goal state
            indexOf0 = getindex(state, 0) 
            cost += 1
            for i in valid_moves[indexOf0[0]][indexOf0[1]]: #for each valid move direction 
                current_state = copy.deepcopy(state)        #we are using deepcopy to create a duplicate of current state in order to not effect the actual state while processing
                
                # For each valid move of '0' based on valid_moves list, we perform the below operations
                if i == "U":
                    prev_value = current_state[indexOf0[0]-1][indexOf0[1]]
                    current_state[indexOf0[0]-1][indexOf0[1]] = 0
                    current_state[indexOf0[0]][indexOf0[1]] = prev_value

                elif i == "R":
                    # print("R")
                    prev_value = current_state[indexOf0[0]][indexOf0[1]+1]
                    current_state[indexOf0[0]][indexOf0[1]+1] = 0
                    current_state[indexOf0[0]][indexOf0[1]] = prev_value

                elif i == "D":
                    # print("D")
                    prev_value = current_state[indexOf0[0]+1][indexOf0[1]]
                    current_state[indexOf0[0]+1][indexOf0[1]] = 0
                    current_state[indexOf0[0]][indexOf0[1]] = prev_value
                
                elif i == "L":
                    # print("L")
                    prev_value = current_state[indexOf0[0]][indexOf0[1]-1]
                    current_state[indexOf0[0]][indexOf0[1]-1] = 0
                    current_state[indexOf0[0]][indexOf0[1]] = prev_value

                # The below steps are taken inorder to avoid coming across duplicate states - push the modified state to open_list only if our agent has not seen it before
                if str(current_state) not in seen_states:
                    successor_states.append(current_state)
                    successor_directions.append(i)
                    successor_g_n.append(cost)
                    heapq.heappush(open_list, (calculate_priority(current_state, cost), current_state, i, cost))
                    seen_states.add(str(current_state))
    # if the open_list becomes empty and we still did not find the goal state, then we return failure
    return "Failure"
print(successor_states())