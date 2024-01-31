#5-shot
standard_prompt = '''Given an array k and an array freq where k contains key values from 1 to n
and freq the respective frequencies for the use of these keys. Construct an 
optimal binary search tree to minimize the average search time for the key values.
Output only the array representation of the optimal binary search tree.
No further explanation needed.

Input: {input}
Answer: 
'''
'''0-shot: Think step by step. Kein Beispiel'''

'''Given an array k and an array freq where k contains key values from 1 to n
and freq the respective frequencies for the use of these keys. Construct an 
optimal binary search tree to minimize the average search time for the key values.
Output only the array representation of the optimal binary search tree.
No further explanation needed.

Input: k=[1,2,3], freq=[3,7,2]
Answer: [2,1,3]
            
Input: k=[1,2,3], freq=[6,4,9]
Answer: [3,1,null,null,2]
            
Input: k=[1,2,3,4,5], freq=[11,8,6,10,4]
Answer: [2,1,4,null,null,3,5]
                
Input: k=[1,2,3,4,5,6,7], freq=[4,13,8,22,9,2,32]
Answer: [4,2,7,1,3,5,null,null,null,null,null,null,6]
                
Input: k=[1,2,3,4,5,6,7,8,9], freq=[7,1,9,4,3,8,2,5,6]
Answer:  [6,3,8,1,4,7,9,null,2]

Input: {input}
Answer: '''



#3-shot
cot_prompt = '''Given an array k and an array freq where k contains key values
and freq the respective frequencies for the use of the keys. Construct an 
optimal binary search tree to minimize the average search time for the key values.
Output the array representing the optimal binary search tree. 
Construct the binary tree stepwise from top to bottom. With each step, try to 
estimate which new nodes can minimize the total costs the most, and construct the 
next level of the optimal binary search tree.

Input: k=[1,2,3], freq=[3,7,2]
Steps:  1. Starting with the root node of the optimal binary search tree as the first entry in 
        our output array. The root node is likely 2, because the key value 2 is in the middle of 
        the array of keys and has the highest frequency value.
        temporary_output: [2]
        2. Now creating the second level of the optimal binary search tree. We can insert the 
        key values 1 and 3 as the two child nodes of 2.
        temporary_output: [2,1,3]
        3. All out key values are used in the optimal binary search tree, so this is our 
        final answer.
Answer: [2,1,3]
            
Input: k=[1,2,3,4,5], freq=[11,8,6,10,4]
Steps:  1. As a root node for the optimal binary search tree, we choose the key value 2.
        Although it does not have the highest frequency, nor is it perfectly in the middle of
        the array of keys. But it is a good compromise between these two main factors.
        temporary_output: [2]
        2. On the second level of the tree, the left child will of course be the key value 1,
        as it is the only remaining one that is smaller than the root node 2 and therefore must
        be in the left partial tree of the root node 2. The right child node of 2 will be 4 
        because it splits the remaining keys that are larger than 2 perfectly in half, and it
        has the highest frequency of all nodes.
        temporary_solution: [2,1,4]
        3. Now only the key values 3 and 5 are missing in out temporary solution, and we can
        add them on the third level of the tree as the children of the node 4. The node 2 will
        just have two empty child nodes that we call null.
        temporary_solution: [2,1,4,null,null,3,5]
        4. All out key values are used in the optimal binary search tree, so this is our 
        final answer.
Answer: [2,1,4,null,null,3,5]
                
Input: k=[1,2,3,4,5,6,7,8,9], freq=[7,1,9,4,3,8,2,5,6]
Steps:  1. As a root node for the optimal binary search tree, we choose the key value 6. It 
        splits the key array almost perfectly in half and has the second-highest frequency value.
        These two properties combined make a good root node for our optimal binary search tree.
        temporary_solution: [6]
        2. On the second level of the tree, the left child will be the key value 3, as it has the 
        highest frequency of all key values, and additionally splits the array of key values that
        are smaller than 6 perfectly in half. The right child of the root node 6 will be 8 for
        the same reasons.
        temporary_solution: [6,3,8]
        3. On the third level of the optimal binary search tree, we can insert up to 4 new nodes.
        The left child of 3 will be 1, as there are only two key values remaining that are
        smaller than 3, and 1 has a higher frequency than the value 2. The right child of 3 will be
        4 because it has a higher frequency than the key value 5. For the node with the value 8, 
        the choice is very clear because the only left child can be 7, and the only right child 
        can be 9.
        temporary_solution: [6,3,8,1,4,7,9]
        4. On the fourth level, the left child of 1 has to be null because there is no key value
        that is smaller than 1. The right child of 1 is 2 though because it is the only remaining
        key value between the already used values 1 and 3. The left child of 4 is null, and the 
        right child of 4 is the key value 5. Now there are no more missing key values, so 
        the children of 7 and 9 will all be null.
        temporary_solution: [6,3,8,1,4,7,9,null,2,null,5,null,null,null,null]
        5. All out key values are used in the optimal binary search tree, so this is our 
        final answer.
Answer:  [6,3,8,1,4,7,9,null,2,null,5,null,null,null,null]

Input: {input}
Steps:
Answer:
'''

#1-shot
propose_prompt = '''Given an array k and an array freq where k contains key values
and freq the respective frequencies for the use of the keys. The goal is to construct an 
optimal binary search tree to minimize the average search time for the key values.
In the very end, output the array representing the optimal binary search tree.
Given a complete example of how to construct an optimal binary search tree,
and an example of possible next steps given the input arrays k and freq and an already
partially created optimal binary search tree, propose possible next steps in the construction of 
the optimal binary search tree in the last example.
Complete example:
Input: k=[1,2,3,4,5], freq=[11,8,6,10,4]
Steps:  1. As a root node for the optimal binary search tree, we choose the key value 2.
        Although it does not have the highest frequency, nor is it perfectly in the middle of
        the array of keys. But it is a good compromise between these two main factors.
        temporary_output: [2]
        2. On the second level of the tree, the left child will of course be the key value 1,
        as it is the only remaining one that is smaller than the root node 2 and therefore must
        be in the left partial tree of the root node 2. The right child node of 2 will be 4 
        because it splits the remaining keys that are larger than 2 perfectly in half, and it
        has the highest frequency of all nodes.
        temporary_solution: [2,1,4]
        3. Now only the key values 3 and 5 are missing in out temporary solution, and we can
        add them on the third level of the tree as the children of the node 4. The node 2 will
        just have two empty child nodes that we call null.
        temporary_solution: [2,1,4,null,null,3,5]
        4. All out key values are used in the optimal binary search tree, so this is our 
        final answer.
Answer: [2,1,4,null,null,3,5]

Example of possible next steps:
Input: k=[1,2,3,4,5], freq=[11,8,6,10,4], and the partially created tree [2]
Possible next steps in the Optimal Binary Tree Construction:
[2, 1, 3]
[2, 1, 4]
[2, 1, 5]
[2, null, 3]
[2, null, 4]
[2, null, 5]
[2, 1, null]

Input: {input}
Possible next steps in the Optimal Binary Tree Construction: 
Your proposals here

'''

value_prompt = '''Given a partially constructed binary tree, evaluate whether it has a chance of becoming
the Optimal Binary Search Tree and how high that chance is. Give an estimator value representing this chance.
The estimator value must be an integer between 1 and 10 where 1 indicates a very low chance, and 10 a very high chance.

Input: k=[1,2,3], freq=[3,7,2], and the partially created tree [2]
Reasoning: The key value 2 is root of our constructed tree, and it has the highest frequency and is in the middle of the values of the key array. 
Judgement: 9

Input: k=[1,2,3], freq=[6,4,9], and the partially created tree [1]
Reasoning: The key value 1 only has the second-highest frequency and is not in the middle of the values of the key array.
Judgement: 3

Input: k=[1,2,3,4,5], freq=[11,8,6,10,4], and the partially created tree [2,1,4]
Reasoning: The root of the partially created tree has the value 2. It is not exactly in the middle of the array
of keys, but it can still split it in half almost perfectly. Also, it has a modestly high frequency value.
Jugement pobably likely. But the key values 1 and 4 are on the second level of the tree, and they have
the two highest frequency numbers of all the key values. Additionally, the key value 4 splits the partial
array [3,4,5] very well in half.
Judgement: 8

Input: {input}
Reasoning:
Judgement: {{Fill in your estimator value here. Value must be an integer between 1 and 10, and one specific value MUST be provided.}}
'''


'''Input: k=[1,2,3,4,5,6,7], freq=[4,13,8,22,9,2,32], and the partially created tree [2, [1, ...], [4, [5, ...]]]
The root of the partially created tree has the value 2. It does not split the array of keys in half very well.
Additionally, the key 2 only has the third-hightest frequency value among all keys. 
In the right sub-tree, the value 4 does not split the array on the right side of 2 very well either, and
although it has the second-highest frequency, the key value 7 still has a significantly higher frequency.
less likely

Input: k=[1,2,3,4,5,6,7,8,9], freq=[7,1,9,4,3,8,2,5,6], and the partially created tree [6, [3, ...], [8, ...]]
The root of the partially created tree has the value 6. It does not split the array of keys in the middle,
but is still in a reasonable position to be considered the root node. Additionally, its frequency value
is the second-highest among all frequency values. In the left sub-tree, the key with the value 3 splits
the remaining left array in half very well and has the highest frequency. In the right sub-array, the 
key with the value 5 is in the middle and has a relatively high frequency.
So the root node is a bit suspicious, but the partially created tree still has a good chance of becoming
the optimal binary search tree for the given input.
likely'''


completeness_prompt = '''Given the following array of keys k and the result array tree
that represents a binary tree. Check whether the tree is a complete binary search
tree for the given keys. This means that all keys are present in the tree, and that 
the tree maintains a corrects binary tree structure. If so, answer with 1, if not,
answer with 0.
Examples:
Input: k=[1,2,3,4,5], tree=[2,1,4,null,null,3,5]
Reasoning: All key values from 1 up to 5 are used exactly once in the binary tree.
Answer: 1

Input: k=[1,2,3], tree=[3,1,4,null,2,null,null]
Reasoning: In the binary tree, the value 4 is used which is not part of the key values.
Answer: 0

Input: k=[1,2,3,4,5,6,7,8,9], tree=[6,3,8,1,4,7,9]
Reasoning: The key values 2 and 5 are missing in the binary tree.
Answer: 0

Input: k=[1,2,3,4,5,6,7], tree=[5,3,6,2,4,null,7,1,null,null,null,null,null,null,null]
Reasoning: All key values from 1 up to 7 are used exactly once in the binary tree.
Answer: 1

Input: {input}
Reasoning:
Answer: Your answer here. Exactly one value of either 0 or 1 MUST be provided.
'''


