import json
import os
from nodes import *
from pass_program import convert_program

def compute_program(program):
    node_values = []

    for node, inputs in zip(program["nodes"], program["inputs"]):
        node_values.append(node.compute([node_values[i] for i in inputs]))

if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    with open(dir_path[:-12] + '/data/programs/example.json', 'r') as example_file:
        example_program = json.load(example_file)

    program = convert_program(example_program)

    compute_program(program)