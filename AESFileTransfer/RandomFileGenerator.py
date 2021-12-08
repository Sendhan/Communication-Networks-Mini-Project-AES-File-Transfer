import uuid

def random_txt_file(filename, number_of_lines):
    with open(filename, 'w') as file:
        for i in range(number_of_lines):
            line = str(uuid.uuid4())
            file.write(line + '\n')


filename = input("Enter a filename : ")
number_of_lines = int(input("Enter number of lines : "))
random_txt_file(filename, number_of_lines)