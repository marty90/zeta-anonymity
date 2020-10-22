from datetime import datetime, timedelta
import json
import numpy as np
from utils import *
import sys

def run(Deltat, H, LRU, c, output, lines, observed_attributes, c_oa, t_oa, file):
    """Function that calls all the methods for the implementation of the z-anon
    
    Input:
    Deltat(int): the time period, in seconds
    H(dict): the attributes' hash table
    LRU(dict): FIFO lists of users, one per attribute
    c(dict): the Python dictionary containing the counter value for every attribute
    output(list): the list where to record the counter value for each input tuple
    lines(int): the number of lines to read from the input file
    observed_attibutes(list): list of attributes whose counter values are monitored over time
    c_oa(dict): the Python dictionary containing the counter value for the observed attributes
    t_oa(dict): the Python dictionary containing the timestamp for the corresponding counter value in c_oa
    
    Output:
    t_start(int), t_stop(int): the start and end timestamp of the """
    i = 0
    for line in open(file, 'r'):
        i += 1
        #read next input line
        t, u, a = read_next_visit(line, file)
        if i == 1:
            t_start = t
            
        #manage data structure
        manage_data_structure(t, u, a, H, LRU, c, file)
        #evict old users
        evict(t, H, LRU, c, Deltat)
        #possibly outputs the data
        check_and_output(t, u, a, c, output, file)
        
        if i%(lines/100) == 0: #save one hundred samples for monitoring
            for oa in observed_attributes:
                t_oa[oa].append(t)
                c_oa[oa].append(c[oa] if oa in c else 0)
        
        if i == lines:
            t_stop = t
            break
    print('End of simulation (simulated time: {})'.format(str(timedelta(seconds = int(t_stop - t_start)))))
    return t_start, t_stop

def main(lines, file):
    """Defines the simulation parameters. Writes valuable information from the simulation in files.
    
    Input:
    lines(int): the number of lines to read from the input file
    """
    # algorithm parameters
    Deltat = 3600 #in seconds
    #data structures
    H = {}
    LRU = {}
    c = {}
    output = []
    #run parameters
    observed_attributes = ['google.it', 'yahoo.com', 'gazzetta.it']
    c_oa = {k:[] for k in observed_attributes} #a list of counters for the observed attributes
    t_oa = {k:[] for k in observed_attributes} #the moments in which the counters have been evaluated
    start, stop = run(Deltat, H, LRU, c, output, lines, observed_attributes, c_oa, t_oa, file)
    
    #save the output as file
    f = open('simulation_output.txt', 'w+')
    i=0
    z=50
    for record in output: 
        f.write("\t".join(str(x) for x in record[0])+ "\t" + "\t".join(str(x) for x in record[1]) + '\n')
    f.close()
    
    g = open('output_params.json', 'w+')
    g.write(json.dumps({'c_oa': c_oa, 't_oa': t_oa, 'start': start, 'observed_attributes': observed_attributes}))
    g.close()

if __name__ == '__main__':
    lines = int(sys.argv[1])
    file = str(sys.argv[2])
    main(lines, file)