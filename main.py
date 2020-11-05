import math
import operator
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import pandas as panda
from itertools import islice


def findId(node):
    index = 0
    for nd in G.nodes:
        if node == nd:
            return index
        index = index + 1


def yakobi(B):
    global dictNumToLink
    E = 0.001
    solveVector = []
    newVector = []
    for i in range(0, len(B)):
        solveVector.append(B[i][len(B)])
    eps = 1
    while eps > E:
        for i in range(0, len(B)):
            sum = 0
            for j in range(0, len(solveVector)):
                sum = sum + solveVector[j] * B[i][j]
            sum = sum + B[i][len(B)]
            newVector.append(sum)
        eps = 0
        for j in range(0, len(solveVector)):
            eps = eps + math.fabs(newVector[j] - solveVector[j])

        solveVector = newVector.copy()
        newVector.clear()
    finalDict = dict()
    for j in range(0, len(solveVector)):
        finalDict[j] = solveVector[j]
    finalDict = sorted(finalDict.items(), key=operator.itemgetter(1), reverse=True)
    return finalDict

#url = "https://prodota.ru"
url = "https://stackoverflow.com"
page = requests.get(url)
data = page.text
soup = BeautifulSoup(data, 'html.parser')
domain_name = urlparse(url).netloc

links = []
internal_links = []

links_id = []

for link in soup.find_all('a'):
    href = link.get('href')
    if href == url:
        continue
    if href in links:
        continue
    if href == "" or href is None:
        continue
    if domain_name not in href:
        continue
    links.append(href)
    links_id.append(href)
    internal_links.append([url, href])

for link in links:
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    visited = []
    for line in soup.find_all('a'):
        href = line.get('href')
        if href == link:
            continue
        if href in visited:
            continue
        if href == "" or href is None:
            continue
        if domain_name not in href:
            continue
        visited.append(href)
        internal_links.append([link, href])
        links_id.append(href)

df = panda.DataFrame(internal_links, columns=["from", "to"])
G = nx.from_pandas_edgelist(df, source="from", target="to")
nx.draw(G, with_labels=False)
plt.show()

dictNumToLink = dict()
for key, value in internal_links:
    if value in dictNumToLink.keys():
        dictNumToLink[value] = dictNumToLink[value] + 1
    else:
        dictNumToLink[value] = 1

dictNumToCountOfLink = dict()
for key, value in internal_links:
    if key in dictNumToCountOfLink.keys():
        dictNumToCountOfLink[key] = dictNumToCountOfLink[key] + 1
    else:
        dictNumToCountOfLink[key] = 1

d = 0.5
B = [[0 for x in range(len(G.nodes) + 1)] for y in range(len(G.nodes))]

for n in G.edges:
    B[findId(n[1])][findId(n[0])] = d / dictNumToCountOfLink[n[0]]

for i in range(0, len(B)):
    B[i][len(B)] = 1 - d

solution = yakobi(B)

for key, value in list(islice(solution, 10)):
    print(links_id[key], value)
