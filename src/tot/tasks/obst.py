import re
import os
import json
from typing import Self
import sympy
import pandas as pd
from tot.tasks.base import Task, DATA_PATH
from tot.prompts.obst import * 
import sys

# Dynamic Programming code for Optimal Binary Search 
# Tree Problem 

INT_MAX = 2147483647

""" A Dynamic Programming based function that
calculates minimum cost of a Binary Search Tree. """
def optimalSearchTree(keys, freq, n):

	""" Create an auxiliary 2D matrix to store
		results of subproblems """
	cost = [[0 for x in range(n)] 
			for y in range(n)]
	r_values = [[-1 for x in range(n)] 
			for y in range(n)]

	""" cost[i][j] = Optimal cost of binary search 
	tree that can be formed from keys[i] to keys[j]. 
	cost[0][n-1] will store the resultant cost """

	# For a single key, cost is equal to
	# frequency of the key 
	for i in range(n):
		cost[i][i] = freq[i] 
		r_values[i][i] = i + 1

	# Now we need to consider chains of 
	# length 2, 3, ... . L is chain length. 
	for L in range(2, n + 1): #2,3,4,...,n
	
		# i is row number in cost 
		for i in range(n - L + 1): #0-(n-1),0-(n-2),...,0-1
			
			# Get column number j from row number 
			# i and chain length L 
			j = i + L - 1 #(1,2,3,...,n),(2,3,4,...,n),(3,4,5,...,n),...,(n-1,n)
			off_set_sum = sum(freq, i, j)
			if i >= n or j >= n:
				break
			cost[i][j] = INT_MAX
			
			# Try making all keys in interval 
			# keys[i..j] as root 
        
			for r in range(i, j + 1): 
		
			    # c = cost when keys[r] becomes root 
				# of this subtree
				c = 0
				r_fin = -1
				if (r > i):
					c += cost[i][r - 1]
				if (r < j):
					c += cost[r + 1][j]
				c += off_set_sum 
                
				if (c < cost[i][j]):
					cost[i][j] = c
					r_fin = r
					#print(keys[r_fin])  
					r_values[i][j] = keys[r_fin]
     
    #now extracting the tree structure from r_values
	tree_array = get_tree_structure_driver(r_values, n)

	return cost[0][n - 1], r_values, cost, tree_array

# A utility function to get sum of 
# array elements freq[i] to freq[j] 
def sum(freq, i, j):
    s = 0
    for k in range(i, j + 1):
        if j >= len(freq):
            break
        s += freq[k] 
    return s 

#A utility function to get the OBST structure out of r_values
def get_tree_structure_driver(r_values, n):
    tree_array = [-1 for x in range(n)]
    tree_array[0] = r_values[0][n-1]
    go_left(r_values, n, 0, n-1, tree_array)
    go_down(r_values, n, 0, n-1, tree_array)
    
    return tree_array

def go_left(r_values, n, i, j, tree_array):
    if j < 0:
        return
    while(j >= 1 and r_values[i][j] == r_values[i][j-1] and r_values[i][j] > -1):
        j -= 1
    if j > 0:
        j -= 1
    if r_values[i][j] > -1 and r_values[i][j] != r_values[i][j+1]:
        k = 0
        while(k < n and tree_array[k] > -1):
            k += 1
        if k < n and r_values[i][j] not in tree_array:
            tree_array[k] = r_values[i][j]
    if j > 0 and r_values[i][j-1] > -1 and r_values[i][j] > -1:
        go_left(r_values, n, i, j, tree_array)
    if i < n-1 and r_values[i+1][j] > -1 and r_values[i][j] > -1:
        go_down(r_values, n, i, j, tree_array)
    
    
        
def go_down(r_values, n, i, j, tree_array):
    if i > n-1:
        return
    while(i < n-1 and r_values[i][j] == r_values[i+1][j]and r_values[i][j] > -1):
        i += 1
    if i < n-1:
        i += 1
    if r_values[i][j] > -1 and r_values[i][j] != r_values[i-1][j]:
        k = 0
        while(k < n and tree_array[k] > -1):
            k += 1
        if k < n and r_values[i][j] not in tree_array:
            tree_array[k] = r_values[i][j]
            #print(tree_array[k])#TODO
    if j > 0 and r_values[i][j-1] > -1 and r_values[i][j] > -1:
        go_left(r_values, n, i, j, tree_array)
    if i < n-1 and r_values[i+1][j] > -1 and r_values[i][j] > -1:
        go_down(r_values, n, i, j, tree_array)      


class Obst(Task):
    """
    Input (k, freq)   : k an array of key values, freq an array with the frequencies of k[i]
    Output (y)  : the optimal binary search tree
    Reward (r)  : 0 or 1, depending on whether the trajectory is correct
    Input Example: 
        keys=[1,2,3,4,5],
        freq=[11,8,6,10,4]
    Output Example: 
        [2, [1, null, null],
            [4, [3, null, null],
                [5, null, null]]]
    """
    def __init__(self, file='obst.json'):
        """
        file: a csv file (fixed)
        """
        super().__init__()
        path = os.path.join(DATA_PATH, 'obst', file)
        self.data = json.load(open(path))
        for i in self.data:
            print(i)
        self.n = len(self.data)
        self.value_cache = {}
        self.steps = 3
        #self.stops = ['\n'] * 4
        

    def __len__(self) -> int:
        return self.n
    
    def set_steps(self, s):
        self.steps = s

    def get_input(self, idx: int) -> str:
        return self.data[idx]

    def test_output(self, idx: int, output: str):
        #only used for logging        
        if str(self.data[idx][1][0]).replace(" ", "") == output.replace(" ", ""):
            return {'r': 1}
        else:
            return {'r': 0}
       
                        
    @staticmethod
    def standard_prompt_wrap(x: str, y:str='') -> str:
        formal_input = "k=" + str(x[0][0]) + ",freq=" + str(x[0][1])
        prompt= standard_prompt.format(input=formal_input) + y
        print(prompt)
        print("standard_prompt_wrap-----------------------------------------------------------")
        return prompt

    @staticmethod
    def cot_prompt_wrap(x: str, y:str='') -> str:
        formal_input = "k=" + str(x[0][0]) + ",freq=" + str(x[0][1])
        prompt= cot_prompt.format(input=formal_input) + y
        print(prompt)
        print("cot_prompt_wrap-----------------------------------------------------------")
        return prompt
    
    @staticmethod
    def propose_prompt_wrap(x: str, y: str='') -> str:
        formal_input = ("k=" + str(x[0][0]) + ",freq=" + str(x[0][1]) + ", and the partially created tree " + y)
        if y == '':
            formal_input += " []"
        prompt = propose_prompt.format(input=formal_input)
        print(prompt)
        print("propose_prompt_wrap-----------------------------------------------------------")
        return prompt
        
    
    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        formal_input = ("k=" + str(x[0][0]) + ",freq=" + str(x[0][1]) + ", and the partially created tree " + y).strip()
        prompt = value_prompt.format(input=formal_input)
        print(prompt)
        print("value_prompt_wrap-----------------------------------------------------------")
        return prompt
    
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        #if len(y.strip().split('\n')) == 4 and 'answer' not in y.lower():
            #return 0
        value_names = [_.split('\n')[-1] for _ in value_outputs]
        #value_map = {'less likey': 0.001, 'likely': 1, 'very likely': 20}  # TODO: ad hoc
        try:   
            value = int(re.findall(r'\d', value_names[-1])[-1]) if value_names else None
        except IndexError:
            value = 1
        #TODO when searching for the last number in the response, and if the 
        #chance is not provided, a wrong number is assumed to be the chance value
        print(value)
        print("value_outputs_unwrap-----------------------------------------------------------")
        return value
    
    @staticmethod
    def completeness_prompt_wrap(x: str, y: str):
        formal_input = ("k=" + str(x[0][0]) + ", tree=" + y).strip()
        prompt = completeness_prompt.format(input=formal_input)
        print(prompt)
        print("completeness_prompt_wrap-----------------------------------------------------------")
        return prompt
    
    
    
def print_info(cost_value, r_values, cost, tree_array):
    print("The optimal cost is: ", cost_value)
    
    print("The r_values are:")
    for i in range(len(r_values)):
        print(r_values[i])
    
    print("\nThe cost matrix is: ")
    for i in range(len(cost)):
        print(cost[i])
        
    print("\nThe tree array is: ", tree_array)
    print("\n\n")
   
    
    


#cost_value, r_values, cost, tree_array = optimalSearchTree([1,2,3,4,5,6,7,8,9],[5,2,4,1,3,12,17,15,11], 9)
#print_info(cost_value, r_values, cost, tree_array)

