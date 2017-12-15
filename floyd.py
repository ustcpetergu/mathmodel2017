#!/usr/bin/env python3

num = 65 + 1
dist = [[0 for col in range(num)] for row in range(num)]

fin = open("./data.txt", "r")
for i in range(num):
    data = fin.readline()
    dist[i] = [float(j) for j in data.split()]


print(dist)

fin.close()

