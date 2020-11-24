from utils import *
from evaluate_category import *
from evaluate_output import *
import matplotlib.pyplot as plt
import collections

class zanon(object):

    def __init__(self, deltat): 
        super(zanon, self).__init__()
        self.deltat = deltat
        self.z = 10
        self.H = {}
        self.LRU = {}
        self.c = {}
        self.t_start = 0
        self.t_stop = 0
        self.last_update = 0
        self.test = []
        self.time = []
        self.kanon = []
        self.queue = collections.deque()
        self.f_out = open('output.txt', 'w+')
        self.f_count = open('counters.txt', 'w+')
        self.tot_data = []
        self.POS = {}
	
    def anonymize(self, tupla):
        
        t = float(tupla[0])
        u = tupla[1]
        a = tupla[2].strip()     
        
        if self.t_start == 0:
            self.t_start = t
            
        sep = '*'
        cat = a.split(sep)
        for level in range(len(cat)):    
            att = '*'.join(cat[:level + 1])
            if att in self.H:
                evict(self, t, att)
                
        if self.queue:            
            while True:
                temp = self.queue.popleft()
                if(t - temp[0] <= 3600.0):
                    self.queue.appendleft(temp)
                    break

            
        z_change(self, t)     
       
        self.t_stop = t
                
        manage_data_structure(self, t, u, a)
        check_and_output(self, t, u, a)
               

    def duration(self):
        print('End of simulation (simulated time: {})'.format(str(timedelta(seconds = int(self.t_stop - self.t_start)))))

    def evaluate_output(self):
        evaluate_output()
        
    def evaluate_category(self,z):
        evaluate_cat(z)
        
    def final_kanon(self):
        final_kanon()

    def plot_z(self):
        plot_z(self)
        
    def endFiles(self):
        self.f_out.close()
        self.f_count.close()
		