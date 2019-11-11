###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
import string

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    inFile = open(filename, 'r')    
    data_cows = {}
    for line in inFile:
        #string is immuatble so a new string must be created to remove new line character
        line = line.strip('\n')
        #split into list
        cow_data = line.split(',')
        #file is in string format, cast weight to an integer
        data_cows[cow_data[0]] = int(cow_data[-1])
    inFile.close()
    return data_cows


# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
#    #sort dictionary in decending order
#    cows_dict = cows.copy()
#    cows_sorted = {}
#    while len(cows_dict) > 0:
#        largest_cow = 0
#        for cow in cows_dict:
#            if int(cows_dict[cow]) > largest_cow:
#                largest_cow = cows_dict[cow]
#                largest_cow_name = cow
#        cows_sorted[largest_cow_name] = largest_cow
#        cows_dict.pop(largest_cow_name)
#
#    #greedy algorithm
#    trips = []
#    while len(cows_sorted) > 0:
#        total_weight = 0
#        cow_on_trip = []
#        for cow in cows_sorted:          
#            if total_weight + cows_sorted[cow] < limit:
#                total_weight += cows[cow]
#                cow_on_trip.append(cow)
#        for cow in cow_on_trip:
#             cows_sorted.pop(cow)
#        trips.append(cow_on_trip)
#    return trips


    #alternatively, sort dictionary keys using built-in sorted() function (return the cow names in a list of decending weights)
    cows_sorted =  sorted(cows, key=cows.get, reverse=True)
    trips = []
    while len(cows_sorted) > 0:
        total_weight = 0
        cow_on_trip = []
        for cow in cows_sorted:          
            if total_weight + cows[cow] < limit:
                total_weight += cows[cow]
                cow_on_trip.append(cow)
        for cow in cow_on_trip:
             cows_sorted.remove(cow)
        trips.append(cow_on_trip)
    return trips    
    


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    #set_parition captures the cow combination within the specified weight limit
    #num_trips captures the number of trip take for the acceptable cow combinations
    set_partition = []
    num_trips = []
    for trip_comb in get_partitions(cows):
        #score ensure that all trips per cow combination are within the specified weight limit
        score = 0
        for trip in trip_comb:
            total_weight = 0
            for cow in trip:
                total_weight += cows[cow]
            if total_weight > limit:
                break
            else:
                score +=1
        if score == len(trip_comb):
            set_partition.append(trip_comb)
            num_trips.append(len(trip_comb))
    fewest_trips = min(num_trips)
    for trips in set_partition:
        if len(trips) == fewest_trips:
            return trips
    
        
    
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows('ps1_cow_data.txt')     
    
    print('-------------Greedy Cow Transport Algorithm-------------')
    greedy_start = time.time()
    greedy_sol = greedy_cow_transport(cows)
    greedy_end = time.time()
    num_greedy = len(greedy_sol)
    print('Minimum number of trips：', num_greedy)
    print('Cow allocation:', greedy_sol)
    print('Time taken to execute the algorithm:', greedy_end - greedy_start)
    
    print('\n')
    print('-------------Brute Force Cow Transport Algorithm-------------')
    bf_start = time.time()
    bf_sol = brute_force_cow_transport(cows)
    bf_end = time.time()
    num_trips_bf = len(bf_sol)
    print('Minimum number of trips:', num_trips_bf)
    print('Cow allocation:', bf_sol)
    print('Time taken to execute the algorithm:', bf_end - bf_start)
    
compare_cow_transport_algorithms()