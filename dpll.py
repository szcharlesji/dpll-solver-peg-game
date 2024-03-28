import sys

atoms = set()


def dpll(clauses, results):
    global atoms

    if not clauses:  # If there are no clauses, satisfied
        return results
    elif [] in clauses:  # If there is an empty clause, unsatisfiable
        return None

    # Check for single atom clauses and prioritize in the order of atoms
    for clause in clauses:
        if len(clause) == 1:
            literal = clause[0]
            current_atom = abs(literal)
            if current_atom not in results:
                # change the order in which atoms are chosen
                atoms.remove(current_atom)
                atoms.insert(0, current_atom)

    satisfied = True
    current_atom = None
    for atom in atoms:
        if atom not in results:  # If a atom does not have a value
            satisfied = False  # It's not yet satisfied
            current_atom = atom
            break
    if satisfied:
        return results  # Otherwise, everything is satisfied and return

    true_results = results.copy()  # Try setting the current atom to True
    true_results[current_atom] = True
    false_results = results.copy()  # Try setting the current atom to False
    false_results[current_atom] = False

    # The new clauses to test the current atom
    true_clauses = []
    false_clauses = []
    # A clause is satisfied if it contains the current atom
    for clause in clauses:
        if current_atom not in clause:
            true_clauses.append(clause)
        if -current_atom not in clause:
            false_clauses.append(clause)

    # Remove the opposite of the current atom from the clause
    # for true
    for i in range(len(true_clauses)):
        new_clause = []
        for literal in true_clauses[i]:
            if literal != -current_atom:
                new_clause.append(literal)
        true_clauses[i] = new_clause
    result_true = dpll(true_clauses, true_results)
    # for false
    for i in range(len(false_clauses)):
        new_clause = []
        for literal in false_clauses[i]:
            if literal != current_atom:
                new_clause.append(literal)
        false_clauses[i] = new_clause
    result_false = dpll(false_clauses, false_results)

    if result_true:
        return result_true
    if result_false:
        return result_false
    return None


def main(*args, **kwargs):
    # parse text input
    if len(sys.argv) != 3:
        print("Usage: python dpll.py <input_file> <output_file>")
        return

    # input and output
    input_file = open(sys.argv[1], "r")
    output_file = open(sys.argv[2], "w")

    clauses = []
    start_back_matter = False
    back_matter = []
    for line in input_file:
        if line[0] == "0":  # If the line is the end of the clauses
            start_back_matter = True
            continue
        if start_back_matter:  # If the line is in the back matter
            back_matter.append(line)
            continue
        clause = []
        for literal in line.split():  # If the line is a clause
            clause.append(int(literal))
        clauses.append(clause)

    global atoms

    # Get all the atoms
    for clause in clauses:
        for literal in clause:
            atoms.add(abs(literal))
    atoms = list(atoms)
    results = {}
    result = dpll(clauses, results)

    # Write the result to the output file
    if result:
        for atom in atoms:
            if atom not in result:
                result[atom] = True
        # Sort the result by atoms' orders
        result = dict(sorted(result.items()))
        for k, v in result.items():
            output_file.write(str(abs(k)) + " ")
            if v:
                output_file.write("T")
            else:
                output_file.write("F")

            if k != len(result):
                output_file.write("\n")
            else:
                output_file.write("\n0")
    # When whole thing is unsatisfiable
    else:
        output_file.write("0")

    # Writing the back matter in the input file
    if back_matter:
        output_file.write("\n")
        for line in back_matter:
            output_file.write(line)

    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
