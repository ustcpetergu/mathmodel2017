#!/usr/bin/env python3
'''
Floyd algorithm: shortest path between each two nodes
input from data.txt, and output result to data2.txt
2017/12/16
'''
num = 65 + 1
#0 - 65 destinations

dist = [[0 for col in range(num)] for row in range(num)]
#init the distance matrix

fin = open("./data.txt", "r")
fout = open("data2.txt", "w")
for i in range(num):
    data = fin.readline()
    dist[i] = [float(j) for j in data.split()]
for i in range(num):
    for j in range(num):
        if i < j:
            dist[j][i] = dist[i][j]
for k in range(num):
    for i in range(num):
        for j in range(num):
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][k] + dist[k][j] < dist[i][j]
for i in dist:
    for j in i:
        fout.write(str(j) + ' ')
    fout.write('\n')
fin.close()
fout.close()

