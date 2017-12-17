#!/usr/bin/env python3
'''
genetic algorithms solving the MTSP question in Question 1
touched on Sat Dec 16
Yimin Gu
'''
from random import *
from math import *

cities = 66     #all 66 cities
travelers = 14  #all 14 travelers
T = 200     #generations
N = 100     #population

pc = 0.8    #crossover probability
pm = 0.1    #mutation probability

class individual:
    def __init__(self):
        #fitness of each individual
        self.fitness = 0
        #the chromosomes -- S
        #   a three-dimension array
        #each individual from the population:
        #each traveler -- S_i: S_1 to S_travelers
        #   m-bit non-negative integer number(m means cities)
        #       S_i_1 to S_i_m
        #   each digit not larger than m
        #S_i_j = k:traveler i goto city k in the j-th step globally
        #S_i_j = 0:traveler i don't move in the j-th step globally
        #note that S_*_j only has only one non-zero value while *
        #goes from 1 to traveler
        #
        #using this method is easier to program
        self.chrm = [['\0' for k in range(cities)] for i in range(travelers)] 


#the population and popnew for temp storage
population = [individual() for i in range(N)]
popnew = [individual() for i in range(N)]

def initialize():
    pass

def calc_fitness():
    pass

#linear ranking selection
#probability of individual i: 
#p[i]=(a-b/(n+1))/n
#n is ranking
#a and b are constants 1<=a<=2, always 1.1, b=2a-2
def select():
    global population
    global popnew
    #sort
    population = sorted(population, key = lambda x: x.fitness)
    p = [0 for i in range(N)]
    selection = [0.0 for i in range(N)]
    pall = 0
    #get probability of each individual and total probability
    a = 1.1
    b = 2 * a - 2
    for i in range(N):
        n = i + 1
        p[i] = (a - b / (n + 1)) / (n)
        pall += p[i]
    #build up the selection, selection goes from smaller to larger
    for i in range(N):
        selection[i] = p[i] / pall
    for i in range(1, N):
        selection[i] += selection[i - 1]
    #choose randomly
    for i in range(N):
        #random real number from 0 to 1
        rand = random()
        idx = 0
        while rand > selection[idx]:
            idx += 1
        popnew[i] = population[idx]
    #copy
    for i in range(N):
        population[i] = popnew[i]

def crossover():
    pass

def mutation():
    pass

#begin of main
initialize()
#main loop
for t in range(T):
    calc_fitness()
    select()
    crossover()
    mutation()


