# DPLL SAT Solver with peg game parser

This program is written and tested in Python 3.9

1. Frontend:
The frontend reads the input file and parses the peg game. It then converts the peg game into a CNF formula and writes it to the output file.

``` bash
python3 frontend.py <input_file> <output_file>
```

2. DPLL
The DPLL algorithm reads the CNF formula from the input file and solves it. It then writes the solution to the output file.

``` bash
python3 dpll.py <input_file> <output_file>
```

3. Backend
THe backend converts the DPLL solution into a peg game solution and writes it to the output file.

``` bash
python3 backend.py <input_file> <output_file>
```
