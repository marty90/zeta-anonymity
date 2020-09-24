import matplotlib.pyplot as plt
import numpy as np
import json

def plot_ca():
    params = json.loads(open('output_params.json', 'r').read())
    start = params['start']
    c_oa = params['c_oa']
    t_oa = params['t_oa']
    observed_attributes = params['observed_attributes']
    plt.figure(figsize = (10,6))
    plt.xlabel('s')
    plt.ylabel('c_a')
    #plt.plot([0, stop-start], [z, z], '--', label = 'z')
    for oa in observed_attributes:
        plt.plot([(x - start) for x in t_oa[oa]], c_oa[oa], label = oa)

    #plt.xticks()
    plt.grid()
    plt.legend()
    plt.show()

def get_pkanon(output, z):
    final_dataset = {}
    for o in output:
        record = o[0]
        c_a = o[1]
        if c_a >= z:
            if record[1] in final_dataset:
                final_dataset[record[1]].add(record[2])
            else:
                final_dataset[record[1]] = {record[2]}

    final_dataset_inv = {}
    for k,v in final_dataset.items():
        if str(v) not in final_dataset_inv:
            final_dataset_inv[str(v)] = [k]
        else:
            final_dataset_inv[str(v)].append(k)

    #ks = np.array([len(v) for v in final_dataset_inv.values()])
    return final_dataset_inv

        
def pkanon_vs_z():
    output = []
    for line in open('simulation_output.txt', 'r'):
        items = line.split('\t') 
        output.append(((float(items[0]), items[1], items[2]), int(items[3].strip())))
    
    z_range = range(10, 50)
    #k1 = []
    k2 = []
    k3 = []
    k4 = []
    for z in z_range:
        ks = np.array([len(v) for v in get_pkanon(output, z).values()])
        #k1.append(sum(ks[ks == 1])/sum(ks))
        k2.append(sum(ks[ks >= 2])/sum(ks))
        k3.append(sum(ks[ks >= 3])/sum(ks))
        k4.append(sum(ks[ks >= 4])/sum(ks))

    plt.figure()
    plt.xlabel('z')
    plt.ylabel('p_kanon')
    #plt.plot(z_range, k1,  '-', label = 'k = 1')
    plt.plot(z_range, k2, label = 'k = 2')
    plt.plot(z_range, k3, label = 'k = 3')
    plt.plot(z_range, k4, label = 'k = 4')
    plt.legend()
    plt.show()
    
if __name__ == '__main__':
    plot_ca()
    pkanon_vs_z()