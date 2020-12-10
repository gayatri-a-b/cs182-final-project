## **USER** USE THIS FILE TO RUN THE NAIVE AND ABT ALGORITHMS
## FOLLOW THE DIRECTIONS IN THIS DOCUMENTS
import numpy
import pandas
import networkx 
import test_dcop
import matplotlib.pyplot as plt
# Note: you may need to pip install networkx to make this work

## STEP BY STEP USAGE

# 1. Initialize the variables
## All
cooperation = [0.8, 0.2]  # likelihood of cooperating, likelyhood of not getting along
number_students = 36        # number of students in the class
happiness = 4               # reward for placing students who get along side by side
sadness = -8                # reward for placing students who do not get along side by side
iterations = 5              # number of times to simulate algorithm

## ALL - Algorithm
test_function = test_dcop.simulate_naive    # test_dcop.simulate_navive or test_dcop.simulate_abt

## Random Desk graph only 
edge_probability = [0.9, 0.1]   # edge probability [exists, not exists] for random graph generator only

## Grid Desk graph only
num_rows = 6                 # number of rows for grid graph only
students_per_row = 6         # number of students per row for grid graph only

## Cluster Desk graph only
num_clusters = 6             # number of clusters for cluster graph only
students_per_cluser = 6      # number of students per cluster for cluster graph only

## ABT Algorithm only
abt_simulation = 2000           # parameter for abt algorithm only

## All - SEED
seed = 5                        # seed for numpy.random


# 2. Choose a layout
desks = test_dcop.random_test_graph(num_students = number_students, edge_probability = edge_probability)
## desks = test_dcop.grid_layout(num_rows = num_rows, students_per_row = students_per_row)
## desks = test_dcop.cluster_layout(num_clusters = num_clusters, students_per_cluser = students_per_cluser)

# 3. Get the best assignments and their max utility after running the simulation iterations number of times
## test_function can either be test_dcop.simulate_naive or test_dcop.simulate_abt
## best_assignment(num_students, desks, cooperation, happiness, sadness, iterations, test_function, seed = 3, abt_simulation = 20000)
(best_assignments, max_utility, best_constraints, best_runtimes, best_violations) = test_dcop.best_assignment(number_students, desks, cooperation, happiness, sadness, iterations, test_function, seed = seed, abt_simulation = abt_simulation)

## get the overall best assignment, defined as that with lowest num of violations / num of constraints ratio
(overall_best_assignment, overall_best_constraints, overall_best_runtime, overall_best_ratio) = test_dcop.overall_best(best_assignments, best_constraints, best_runtimes, best_violations)

## print statements to console
print("Max utility: ", max_utility)
print("Runtimes: ", overall_best_runtime)
print("Violation ratio : ", overall_best_ratio)
print("\nConstraints: ", overall_best_constraints)

## making labels, creating label mappings, to use in networkx graphing
student_labels = ["D" + str(num) + ": S" + str(student) for num, student in enumerate(overall_best_assignment)]
print("Student Assignments:\n", student_labels)
"""

"""
## OPTIONAL
# 4. Display the graph
mapping = {}
for i in range(number_students):
    mapping[i] = student_labels[i]

## graph using networkx
G = networkx.from_numpy_matrix(numpy.array(desks)) 

# RECOMMENDED (optional) - change k and iterations to change the spacing of vertices within graph
## greater k is greater spacing between vertices
## iterations is number of times it will try to reorganize the layout
pos = networkx.spring_layout(G, k = 0.2, iterations=1000)
networkx.draw(G, pos, labels=mapping)

# 5. Replace this with the name of the graph you are making
## this will save a png in the directory you are working in
plt.savefig("abt_dcop.png")
plt.show()

## clear the drawing and close the window
plt.clf()
plt.close()



## TESTS: FOR REPLICATION, RUN

"""
# TESTING STUDENT
number_studentsz = []
timez = []
ratioz = []
utilitiez = []

num_rows = 2
students_per_row = 4

for k in range(6):
    number_students = num_rows * students_per_row 
    
    desks = test_dcop.grid_layout(num_rows = num_rows, students_per_row = students_per_row)

    (best_assignments, max_utility, best_constraints, best_runtimes, best_violations) = test_dcop.best_assignment(number_students, desks, cooperation, happiness, sadness, iterations, test_function, seed = seed, abt_simulation = abt_simulation)
    (overall_best_assignment, overall_best_constraints, overall_best_runtime, overall_best_ratio) = test_dcop.overall_best(best_assignments, best_constraints, best_runtimes, best_violations)

    number_studentsz.append(number_students)
    timez.append(overall_best_runtime)
    ratioz.append(overall_best_ratio)
    utilitiez.append(max_utility)

    num_rows += 2
    students_per_row += 2

data = {'Number Students': number_studentsz, 'Runtime': timez, 'Ratio': ratioz, 'Utility': utilitiez}
df = pandas.DataFrame(data=data)

df.to_csv(r'data.csv', index = False)

print(number_studentsz)
print(timez)
print(ratioz)
print(utilitiez)
"""

"""
# TESTING ABT_SIMULATION'S ITERATIONS
abt_simulationz = [50, 100, 250, 500, 1000, 2500, 5000, 10000, 20000]
timez = []
ratioz = []
utilitiez = []

for k in abt_simulationz:
    abt_simulation = k
    
    desks = test_dcop.grid_layout(num_rows = num_rows, students_per_row = students_per_row)

    (best_assignments, max_utility, best_constraints, best_runtimes, best_violations) = test_dcop.best_assignment(number_students, desks, cooperation, happiness, sadness, iterations, test_function, seed = seed, abt_simulation = abt_simulation)
    (overall_best_assignment, overall_best_constraints, overall_best_runtime, overall_best_ratio) = test_dcop.overall_best(best_assignments, best_constraints, best_runtimes, best_violations)

    timez.append(overall_best_runtime)
    ratioz.append(overall_best_ratio)
    utilitiez.append(max_utility)

data = {'Iterations': abt_simulationz, 'Runtime': timez, 'Ratio': ratioz, 'Utility': utilitiez}
df = pandas.DataFrame(data=data)

df.to_csv(r'data.csv', index = False)

print(abt_simulationz)
print(timez)
print(ratioz)
print(utilitiez)
"""

"""
# TESTING ITERATIONS
iterationz = [50, 100, 250, 500, 1000, 2500, 5000, 10000]
timez = []
ratioz = []
utilitiez = []

for k in iterationz:
    iterations = k
    
    desks = test_dcop.grid_layout(num_rows = num_rows, students_per_row = students_per_row)

    (best_assignments, max_utility, best_constraints, best_runtimes, best_violations) = test_dcop.best_assignment(number_students, desks, cooperation, happiness, sadness, iterations, test_function, seed = seed, abt_simulation = abt_simulation)
    (overall_best_assignment, overall_best_constraints, overall_best_runtime, overall_best_ratio) = test_dcop.overall_best(best_assignments, best_constraints, best_runtimes, best_violations)

    timez.append(overall_best_runtime)
    ratioz.append(overall_best_ratio)
    utilitiez.append(max_utility)

data = {'Iterations': iterationz, 'Runtime': timez, 'Ratio': ratioz, 'Utility': utilitiez}
df = pandas.DataFrame(data=data)

df.to_csv(r'data.csv', index = False)

print(iterationz)
print(timez)
print(ratioz)
print(utilitiez)
"""


"""
# TESTING COOPERATION
a = 1.00
b = 0.00

cooperation = [a, b]

coopz = []
timez = []
ratioz = []
utilitiez = []

while a > -0.05:
    cooperation = [a, b]
    print(cooperation)
    
    desks = test_dcop.random_test_graph(num_students = number_students, edge_probability = edge_probability)

    (best_assignments, max_utility, best_constraints, best_runtimes, best_violations) = test_dcop.best_assignment(number_students, desks, cooperation, happiness, sadness, iterations, test_function, seed = seed, abt_simulation = abt_simulation)
    (overall_best_assignment, overall_best_constraints, overall_best_runtime, overall_best_ratio) = test_dcop.overall_best(best_assignments, best_constraints, best_runtimes, best_violations)

    coopz.append(cooperation)
    timez.append(overall_best_runtime)
    ratioz.append(overall_best_ratio)
    utilitiez.append(max_utility)

    a = round(a-0.05,2)
    b = round(b+0.05,2)

data = {'Cooperation': coopz, 'Runtime': timez, 'Ratio': ratioz, 'Utility': utilitiez}
df = pandas.DataFrame(data=data)

df.to_csv(r'data.csv', index = False)

print(coopz)
print(timez)
print(ratioz)
print(utilitiez)
"""
