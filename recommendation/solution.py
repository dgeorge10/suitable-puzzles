#!/usr/bin/env python3
import sys
from heapq import nlargest 
import json
from math import *

ratings = {}
rest = {}
visited = []

#function jaccard 
#calculate the similarity index between two teammated by their ID's
#parameters- ratings, id1, id2
#ratings - the dictionary of ratings that got established in init()
#id1 - id of the teammate we are recommending for
#id2 - if of the teammate we are comparing against
def jaccard(ratings, id1, id2):
    teammate1 = ratings[id1]
    teammate2 = ratings[id2]
    #intersection of both teammates likes
    likes = set.intersection(*[set(teammate1[0]), set(teammate2[0]) ])
    #intersection of both teammates dislikes
    dislikes = set.intersection(*[set(teammate1[1]), set(teammate2[1]) ])
    #intersection of likes of teammate 1 and the dislikes of teammate 2
    ld = set.intersection(*[set(teammate1[0]), set(teammate2[1]) ])
    #intersection of dislikes of teammate 1 and the likes of teammate 2
    dl = set.intersection(*[set(teammate1[1]), set(teammate2[0]) ])
    #union of all of the ratings
    union = set.union(*[set(teammate1[0] + teammate1[1]), set(teammate2[0] + teammate2[1]) ])
    #calculate the numerator of the similarity equation
    top = (len(likes) + len(dislikes) - len(ld) - len(dl))
    #denom
    bottom = len(union)
    #return jaccard index
    return top/float(bottom)

#function init
#init is going to build a couple of data structures that are needed for this procedure
#ratings: dictionary - key is the teammate id, value is a list. 
#                      the value is a list of two lists where [0] is the list of likes and [1] is the list of dislikes
#                                   [[likes],[dislikes]]
#rest: dictionary - key is the restauraunt id, value is a list
#                   the value is a list of two lists where [0] is the list of teammates who liked that restauraunt and [1] is vice versa
#                           [[teammates who like rest], [teammates who dislike rest]]
#visited- list - list of restaurants that the 'current' teammate has already visited
#parameters current- current is the id of the teammate that we are trying to recommend for
def init(current):
    #init the ratings to be empty
    with open("../seed/out/teammates.json") as teammates:
        data = json.load(teammates)
        for row in data:
            ratings[row["id"]] = [[], []]
    #init the rest to be empty
    with open("../seed/out/restaurants.json") as restaurants:
        data = json.load(restaurants)
        for row in data:
            rest[row["id"]] = [[], []]

    #begin processing the ratings
    with open("../seed/out/ratings.json") as ratings_data:

        data = json.load(ratings_data)
        for item in data:
            #keep track of which restaurants the 'current' has already visited
            if item["teammateId"] == current:
                visited.append(item["restaurantId"])

            #if the current rating is a like, add it to ratings and rest 
            if item["rating"] == "LIKE":
                #print(ratings[item["teammateId"]])
                ratings[item["teammateId"]][0].append(item["restaurantId"]) 
                rest[item["restaurantId"]][0].append(item["teammateId"])
            #current rating is a dislike
            else:
                ratings[item["teammateId"]][1].append(item["restaurantId"]) 
                rest[item["restaurantId"]][1].append(item["teammateId"])

#function predict- this function is what is going to calculate the prediction algorithm
def predict():
    #L is going to store all of our prediction values, so we can find a max at the end of simulation
    L = {}
    for item in rest:
        #ensure that we are only proccessing restauraunts that the 'current' hasn't already visited
        if item not in visited:
            #print("restaurant id", item)

            #we need the sum of the liked and disliked jaccardian indexes

            for liked in rest[item][0]:
                sum_liked = 0
                if liked != current:
                    jac = jaccard(ratings, current, liked) 
                    sum_liked += jac

            #print("sum of liked similarities:",sum_liked)

            for disliked in rest[item][1]:
                #print(disliked)
                sum_disliked = 0
                if disliked != current:
                    jac = jaccard(ratings, current, disliked)
                    sum_disliked += jac
            #print("sum of disliked similarities:", sum_disliked)
            
            #calculate the prediction, and store it in a dict L
            top = sum_liked - sum_disliked
            bottom = len(rest[item][0]) + len(rest[item][1])
            #normalize prob by 100
            p = (100*(top/float(bottom)))
            L[item] = p

    #calculate and return what the top 3 probabilities are 
    largest = {}
    ids = nlargest(3, L, key=L.get)
    vals = sorted(L.values(), reverse=True)[:3]
    for id, value in zip(ids, vals):
        largest[id] = value

    return largest

#function get_rating - gets the rating of a restauraunt by id
def get_rating(rest_id):
    with open("../seed/out/restaurants.json") as restaurants:
        data = json.load(restaurants)
        for item in data:
            if item['id'] == rest_id:
                return item["rating"]

#function print_rest - prints a restauraunt by id
def print_rest(rest_id):
    string = ""
    with open("../seed/out/restaurants.json") as restaurants:
        data = json.load(restaurants)
        for item in data:
            if item['id'] == rest_id:
                string += "Name: " + item['name'] + "\nPrice: " + item['price'] + "\nRating:" + str(item['rating'])
    print(string)


#print_largest - prints out the top 3 matched restauraunts in descending rating order
def print_largest(largest):
    L = {}
    for item in largest:
        L[item] = get_rating(item)
    i = 1
    sortedL = sorted(L.items(), reverse=True, key=lambda kv: kv[1])
    for item in sortedL:
        print("Ranking:",i)
        print_rest(item[0])
        print()
        i+=1

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("need to supply a teammate id to suggest to!")
        sys.exit()
    elif len(sys.argv) > 2:
        print("too many arguments supplied")
        sys.exit()

    #get the user id we are interested in
    current = sys.argv[1] 
    #initialize the system
    init(current)
    #get the largest probabilities
    largest = predict()
    #print the results
    print_largest(largest)

