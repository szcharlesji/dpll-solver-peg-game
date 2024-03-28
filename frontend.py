import sys


def convert_to_cnf(num_holes, starting_hole, pegs):
    atoms = {}
    clauses = []
    var_count = 1

    # Generate atoms for jumps
    for peg in pegs:
        a, b, c = peg
        for i in range(1, num_holes - 1):
            atoms[(a, b, c, i)] = var_count
            var_count += 1
        for i in range(1, num_holes - 1):
            atoms[(c, b, a, i)] = var_count
            var_count += 1
    # Generate atoms for pegs
    for i in range(1, num_holes + 1):
        for j in range(1, num_holes):
            atoms[(i, j)] = var_count
            var_count += 1

    # Generate clauses
    # Precondition axioms
    for peg in pegs:
        a, b, c = peg
        for i in range(1, num_holes - 1):
            clauses.append([-atoms[(a, b, c, i)], atoms[(a, i)]])
            clauses.append([-atoms[(a, b, c, i)], atoms[(b, i)]])
            clauses.append([-atoms[(a, b, c, i)], -atoms[(c, i)]])

        for i in range(1, num_holes - 1):
            clauses.append([-atoms[(c, b, a, i)], atoms[(c, i)]])
            clauses.append([-atoms[(c, b, a, i)], atoms[(b, i)]])
            clauses.append([-atoms[(c, b, a, i)], -atoms[(a, i)]])

    # Causal axioms
    for peg in pegs:
        a, b, c = peg
        for i in range(1, num_holes - 1):
            clauses.append([-atoms[(a, b, c, i)], -atoms[(a, i + 1)]])
            clauses.append([-atoms[(a, b, c, i)], -atoms[(b, i + 1)]])
            clauses.append([-atoms[(a, b, c, i)], atoms[(c, i + 1)]])

        for i in range(1, num_holes - 1):
            clauses.append([-atoms[(c, b, a, i)], -atoms[(c, i + 1)]])
            clauses.append([-atoms[(c, b, a, i)], -atoms[(b, i + 1)]])
            clauses.append([-atoms[(c, b, a, i)], atoms[(a, i + 1)]])

    # Possible jumps
    jumps = []
    for peg in pegs:
        a, b, c = peg
        jumps.append((a, b, c))
        jumps.append((c, b, a))

    # Frame axioms
    for i in range(1, num_holes + 1):  # i is the hole number
        for j in range(1, num_holes - 1):  # j is time
            possible_jumps = []
            for jump in jumps:
                a, b, c = jump
                if i == a or i == b:
                    possible_jumps.append(atoms[(a, b, c, j)])
            if len(possible_jumps) > 0:
                clauses.append([-atoms[(i, j)], atoms[(i, j + 1)], *possible_jumps])

    for i in range(1, num_holes + 1):  # i is the hole number
        for j in range(1, num_holes - 1):  # j is time
            possible_jumps = []
            for jump in jumps:
                a, b, c = jump
                if i == c:
                    possible_jumps.append(atoms[(a, b, c, j)])
            if len(possible_jumps) > 0:
                clauses.append([atoms[(i, j)], -atoms[(i, j + 1)], *possible_jumps])

    # One action at a time
    for i in range(1, num_holes - 1):  # j is time
        for j in range(len(jumps)):
            for k in range(j + 1, len(jumps)):
                jump1 = jumps[j]
                jump2 = jumps[k]
                a1, b1, c1 = jump1
                a2, b2, c2 = jump2
                clauses.append([-atoms[(a1, b1, c1, i)], -atoms[(a2, b2, c2, i)]])

    # Starting state
    clauses.append([-atoms[(starting_hole, 1)]])
    for i in range(1, num_holes + 1):
        if i != starting_hole:
            clauses.append([atoms[(i, 1)]])
    # Final solution
    solution = []
    for i in range(1, num_holes + 1):
        solution.append(atoms[(i, num_holes - 1)])
        print("Peg(%d,%d)" % (i, num_holes - 1))
    clauses.append(solution)

    # Ending state. No two holes have a peg
    for i in range(1, num_holes + 1):
        for j in range(i + 1, num_holes + 1):
            clauses.append([-atoms[(i, num_holes - 1)], -atoms[(j, num_holes - 1)]])
            print("-Peg(%d,%d), -Peg(%d,%d)" % (i, num_holes - 1, j, num_holes - 1))

    return atoms, clauses


def main(*args, **kwargs):
    if len(sys.argv) != 3:
        print("Usage: python3 frontend.py <input_file> <output_file>")
        return
    input_file = open(sys.argv[1], "r")
    output_file = open(sys.argv[2], "w")

    num_holes, starting_hole = map(int, input_file.readline().split())
    pegs = []
    while True:
        line = input_file.readline()
        if not line:
            break
        pegs.append(list(map(int, line.split())))

    print("Input data:")
    print(num_holes, starting_hole)
    for peg in pegs:
        print(peg)

    print("\nOutput data:")
    atoms, clauses = convert_to_cnf(num_holes, starting_hole, pegs)
    # for atom in atoms:
    #     if len(atom) == 2:
    #         print("Peg(%d,%d) = %d" % (atom[0], atom[1], atoms[atom]))
    #     else:
    #         print("Jump(%d,%d,%d,%d) = %d" % (atom[0], atom[1], atom[2], atom[3], atoms[atom]))
    # for clause in clauses:
    #     print(clause)

    # Write to output file
    for clause in clauses:
        output_file.write(" ".join(map(str, clause)) + "\n")
    output_file.write("0\n")
    for atom in atoms:
        if len(atom) == 2:
            output_file.write("%d Peg(%d,%d)" % (atoms[atom], atom[0], atom[1]))
        else:
            output_file.write("%d Jump(%d,%d,%d,%d)" % (atoms[atom], atom[0], atom[1], atom[2], atom[3]))
        if atom != list(atoms.keys())[-1]:
            output_file.write("\n")

    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
