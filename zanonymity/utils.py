import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
import numpy as np
from collections import defaultdict
import subprocess
import sys
import collections
from datetime import datetime, timedelta
#subprocess.check_call([sys.executable, "-m", "pip", "install", '-U', '--user', 'file_read_backwards'])
#from file_read_backwards import FileReadBackwards

def final_kanon():
    final_dataset = defaultdict(set)
    file = open('output.txt','r')
    for line in file:
        t,u,a = line.split("\t")
        t = float(t)
        a.strip()          
        final_dataset[u].add(a)

    final_dataset_inv = defaultdict(list)
    for k,v in final_dataset.items():
        final_dataset_inv[str(v)].append(k)
    ks = np.array([len(v) for v in final_dataset_inv.values()])
    for k in range(2,5):
        print("Final " + str(k) + "-anonymization: " + str(sum(ks[ks >= k])/sum(ks)))


def compute_kanon(self):   
    
    final_dataset = defaultdict(set)
    for i in self.queue:
        final_dataset[i[1]].add(i[2])       
    final_dataset_inv = defaultdict(list)
    for k,v in final_dataset.items():
        final_dataset_inv[str(v)].append(k)
    
    ks = np.array([len(v) for v in final_dataset_inv.values()])
    #print(sum(ks[ks >= 2])/sum(ks))
    return sum(ks[ks >= 3])/sum(ks)

def read_next_visit(line):
    t, u, a = line.split(',')
    t = float(t)
    a = a.strip()
    return t, u, a
    
def a_not_present(self, t, u, a):
    self.H[a] = {u:t}
    #self.LRU[a] = [(t,u)]
    self.c[a] = 1

def a_present(self, t, u, a):
    if u not in self.H[a].keys():
        u_not_present(self, t, u, a)
    else:
        u_present(self, t, u, a)

def u_not_present(self, t, u, a):
    self.H[a][u] = t
    self.c[a] += 1
    
def u_present(self, t, u, a):
    self.H[a][u] = t
    
def evict(self, t, a):
    to_remove = []
    for u,time in self.H[a].items():
        if (t - time > self.deltat):
            to_remove.append(u)
    for u in to_remove:
        self.H[a].pop(u, None)
        self.c[a] -= 1
        if len(self.H[a]) == 0:          
            self.H.pop(a, None)
            break

def manage_data_structure(self, t, u, a):
    sep = '*'
    cat = a.split(sep)
    for level in range(len(cat)):
        i = '*'.join(cat[:level + 1])
        if i not in self.H:
            a_not_present(self, t, u, i)
        else:
            a_present(self, t, u, i)
            
def z_change(self, t):
     if(t - self.t_start >= self.deltat and (t-self.last_update) >=300):
        self.last_update = t
        result = compute_kanon(self)
        self.kanon.append(result)
        if(result < 0.80):
            self.z += 1
        if(result > 0.81 and self.z > 5):
            self.z -=1
        #print("Value of z: " + str(self.z))
        self.test.append(self.z)
        self.time.append(str(datetime.utcfromtimestamp(t + 7200).strftime('%Y-%m-%d %H:%M:%S')))
        self.tot_data.append(len(self.queue))

        
def check_and_output(self, t, u, a):
    sep = '*'
    cat = a.split(sep)
    counters = []
    output = None
    for level in range(len(cat)):
        attr = '*'.join(cat[:level + 1])
        counters.append(self.c[attr])
        if self.c[attr] >= self.z:
            output = (t,u,attr)  
    if(output != None):
        self.queue.append(output)
        self.f_out.write("\t".join(str(x) for x in output) + "\n")
    self.f_count.write("\t".join(str(x) for x in [t,u,a])+ "\t" +
                       "\t".join(str(x) for x in counters[::-1]) + '\n')
 

def plot_z(self):
        
        color = 'tab:red'
        fig, ax_left = plt.subplots(figsize=(20, 10))
        ax_right = ax_left.twinx()
        ax_third = ax_left.twinx()
        ax_third.spines["right"].set_position(("axes", 1.1))
        ax_left.plot(self.time,self.test, color=color)
        ax_right.plot(self.time, self.kanon, color='black')
        ax_third.plot(self.time, self.tot_data, color = 'blue')
        ax_left.set_xlabel('time', fontsize=20)
        ax_left.set_ylabel('z', color=color, fontsize=20)
        ax_left.autoscale()
        ax_third.autoscale()
        ax_third.set_ylabel('Traffic', color = "blue", fontsize=20)
        ax_third.tick_params(axis='y', labelcolor="blue", labelsize=20.0)
        ax_right.set_ylim(bottom = 0.0, top = 1.0)
        ax_left.tick_params(axis='y', labelcolor=color, labelsize=20.0)
        ax_right.set_ylabel('pkanon', color='black', fontsize= 20)
        ax_right.tick_params(axis='y', labelcolor='black', labelsize = 20.0)
        ax_left.get_xaxis().set_major_locator(LinearLocator(numticks=20))
        ax_left.tick_params(labelsize=20)        
        fig.autofmt_xdate(rotation = 45)
        fig.tight_layout()
        fig.savefig('z_tuning.pdf')
        