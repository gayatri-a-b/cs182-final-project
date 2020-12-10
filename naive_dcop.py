# NAIVE DCOP ALGORITHM CLASS
# finds the most optimized assignment based on an algorithm that randomly assigns students to verices
import numpy

class Naive:

    # constructor for the Naive class
    def __init__(self, desks, cooperation, happiness, sadness):
        # save parameters to attributes
        self._graph = desks
        self._constraints = cooperation
        self._cost = sadness
        self._reward = happiness

        self._number_students = len(self._graph)

    # create the random assignment once
    # this method just randomly assigns students to desks
    # (so all the vertices simultaneously choose which student they want to seated at that desk)
    def _random_assignment(self, seed = 5):

        # create an array with all the students
        random_assignment = [*range(self._number_students)]

        # shuffle the array so that 
        numpy.random.shuffle(random_assignment)

        return random_assignment

    # check the satisfaction of that random assignment
    def satisfaction_check(self, seed = 5):
        numpy.random.seed(seed)
        arrangement = self._random_assignment(seed = seed)

        utility = 0

        # this double for loop lets us check every edge
        # we double count, so (a, b) and (b, a) are both checked
        for i in range(self._number_students):
            assigned_student = arrangement[i]

            for j in range(self._number_students):
                connected_student = arrangement[j]

                # check if there is an edge between the two students
                edge = self._graph[i][j]

                # if there is an edge
                if edge:
                    # if that edge is a violation, pay a cost
                    if (assigned_student, connected_student) in self._constraints:
                        utility -= self._cost
                    # if there is no violation, get a reward
                    else:
                        utility += self._reward
                # if there is no edge, get a reward               
                else:
                        utility += self._reward
        
        # return the total utilty of the assignment
        # return the assignment
        return ((arrangement, utility))

        
                