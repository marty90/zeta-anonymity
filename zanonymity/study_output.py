from collections import defaultdict
import numpy as np
MAX_GENERALIZATION = 20

final_dataset = defaultdict(set)
file = open('output.txt','r')
gen = [0]*MAX_GENERALIZATION
tot = 0
for line in file:
    tot += 1
    t,u,a = line.split("\t")
    t = float(t)
    a.strip()          
    final_dataset[u].add(a)
    cat = a.split("*")
    gen[len(cat)] += 1

final_dataset_inv = defaultdict(list)
for k,v in final_dataset.items():
    final_dataset_inv[str(v)].append(k)
ks = np.array([len(v) for v in final_dataset_inv.values()])
for k in range(2,5):
    print("Final " + str(k) + "-anonymization: " + str(sum(ks[ks >= k])/sum(ks)))
    
for index,i in enumerate(gen):
    if(i == 0 and index == 0):
        continue
    elif(i == 0):
        break
    print("Tuple passed with " + str(index ) + "-details level: " + str(i))
print("Tuple anonymized: " + str(3000000 - tot))
    