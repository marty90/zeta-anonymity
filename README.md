# zeta-anonymity

A script that simulates the behaviour of a $z$-anonymity module. The input arrives in the form of a triple $(t,u,a)$, meaning that at tome $t$ a user $u$ exposes an attribute $a$. The output is stored in the file `simulation_output.txt`, where each line describes the input triple, with the addition of the counter of $a$ in the $\Delta t$. A subsequent analysis of the output file can simulate the behaviour of the system with different values of $z$.

The `main.py` file launches and hold the simulation, together with the functions contained in `utils.py`. The `evaluate_output.py` file performs some analysis on the simulation results.

To run the simulation, execute the following command:

```
>>> python main.py <lines of input to simulate>
```