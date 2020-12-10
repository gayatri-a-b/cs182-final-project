# ASYNCH BACKTRACKING DCOP ALGORITHM CLASS
import numpy

class ABT:

    # constructor
    def __init__(self, desks, cooperation, happiness, sadness):
        # save the parameters as attributes of the instance
        self._graph = desks
        self._constraints = cooperation
        self._cost = sadness
        self._reward = happiness

        self._number_students = len(self._graph)

    # get the priority of seating students based on the constraints
    def _get_priority(self):
        occurances = {}

        # create an empty dictionary for all the students
        for i in range(self._number_students):
            occurances[str(i)] = 0

        # each time we see a student in the constraints, increment the dictionary element for that student
        for (a, b) in self._constraints:
            occurances[str(a)] += 1
            occurances[str(b)] += 1

        # sort the dictionary most conflicted student (most priority) to least conflicted student (least priority)
        # for two students with same number of conflicts, lower number student gets priority
        priority = [(k, occurances[k]) for k in sorted(occurances, key=occurances.get, reverse=True)]

        return priority

    # naive backtracking computation
    # bases on number of iterations to prevent a case where these is no termination
    def _abt(self, iterations = 3000):
        # seating arrangement that we are going to keep
        keep_seating = []

        # get the student priority that we will initialize the seat assignment
        priority = self._get_priority()

        # keep track of the previous seating arrangement and the current seating arrangement
        previous_seating = []
        seating = [None]*self._number_students
        
        # keep track of the students we have added
        students_added = []
        
        # keep track of no goods assignments in a dictioary
        not_allowed = {}

        # initialize the dictionary to completely empty arrays for each student
        for i in range(self._number_students):
            not_allowed[str(i)] = []

        # keep track of iterations as a naive way to prevent no termination
        prevent_forever = 0

        # initialize the student index tracker
        j = 0

        # index to keep track of only the arrangements with the fewest number of assigned students (aka best solutions)
        min_none = self._number_students

        # make sure we don't stop searching
        if iterations < self._number_students:
            iterations += self._number_students

        # loop through both all the students and while our loop doesn't go forever
        while j < self._number_students and prevent_forever < iterations:
            # get the student we are seating's priority (it's a sting so we convert to int)
            (student, _) = priority[j]
            student = int(student)
            
            # keep track of the seats we have not assigned anyone
            free_seats = [i for i,v in enumerate(seating) if v == None]

            # keep track of which students have higher priorities
            higher_priorities = seating[slice(0, free_seats[0])]
            
            # index to keep track of when we get a no good
            no_good = True

            # index to keep track of the seat index
            seat_index = 0

            # while we have a no good
            while no_good:
                # if the seat index is a number of free seats (so incremented too far and not a possible index)
                if seat_index == len(free_seats):
                    break

                # check whether we have a no good
                no_good = self._check_nogood(student, free_seats[seat_index], seating, higher_priorities, not_allowed)
                
                # if we have a no good, try to place in the next possible seat
                if no_good:
                    seat_index += 1

            # if we still have no good but have tried all the other seats, we need to backtrack
            # we need to re-place the previous student and then come back to this student
            if no_good == True:
                # figure out who the previous student was
                prev_student = students_added.pop()

                # add to the previous student that they cannot be placed in the seat that they just were
                not_allowed[str(prev_student)].append(seating.index(prev_student))
                
                # change the list of places that this student cannot sit
                not_allowed[str(student)] = []

                # get the previous seating arrangement
                previous_seat = previous_seating.pop()
                
                # set the current seating arrangement as the former
                seating = previous_seat

                # now consider placing the previous student by decrementing the index
                j -= 1
            
            # if we are good
            else:
                # say that we have placed this student
                students_added.append(student)

                # add this arrangment to our seating history
                previous_seating.append(seating[:])

                # seat our student
                seating[free_seats[seat_index]] = student
                
                # and consider our next student
                j += 1

            # increment our index to prevent a forever loop
            prevent_forever += 1

            # don't keep track of the first five seating arrangments, but check to keep everything else
            if prevent_forever > (self._number_students - 4):
                # find how many nones there are
                num_none = sum(x is None for x in seating)

                # if this is the minimal number of nones then keep track of the arrangment
                if num_none <= min_none:
                    keep_seating.append(seating)

            #print(seating)

        # return the seating arrangments we found most optimal
        return keep_seating

    # figure out where to place a given student (whether it is good or no good)
    def _check_nogood(self, student, seat, seating, higher_priorities, not_allowed):
        # if we can't place the student there base on the places that student cannot be placed, no good
        if seat in not_allowed[str(student)]:
            return True

        # check if conflicts with higher priority students
        for higher_prir_stu in higher_priorities:
            # get where the higher priority student is sitting
            higher_prir_stu_seating = seating.index(higher_prir_stu)

            # if the constraint exists in constraints
            if (higher_prir_stu, student) or (student, higher_prir_stu) in self._constraints:
                
                # if the edge exists, we have a no good
                if self._graph[higher_prir_stu_seating][seat] == 1:
                    return True
            # otherwise we have found a valid assignment and we are good
            else:
                return False
        

    # check the satisfaction of that random assignment
    def satisfaction_check(self, iterations = 40000):
        # get all the maximal arrangements from the backtracking algorithm
        arrangements = self._abt(iterations = iterations)
        f_arrangements = []

        # create  a list of all students
        all_students = [i for i in range(0, self._number_students)]

        # fill arrangments that never made it all the way
        for arrangement in arrangements:
            missing_elms = [ele for ele in all_students if ele not in arrangement]
    
            original_arr = arrangement.copy()

            for elm in missing_elms:
                for ind, student in enumerate(arrangement):
                    if student is None:
                        arrangement[ind] = elm

            f_arrangements.append(arrangement)

            missing_elms.reverse()

            for elm in missing_elms:
                for ind, student in enumerate(original_arr):
                    if student is None:
                        original_arr[ind] = elm

            f_arrangements.append(original_arr)
        
        # empty array to keep track of utility for each trial
        utilities = []
    
        # utility of each arrangement
        for arrangement in f_arrangements:
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

            # add the utility to our tacker
            utilities.append(utility)

        # find the index of the max utility's index
        max_utility_index = utilities.index(max(utilities))

        # reutrned the arrangment with max utility and the utility it had
        return ((f_arrangements[max_utility_index], utilities[max_utility_index]))