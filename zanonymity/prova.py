import zanon
import cProfile

def run_anonymity():
    for i,line in enumerate(open(file_in, 'r')):
        t,u,a = line.split(",")
        z.anonymize((t,u,a))
        if(i == 3000000):
            break
    z.endFiles()
file_in = "trace.txt"
deltat = 3600 #in seconds
zeta = 20

z = zanon.zanon(deltat)

cProfile.run("run_anonymity()")

z.duration()
z.plot_z()
z.final_kanon()



