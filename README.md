# zanon

A module to anonymize data streams with zero-delay called z-anonymity.

When instantiating the *zanon* object, the constructor receives a value in seconds for **Delta_t** and a value for **z**.

The *anonymize()* method accepts a tuple with 3 arguments **(t,u,a)** , meaning that at time **t** a user **u** exposes an attribute **a**.

If the tuple exposes an attribute that has not been exposed by at least other **z - 1** users in the past **Delta_t**, the tuple is simply ignored. Otherwise, the tuple is printed in the file 'output.txt'.

The algorithm can handle generalization when providing the attribute with a hierarchy using \* as separator (*max_generalization\*...\*min_generalization\*attribute*).
Whenever releasing the attribute is not possible, the algorithm will look for the most specific generalization exposed by at least other **z - 1** users in the past **Delta_t**. If none is found, nothing is print out.

### other methods

*evaluate_output()* and *evaluate_category(int z)* offer informations about how the algorithm performed.

*duration()* print the range of time covered.

## example of usage
```python
from zanonymity import zanon

file_in = "trace.txt"
deltat = 3600 #in seconds
zeta = 20

z = zanon.zanon(deltat,zeta)

for line in open(file_in, 'r'):
    t,u,a = line.split(",")
    z.anonymize((t,u,a))

z.duration()
z.evaluate_output()
z.evaluate_category(zeta)

```
