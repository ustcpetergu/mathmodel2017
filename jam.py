#!/usr/bin/env python3
#NOTE: run this ONLY ONCE!
#jam 10 ways
from random import *
jammed = 10
realcity = 66
dist = [[0 for col in range(realcity)] for row in range(realcity)]
fin = open("data2.txt", "r")
for i in range(realcity):
    data = fin.readline()
    dist[i] = [float(j) for j in data.split()]
fin.close()
print("sure to jam?")
print("Run this ONLY ONCE!")
print("[N/y]")
choice = input()
if choice == 'y':
    for i in range(jammed):
        x = randint(0, realcity - 1)
        y = randint(0, realcity - 1)
        #jam, distance three times!
        dist[x][y] = dist[x][y] * 3
        dist[y][x] = dist[y][x] * 3
    fout = open("data2.txt", "w")
    for i in dist:
        for j in i:
            fout.write(str(round(j, 3)) + ' ')
        fout.write('\n')
    fout.close()


