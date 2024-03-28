import sys


def main(*args, **kwargs):
    if len(sys.argv) != 3:
        print("Usage: python3 backend.py <input_file> <output_file>")
        return
    input_file = open(sys.argv[1], "r")
    output_file = open(sys.argv[2], "w")

    procedures = []
    truth_values = []
    flag = False
    for line in input_file:
        if line[0] == "0":
            flag = True
            continue
        if flag:
            procedures.append(line.split()[1])
        else:
            truth_values.append(line.split()[1])

    print(procedures)
    print(truth_values)

    if len(truth_values) == 0:
        output_file.write("NO SOLUTION")
        input_file.close()
        output_file.close()
        return

    outputs = []
    for index, truth_value in enumerate(truth_values):
        if truth_value == 'T' and procedures[index].startswith("Jump"):
            # output_file.write(procedures[index])
            # output_file.write("\n")
            outputs.append(procedures[index])

    for output in sorted(outputs, key=lambda x: int(x[-2])):
        output_file.write(output)
        output_file.write("\n")

    # Remove last newline
    output_file.seek(output_file.tell() - 1)
    output_file.truncate()

    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
