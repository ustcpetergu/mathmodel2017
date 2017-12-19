#!/usr/bin/env python3
'''
Floyd algorithm: shortest path between each two nodes
input from infile, and output result to outfile
2017/12/16
'''
infile = input('infile:')
outfile = input('outfile:')
num = int(input('city num:'))
dist = [[0 for col in range(num)] for row in range(num)]
fin = open(infile, "r")
fout = open(outfile, "w")
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
                dist[i][j] = dist[i][k] + dist[k][j] 
for i in dist:
    for j in i:
        fout.write(str(round(j, 3)) + ' ')
    fout.write('\n')
fin.close()
fout.close()

