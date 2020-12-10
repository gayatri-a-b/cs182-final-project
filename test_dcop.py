# TEST METHODS
import numpy
import timeit
import test_graph
import undirected_graph as UD
import naive_dcop
import abt_dcop


## GENERATE GRAPHS
# random graph generator
# takes in a number of students and edge probability that there is conflict
def random_test_graph(num_students = 25, edge_probability = [0.7, 0.3]):
    # create a test graph 
    t = test_graph.Test_Graph(num_students, edge_probability)
    UD.graph(t.get_test())

    # get the adjacency matrix
    t_adj = t.adjMatrix()

    # return the randomly created test graph
    return t_adj

# grid graph generator
# takes in a number of rows and students in each row to generate a grid graph
def grid_layout(num_rows = 4, students_per_row = 5):
    # find the total number of students
    num_students = num_rows * students_per_row

    # empty adjacency matrix
    t_adj = numpy.zeros((num_students, num_students))

    # figure out the edges for each desk
    for desk in range(num_students):
        # find the numbers of the desks adjacent
        left = desk - 1
        right = desk + 1
        up = desk - students_per_row
        down = desk + students_per_row

        # if the desk is on the right or left, it cannot have an edge on the other side
        if desk % students_per_row == 0:
            left = -10
        elif (desk + 1) % students_per_row == 0:
            right = -10

        # keep the possible neighbors in an array
        neighbors = [left, right, up, down]

        # in another array these will be the valid desk neighbors
        kept_neighbors = []

        # check if the neighbor is valid
        for neighbor in neighbors:
            if neighbor in range(num_students):
                kept_neighbors.append(neighbor)

        # add the edge if it is a valid neighbor desk
        for neighbor in kept_neighbors:
            t_adj[desk][neighbor] = 1

    # return the grid test graph
    return t_adj
    
def cluster_layout(num_clusters = 4, students_per_cluser = 5):
    # find the total number of students
    num_students = num_clusters * students_per_cluser

    # empty adjacency matrix
    t_adj = numpy.zeros((num_students, num_students))

    # work on edges for each cluster
    for cluster in range(num_clusters):
        # find the numbers of the desks in that cluser
        cluster_desks = [cluster*5 + 0, cluster*5 + 1, cluster*5 + 2, cluster*5 + 3, cluster*5 + 4]

        # double for loop makes sure we add edges for (a, b) and (b, a)
        # for each desk in the cluster, clique so fully connected
        for desk_i in cluster_desks:
            for desk_j in cluster_desks:
                if desk_i != desk_j:
                    t_adj[desk_i][desk_j] = 1

    # return the cluster test graph              
    return t_adj

# randomly generate constraints for any group of students
# this is how we come up with which students cannot sit with whcih other students
# takes in a number of students and a probability that they [do, don't] cooperate with each other
def random_constraints(num_students = 25, cooperation = [0.9, 0.1], seed = 10):
    # empty array to save the constraint tuples
    constraints = []

    # seed the random
    numpy.random.seed(seed)

    # double for loop ensures we only loop exactly once per possible tuple, so (a, b) but not (b, a) for b > a
    for i in range(num_students):
        for j in range(i+1, num_students):
            # decide whether there is a conflict randomly
            x = numpy.random.choice(2, 1, p=cooperation)[0]
            
            # if there is a conflict then add it to the conflict array
            if x:
                constraints.append((i,j))

    # return our list of tuples of students which represent a mutual conflict between student (a, b)
    return constraints

# count the number of violations in the best assignment
def violation_counter(graph, assignment, constraints):
    violations = 0

    for i in range(len(assignment)):
        assigned_student = assignment[i]

        for j in range(len(assignment)):
            connected_student = assignment[j]

            # check if there is an edge between the two students
            edge = graph[i][j]

            # if there is an edge
            if edge:
                # if that edge is a violation, count it
                if (assigned_student, connected_student) in constraints:
                    violations += 1

    return violations


## RUN SIMULATIONS
# simulate iterations trials of the naive dcop on a given graph
def simulate_naive(num_students, desks, cooperation, happiness, sadness, iterations, seed = 3, abt_simulation = None):
    # save the assignments
    assignments = []

    # save the utilities
    utilities = []

    # save the constraints
    constraints = []

    # save the runtimes
    runtimes = []

    # save the violations
    violations = []

    # for each iteration of the naive algorithm
    for i in range(iterations):
        print("iteration ", i)
        # get constraints
        constraint = random_constraints(num_students = num_students, cooperation = cooperation, seed = seed)

        # make a naive dcop object
        n_dcop = naive_dcop.Naive(desks, constraints, happiness, sadness)

        ## time the algorithm execution
        start = timeit.default_timer()

        # run the naive algorithm
        (assignment, utility) = n_dcop.satisfaction_check(seed = seed)

        ## time the algorithm execution
        stop = timeit.default_timer()
        
        # get the violations
        violation = violation_counter(desks, assignment, constraint)

        # save assignment and utility for this particular trial
        assignments.append(assignment)
        utilities.append(utility)

        # save the constraint
        constraints.append(constraint)

        # save the runtime
        runtimes.append(stop - start)

        # save the violation
        violations.append(violation)

        # increment the seed
        seed += 15

    # return a tuple of assignments and utilities from many trials of the algorithm
    return (assignments, utilities, constraints, runtimes, violations)

# simulate iterations trials of the abt dcop on a given graph
def simulate_abt(num_students, desks, cooperation, happiness, sadness, iterations, seed = 3, abt_simulation = 20000):
    # save the assignments
    assignments = []

    # save the utilities
    utilities = []

    # save the constraints
    constraints = []

    # save the runtimes
    runtimes = []

    # save the violations
    violations = []

    # for each iteration of the abt algorithm
    for i in range(iterations):
        print("iteration ", i)
        # get constraints
        constraint = random_constraints(num_students = num_students, cooperation = cooperation, seed = seed)

        # make an abt object
        a_dcop = abt_dcop.ABT(desks, constraint, happiness, sadness)

        ## time the algorithm execution
        start = timeit.default_timer()

        # run the abt algorithm
        (assignment, utility) = a_dcop.satisfaction_check(iterations = abt_simulation)

        ## time the algorithm execution
        stop = timeit.default_timer()

        # get the violations
        violation = violation_counter(desks, assignment, constraint)

        # save assignment and utility for this particular trial
        assignments.append(assignment)
        utilities.append(utility)
        
        # save the constraint
        constraints.append(constraint)

        # save the runtime
        runtimes.append(stop - start)

        # save the violation
        violations.append(violation)

        seed += 15

    # return a tuple of assignments and utilities from many trials of the algorithm
    return (assignments, utilities, constraints, runtimes, violations)

# find the best assignment for any  type of algorithm
def best_assignment(num_students, desks, cooperation, happiness, sadness, iterations, test_function, seed = 3, abt_simulation = 20000):
    # call the test function
    (assignments, utilities, constraints, runtimes, violations) = test_function(num_students, desks, cooperation, happiness, sadness, iterations, seed = seed, abt_simulation = abt_simulation)

    # find the maximum utility
    max_utility = max(utilities)

    # get the indices of the best utilities
    best_utilities = [i for i, j in enumerate(utilities) if j == max_utility]

    # save the seating charts
    best_assignments = []

    # save the constraints
    best_constraints = []

    # save the runtimes
    best_runtimes = []

    # save the violations
    best_violations = []

    # save all the best assignments
    for index in best_utilities:
        best_assignments.append(assignments[index])
        best_constraints.append(constraints[index])
        best_runtimes.append(runtimes[index])
        best_violations.append(violations[index])

    # return the best assignments and its utility
    return (best_assignments, max_utility, best_constraints, best_runtimes, best_violations)
                    
# get the overall best run, defined by the lowest violation/constraints ratio for all with same utiltiy
def overall_best(best_assignments, best_constraints, best_runtimes, best_violations):
    ratios = []
    
    number_constraints = [len(i) for i in best_constraints]

    for i in range(len(best_assignments)):
        num_violations = best_violations[i]
        num_constraints = number_constraints[i]

        if num_constraints == 0:
            ratios.append(0) 
        else:
            ratios.append(num_violations / num_constraints)

    min_ratio_index = ratios.index(min(ratios))

    overall_best_assignment = best_assignments[min_ratio_index]
    overall_best_ratio = ratios[min_ratio_index]
    overall_best_constraints = best_constraints[min_ratio_index]
    overall_best_runtime = best_runtimes[min_ratio_index]

    return (overall_best_assignment, overall_best_constraints, overall_best_runtime, overall_best_ratio)
