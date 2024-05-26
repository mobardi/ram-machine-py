import sys
from collections import defaultdict

class RAM:
    def __init__(self):
        self.registers = defaultdict(int)
        self.program = None
        self.program_counter = 0

    def parse(self, program_file): # Question 1
        with open(program_file, 'r') as file:
            instructions = file.readlines()
        self.program = [self.parse_inst(inst.strip().split()) for inst in instructions]

    def parse_inst(self, inst):
        if inst[0] in ('LOAD', 'ADD', 'SUB', 'MUL', 'DEC', 'JZ', 'JMP', 'OUTPUT'):
            return inst
        else:
            raise ValueError(f"Invalid instruction: {' '.join(inst)}")
        
    def one_step(self, program, counter, input): # Question 2
        self.parse(program)
        self.program_counter = counter
        for i in range(2):
            self.compute_inst(self.program[self.program_counter], input)
            counter+=1
            
    def compute(self, program, input): # Question 3
        self.parse(program)
        self.program_counter = 0
        while self.program_counter < len(self.program):
            self.compute_inst(self.program[self.program_counter], input)

    def compute_inst(self, inst, input):
        if inst is None:
            self.program_counter += 1
        else:
            inst_str = ' '.join(map(str, inst))
            reg_str = ', '.join([f'r{reg}: {val}' for reg, val in self.registers.items()])
            print(f'Instruction: {inst_str} | Registres: {{{reg_str}}} | Pointeur: {self.program_counter}') # Question 4
            if inst[0] == 'LOAD':
                if inst[2][0] == 'i':
                    self.registers[int(inst[1])] = input[int(inst[2][1:])]  # Vérifie si c'est une entrée ik
                else:
                    self.registers[int(inst[1])] = int(inst[2])  # Considere comme entier (on rajoute des elif en fonction des entrées à utiliser dans le code ram)
                self.program_counter += 1
            elif inst[0] == 'ADD':
                self.registers[int(inst[3])] = self.registers[int(inst[1])] + self.registers[int(inst[2])]
                self.program_counter += 1
            elif inst[0] == 'SUB':
                self.registers[int(inst[3])] = self.registers[int(inst[1])] - self.registers[int(inst[2])]
                self.program_counter += 1
            elif inst[0] == 'MUL':
                self.registers[int(inst[3])] = self.registers[int(inst[1])] * self.registers[int(inst[2])]
                self.program_counter += 1
            elif inst[0] == 'DEC':
                self.registers[int(inst[1])] -= 1
                self.program_counter += 1
            elif inst[0] == 'JZ':
                if self.registers[int(inst[1])] == 0:
                    self.program_counter = int(inst[2])
                else:
                    self.program_counter += 1
            elif inst[0] == 'JMP':
                self.program_counter = int(inst[1])
            elif inst[0] == 'OUTPUT':
                print("Output:", self.registers[int(inst[1])])
                self.program_counter += 1

def main():
    # Usage: python ram.py <fichier.txt> <valeur1> <valeur2>..."
    ram = RAM()
    file_name = sys.argv[1]

    if 'step' in sys.argv:
        input = tuple(map(int, sys.argv[4:]))
        pos=int(sys.argv[3])
        ram.one_step(file_name, pos, input) # Pour executer un pas de la machine python ram.py <fichier.txt> [step] [pos] <valeur1> <valeur2>
    else: # Exécuter le programme normalement du début à la fin
        input = tuple(map(int, sys.argv[2:]))
        ram.compute(file_name, input) # python ram.py <fichier.txt> <valeur1> <valeur2>...
if __name__ == "__main__":
    main()

