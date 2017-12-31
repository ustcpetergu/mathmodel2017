#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
Math modeling
genetic algorithms solving the MTSP question in Question 1
touched on Sat Dec 16
Yimin Gu
I'm quite not sure about the time windows......
Just have a tryyyy..........
'''
from random import *
from math import *
import sys
import copy

realcity = 66   #66 real cities(but I use singular form to have a difference)
cities = 71     #all 71 cities, including 5 virtual cities
travelers = 14  #all 14 travelers
T = 10        #generations
N = 100         #population

pc = 0.2        #crossover probability
                #NOTE: is not REAL crossover, so probability is small
pm = 0.4        #mutation probability

#mapping from cities(including virtual cities) to real city
cities2realcity = [0 for i in range(cities)]

#distances from one real city to another, read from floyd.py
dist = [[0 for col in range(realcity)] for row in range(realcity)]

#weight of each delivering task
weight = [0 for i in range(cities)]
#max weight of each car
maxweight = 14.0

speed = 60
#installation time of each city, in question 1, all is same.
#I'll take the average value, 1.1 hours, and exchange time to distance
#with speed 60km/h
#speed will be multiplied when initialization
installtimelength = [1.1 for i in range(cities)]
#the start point 0 don't need install time
installtimelength[0] = 0
#the time window
timewindow = [0 for i in range(cities)]
#punish for late, add 999km for an hour's late
punish = 999

class individual:
    #init with a random route for each individual
    def __init__(self):
        #fitness of each individual, smaller is better
        #fitness is the biggest length of the 14 travelers
        #fitness2 is total length
        self.fitness = 999999
        self.fitness2 = 999999
        #0 means non timeout, 1 means timed-out
        self.istimeout = 1
        #departure time of each travelers in individual
        self.timedep = [0 for i in range(travelers)]
        #the chromosomes -- S
        #each individual from the population:
        #each traveler -- S_i: S_1 to S_travelers
        #   m-bit non-negative integer number(m means cities)
        #       S_i_1 to S_i_m
        #   each digit not larger than m
        #S_i_j = k:traveler i goto city k in the j-th step globally
        #S_i_j = 0:traveler i don't move in the j-th step globally
        #note that S_*_j only has only one non-zero value while *
        #goes from 1 to traveler
        #NOTE: actually only m-1 is needed, but use m is easier for programming
        #it has caused troubles, but I'm too lazy to fix that
        self.chrm = [[0 for i in range(cities)] for j in range(travelers)] 
        #NOTE: chrm will be inited in initialization function
        # t = [x for x in range(cities)]
        # #sort by timewindow to get better possibility
        # #NOTE: non-zero values in chrm[x][] (let's call it cityseq[]), 
        # #timewindow[cityseq] is a monotone up sequence
        # t = sorted(t, key = lambda x:timewindow[x])
        # # print("init:", t)
        # for i in range(cities):
            # self.chrm[randint(0, travelers - 1)][i] = t[i]

M = 25
#M best individual in-history to make selection better
bestindi = [individual() for i in range(M)]

#global minimum distance
mindistance = 999999.99 #save this only to be able to use calc_fitness
mindistancenow = 999999.99
mindistancetotalnow = 999999.99

mindistancehistory = 999999.99
mindistancetotalhistory = 999999.99
minindividualhistory = individual()

#the population and popnew for temp storage
population = [individual() for i in range(N)]
popnew = [individual() for i in range(N)]

#this cannot make sure ok, but some kind of reasonable
def initindi(indi):
    t = [x for x in range(1, cities)]
    t = sorted(t, key = lambda x:timewindow[x])
    # print([timewindow[x] for x in t])
    for j in range(cities - 1):
        oklist = []
        for k in range(travelers):
            if indi.chrm[k][0] == 0:
                oklist.append(k)
            else:
                l = 0
                while indi.chrm[k][l]:
                    l += 1
                l -= 1
                if timewindow[indi.chrm[k][l]] + 0.5 + installtimelength[indi.chrm[k][l]] / speed + \
                        dist[cities2realcity[indi.chrm[k][l]]][cities2realcity[t[j]]] / speed <= timewindow[t[j]] + 0.5:
                    oklist.append(k)
        # print(oklist)
        #failed, again
        if oklist == []:
            # print("#######")
            # print('---')
            # printchrm(indi)
            # print('---')
            indi.chrm = [[0 for n in range(cities)] for m in range(travelers)] 
            return initindi(indi)
        pos = sample(oklist, 1)
        l = 0
        if indi.chrm[pos[0]][0] == 0:
            l = -1
        else:
            while indi.chrm[pos[0]][l]:
                l += 1
            l -= 1
        indi.chrm[pos[0]][l + 1] = t[j]
    # print("*******")
    # print('---')
    # printtime(indi)
    # print('---')
    return indi

def initialize():
    if len(sys.argv) == 2:
        if sys.argv[1] != "-q":
            print("initialize...")
    #read destdata.txt to get 
    global weight
    global cities2realcity
    global timewindow
    fin1 = open("destdata.txt", "r")
    for i in range(cities):
        # (cities2realcity[i], installtimelength[i], weight[i]) = fin1.readline()
        (cities2realcity[i], nouse, weight[i], timewindow[i]) = fin1.readline().split()
    for i in range(cities):
        cities2realcity[i] = int(cities2realcity[i])
        weight[i] = float(weight[i])
        installtimelength[i] = speed * (float(installtimelength[i]))
        hour, minute = timewindow[i].split(':')
        timewindow[i] = round(int(hour) + float(int(minute)/60), 3)
    fin1.close()
    #read data2.txt containing shortest path generated by floyd.py
    global dist
    fin = open("data2.txt", "r")
    for i in range(realcity):
        data = fin.readline()
        dist[i] = [float(j) for j in data.split()]
    fin.close()
    #now init chrms in in population
    #a inited individual will be in time limit
    for i in range(N):
        population[i] = initindi(population[i])

#calculate the fitness of each individual #2, improved
def calc_fitness2():
    global mindistancenow
    global mindistancetotalnow
    global mindistancetotalhistory
    global mindistancehistory
    global minindividualhistory
    if len(sys.argv) == 2:
        if sys.argv[1] != "-q":
            print("calculate fitness #2...")
    mindistancenow = 999999
    for i in range(N):
        population[i].istimeout = 0
        mindistancetotalnow = 0
        mindistancenowt = -1
        for j in range(travelers):
            length = 0
            weightnow = 0
            time = 0
            #start from city 0
            citynow = 0
            for k in range(cities):
                citynext = population[i].chrm[j][k]
                if citynext != 0:
                    #the first city's time tells when to departure
                    if time == 0:
                        time = population[i].timedep[j] = \
                                timewindow[citynext] - dist[cities2realcity[citynow]][cities2realcity[citynext]] / speed
                    time += dist[cities2realcity[citynow]][cities2realcity[citynext]] / speed
                    #have to wait
                    if time < timewindow[citynext]:
                        length += (timewindow[citynext] - time) * speed
                        time = timewindow[citynext]
                    #late, be punished
                    elif time > timewindow[citynext] + 0.5:
                        #to make it a dead individual
                        weightnow = 999
                        break
                        # print("time out!")
                        # length += (time - timewindow[citynext] - 0.5) * punish
                        #a timed out individual
                        # population[i].istimeout = 1
                    else:
                        pass
                    length += dist[cities2realcity[citynow]][cities2realcity[citynext]]
                    mindistancetotalnow += dist[cities2realcity[citynow]][cities2realcity[citynext]]
                    citynow = citynext
                    #"mindistancenow" at-install
                    length += installtimelength[citynow]
                    mindistancetotalnow += installtimelength[citynow]
                    time += installtimelength[citynow] / speed
                    weightnow += weight[citynow]
            #overload?
            if weightnow > maxweight:
                #just replace the individual and calc again
                #until all is OK
                #to get better result
                population[i] = initindi(individual())
                j -= 1
                continue;
            #go back to city 0
            length += dist[cities2realcity[citynow]][0]
            mindistancetotalnow += dist[cities2realcity[citynow]][0]
            mindistancenowt = max(length, mindistancenowt)
        mindistancenow = min(mindistancenow, mindistancenowt)
        population[i].fitness = mindistancenowt
        population[i].fitness2 = mindistancetotalnow
        #update history
        if population[i].istimeout == 0 and mindistancenow < mindistancehistory:
            mindistancehistory = mindistancenow
            minindividualhistory = copy.deepcopy(population[i])
        mindistancetotalhistory = min(mindistancetotalhistory, mindistancetotalnow)

#improved tournament selection
#to keep the best individuals in history always be used
def select2_2():
    if sys.argv == 2:
        if sys.argv[1] != "-q":
            print("select...")
    global population
    global popnew
    global bestindi
    #non-time-out individual is best
    population = sorted(population, key = lambda x:(x.istimeout, x.fitness, x.fitness2))
    poptmp = [x for x in bestindi + population[:M]]
    poptmp = sorted(poptmp, key = lambda x:(x.istimeout, x.fitness, x.fitness2))
    bestindi = [copy.deepcopy(x) for x in poptmp[:M]]
    print([int(x.fitness) for x in bestindi])
    print([x.istimeout for x in bestindi])
    for i in range(N):
        popt = sorted([population[randint(0, N - 1)], population[randint(0, N - 1)]], key = lambda x:(x.istimeout, x.fitness, x.fitness2))
        popnew[i] = popt[0]
    population = sorted(population, key = lambda x:(x.istimeout, x.fitness, x.fitness2))
    population = popnew
    population = population[:-M] + [copy.deepcopy(x) for x in bestindi]

#input a individual's chromosome
#return striped(without zeros, a one-dimension array) chrm
def strip(chrm):
    return [sum(chrm[j][i] for j in range(travelers)) for i in range(cities)]
#input a striped chromosome and the individual's original chromosome
#return expanded chrm
def expand(schrm, chrm):
    #all these verbose code is cause by <m or m-1> problem!
    #(see defination of individual and chrm for more info)
    schrm = [x for x in schrm if x]
    flag = 0
    for i in range(cities):
        for j in range(travelers):
            if chrm[j][i] != 0:
                t = schrm[flag]
                chrm[j][i] = t
                flag += 1
                break
    return chrm
#check if a chrm is OK, for debug use
def chrmck(chrm):
    h = [0 for i in range(cities)]
    for j in range(cities):
        t = 0
        for i in range(travelers):
            if chrm[i][j] != 0:
                h[chrm[i][j]] += 1
                t += 1
        if t > 1:
            print("No")
            return -1
    for i in range(1, cities):
        if h[i] != 1:
            print("No")
            return -1
    print("Yes")
    return 1
#to make the time of individual better, sort the chrm
def sortchrm(indi):
    for i in range(travelers):
        t = sorted([x for x in indi.chrm[i] if x])
        flag = 0
        for j in range(cities):
            if indi.chrm[i][j]:
                indi.chrm[i][j] = t[flag]
                flag += 1
    return indi
#print chrm
def printchrm(indi):
    for i in range(travelers):
        print(str([cities2realcity[indi.chrm[i][x]] for x in range(cities) if indi.chrm[i][x]]))
    print('')
def printtime(indi):
    for i in range(travelers):
        print(str([timewindow[indi.chrm[i][x]] for x in range(cities) if indi.chrm[i][x]]))
    print('')
def crossover():
    #NEW crossover (may be a VERY BAD one) written by ME
    if len(sys.argv) == 2:
        if sys.argv[1] != "-q":
            print("crossover...")
    # h = [i for i in range(N)]
    # shuffle(h)
    # for i in range(int((N - 1) / 2)):
        # if random() < pc:
    for i in range(N):
        h = [j for j in range(travelers)]
        shuffle(h)
        for j in range(int((travelers) / 2) - 1):
            if random() < pc:
                # print("a crossover....")
                #crossover(or change?) population[i].chrm[h[j]] and population[i].chrm[h[N - j - 1]]
                # print(h[j], h[N - j - 1])
                # print(j, travelers - j - 1)
                # print('--before--')
                # print(population[i].chrm[h[j]])
                # print(population[i].chrm[h[travelers - j - 1]])
                bak1 = copy.deepcopy(population[i].chrm[h[j]])
                bak2 = copy.deepcopy(population[i].chrm[h[travelers - j - 1]])
                citypool = [x for x in population[i].chrm[h[j]] + population[i].chrm[h[travelers - j - 1]] if x]
                citypool = sorted(citypool, key = lambda x:timewindow[x])
                population[i].chrm[h[j]] = [0 for x in range(cities)]
                population[i].chrm[h[travelers - j - 1]] = [0 for x in range(cities)]
                # print([timewindow[x] for x in t])
                #some kind of hard-coding and repeat code I think
                for k in range(len(citypool)):
                    oklist = []
                    for m in (h[j], h[travelers - j - 1]):
                        if population[i].chrm[m][0] == 0:
                            oklist.append(m)
                        else:
                            l = 0
                            while population[i].chrm[m][l]:
                                l += 1
                            l -= 1
                            if timewindow[population[i].chrm[m][l]] + 0.5 + installtimelength[population[i].chrm[m][l]] / speed + dist[cities2realcity[population[i].chrm[m][l]]][cities2realcity[citypool[k]]] / speed <= timewindow[citypool[k]] + 0.5:
                                oklist.append(m)
                    # print(oklist)
                    #failed, reset
                    if oklist == []:
                        population[i].chrm[h[j]] = bak1
                        population[i].chrm[h[travelers - j - 1]] = bak2
                        break
                    pos = sample(oklist, 1)
                    l = 0
                    if population[i].chrm[pos[0]][0] == 0:
                        l = -1
                    else:
                        while population[i].chrm[pos[0]][l]:
                            l += 1
                        l -= 1
                    population[i].chrm[pos[0]][l + 1] = citypool[k]
                # print('--after--')
                # print(population[i].chrm[h[j]])
                # print(j)
                # print(travelers - j - 1)
                # print(population[i].chrm[h[travelers - j - 1]])
                # print('--crossover end')
                # #bad move
                # if population[i].chrm[h[j]] == [] or population[i].chrm[h[travelers - j - 1]] == []:
                    # population[i].chrm[h[j]] = bak1
                    # population[i].chrm[h[N - j - 1]] = bak2
                    # j -= 1
                    # break

def print_result():
    maxi = 0
    for i in range(N):
        if population[i].fitness < population[maxi].fitness:
            maxi = i
    print("Min distance in history:", round(mindistancehistory, 5))
    print("Min distance total in history:", round(mindistancetotalhistory, 5), "time out:", minindividualhistory.istimeout)
    for i in range(travelers):
        print("traveler ", i, ":")
        print([cities2realcity[minindividualhistory.chrm[i][x]] for x in range(cities) if minindividualhistory.chrm[i][x]])
    fout = open("ans.txt", "a")
    fout.write('-----')
    fout.write('\n')
    fout.write("Min distance in history:" + str(round(minindividualhistory.fitness, 5)) + \
            "time out:" + str(minindividualhistory.istimeout))
    fout.write('\n')
    fout.write("Min distance total:" + str(round(minindividualhistory.fitness2, 5)))
    fout.write('\n')
    for i in range(travelers):
        fout.write("traveler " + str(i))
        fout.write('\n')
        fout.write("\tdep. time:" + str(round(minindividualhistory.timedep[i])) + str((round((minindividualhistory.timedep[i] - int(minindividualhistory.timedep[i])) * 60))))
        fout.write('\n')
        fout.write(str([cities2realcity[minindividualhistory.chrm[i][x]] for x in range(cities) if minindividualhistory.chrm[i][x]]))
        fout.write('\n')
    fout.write('-----')
    fout.write('\n\n')
def printmsg():
    if len(sys.argv) == 2:
        if sys.argv[1] == "-q":
            print(str(round(mindistancenow, 5)))
    else:
        print("Generation " + str(t))
        print("Min distance: " + str(round(mindistancenow, 5)))
        print("Min mindistance total:" + str(round(mindistancetotalnow, 5)))
        print("Timed out?", str(minindividualhistory.istimeout))

#begin of main
initialize()
# printchrm(minindividualhistory)
#main loop
calc_fitness2()
for t in range(T):
    printmsg()
    # printchrm(minindividualhistory)
    # printchrm(population[0])
    crossover()
    calc_fitness2()
    # for i in range(N):
        # print(population[i].fitness)
        # print(population[i].istimeout)
    select2_2()
print_result()
print("end.")

