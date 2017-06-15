# MIT 6.034 Lab 6: Neural Nets
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), Jake Barnwell (jb16), and 6.034 staff

from nn_problems import *
from math import e
INF = float('inf')

#### NEURAL NETS ###############################################################

# Wiring a neural net

nn_half = [1]

nn_angle = [2,1]

nn_cross = [2,2,1]

nn_stripe = [3,1]

nn_hexagon = [6,1]

nn_grid = [4,2,1]

# Threshold functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"
    if x>=threshold:
        return 1
    return 0

def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    return float(1)/(1+e**(-steepness*(x-midpoint)))

def ReLU(x):
    "Computes the threshold of an input using a rectified linear unit."
    if x>=0:
        return float(x)
    return float(0)

# Accuracy function
def accuracy(desired_output, actual_output):
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    return -0.5*(desired_output-actual_output)**2


# Forward propagation

def node_value(node, input_values, neuron_outputs):  # STAFF PROVIDED
    """Given a node, a dictionary mapping input names to their values, and a
    dictionary mapping neuron names to their outputs, returns the output value
    of the node."""
    if isinstance(node, basestring):
        return input_values[node] if node in input_values else neuron_outputs[node]
    return node  # constant input, such as -1

def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""

    neuron_outputs={}
    ordered_neurons=net.topological_sort()
    for neuron in ordered_neurons:
        inputs=net.get_incoming_neighbors(neuron)
        tem_out=0
        for input in inputs:
            wire=net.get_wires(startNode=input,endNode=neuron)
            weight=wire[0].get_weight()
            tem_out+=node_value(input,input_values,neuron_outputs)*weight
        neuron_outputs[neuron]=threshold_fn(tem_out)
    return (neuron_outputs[net.get_output_neuron()],neuron_outputs)


# Backward propagation warm-up
def gradient_ascent_step(func, inputs, step_size):
    """Given an unknown function of three variables and a list of three values
    representing the current inputs into the function, increments each variable
    by +/- step_size or 0, with the goal of maximizing the function output.
    After trying all possible variable assignments, returns a tuple containing:
    (1) the maximum function output found, and
    (2) the list of inputs that yielded the highest function output."""
    best=[-INF,None]
    perturbs=[-step_size,0,step_size]
    for perturb1 in perturbs:
        for perturb2 in perturbs:
            for perturb3 in perturbs:
                tem_inputs=[None,None,None]
                tem_inputs[0]=inputs[0]+perturb1
                tem_inputs[1]=inputs[1]+perturb2
                tem_inputs[2]=inputs[2]+perturb3
                tem_val=func(tem_inputs[0],tem_inputs[1],tem_inputs[2])
                if tem_val>best[0]:
                    best[0]=tem_val
                    best_inputs=[tem_inputs[0],tem_inputs[1],tem_inputs[2]]
                    best[1]=best_inputs
    return (best[0],best[1])



def get_back_prop_dependencies(net, wire):
    """Given a wire in a neural network, returns a set of inputs, neurons, and
    Wires whose outputs/values are required to update this wire's weight."""
    dependencies=[]
    dependencies.append(wire.startNode)
    dependencies.append(wire)
    end_node=wire.endNode
    dependencies.append(end_node)
    output_node=net.get_output_neuron()
    if end_node != output_node:
        for next_wire in net.get_wires(startNode=end_node,endNode=None):
            dependencies+=get_back_prop_dependencies(net,next_wire)
    s=set()
    for sth in dependencies:
        s.add(sth)
    return s


# Backward propagation
def calculate_deltas(net, desired_output, neuron_outputs):
    """Given a neural net and a dictionary of neuron outputs from forward-
    propagation, computes the update coefficient (delta_B) for each
    neuron in the net. Uses the sigmoid function to compute neuron output.
    Returns a dictionary mapping neuron names to update coefficient (the
    delta_B values). """
    mappings={}
    neurons=net.topological_sort()
    neurons.reverse()
    for neuron in neurons:
        output = neuron_outputs[neuron]
        if neuron == net.get_output_neuron():
            delta=output*(1-output)*(desired_output-output)
            mappings[neuron] = delta
        else:
            sum=0
            wires=net.get_wires(startNode=neuron,endNode=None)
            for wire in wires:
                end=wire.endNode
                sum+=mappings[end]*wire.get_weight()
            delta=output*(1-output)*sum
            mappings[neuron] = delta
    return mappings


def update_weights(net, input_values, desired_output, neuron_outputs, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses the
    sigmoid function to compute neuron output.  Returns the modified neural net,
    with the updated weights."""

    wires=net.get_wires()
    deltas=calculate_deltas(net,desired_output,neuron_outputs)
    for wire in wires:
        old=wire.get_weight()
        outA=node_value(wire.startNode,input_values,neuron_outputs)
        deltaB=deltas[wire.endNode]
        new_weight=r*outA*deltaB+old
        wire.set_weight(new_weight)
    return net

def back_prop(net, input_values, desired_output, r=1, minimum_accuracy=-0.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses the
    sigmoid function to compute neuron output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""
    iteration=0
    neuron_outputs=forward_prop(net,input_values,sigmoid)
    while accuracy(desired_output,neuron_outputs[0])<minimum_accuracy:
        iteration+=1
        net = update_weights(net,input_values,desired_output,neuron_outputs[1],r)
        neuron_outputs = forward_prop(net, input_values, sigmoid)
    return (net,iteration)

# Training a neural net

ANSWER_1 = 20
ANSWER_2 = 29
ANSWER_3 = 10
ANSWER_4 = 116
ANSWER_5 = 69

ANSWER_6 = 1
ANSWER_7 = "checkerboard"
ANSWER_8 = ['small','medium','large']
ANSWER_9 = "B"

ANSWER_10 = "D"
ANSWER_11 = ['A','C']
ANSWER_12 = ['A','E']


#### SURVEY ####################################################################

NAME = ""
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 0
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""
