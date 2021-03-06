
import ete3
from ete3 import Tree
import numpy 
import random

# Pick a random
# non-root internal node and pick a new random height
# uniformly distributed between its parent and elder child
def uniform(tree_nodes):
	for node in tree_nodes.traverse("postorder"):
		node.height = node.get_farthest_node(topology_only=False)[1]
	#n_tips = len(tree_nodes.get_leaves())
	L = []
	for node in tree_nodes.traverse("postorder"):	
	    if node.is_leaf() == False:
	        L.append(node)
	internal_i = random.randint(0,len(L)-2)
	internal = L[internal_i]
	#internal_i = n_tips + numpy.random.randint(n_tips - 2)
	#internal = tree_nodes[internal_i]
	parent = internal.up

	left_child, right_child = internal.children

	elder_child_height = max(left_child.height, right_child.height)

	uniform_range = parent.height - elder_child_height

	internal.height = elder_child_height + numpy.random.random() * uniform_range

	internal.dist = parent.height - internal.height
	left_child.dist = internal.height - left_child.height
	right_child.dist = internal.height - right_child.height

	internal.new_dist = True
	left_child.new_dist = True
	right_child.new_dist = True
	return tree_nodes

# Pick a new root height from the distribution x + exp(1/x) where x is the
# height of the oldest non-root internal node.
def exponential(tree_nodes):
	root = tree_nodes[-1]
	old_height = root.height

	left_child, right_child = root.children

	elder_child_height = max(left_child.height, right_child.height)

	root.height = elder_child_height + numpy.random.exponential(elder_child_height)

	left_child.dist = root.height - left_child.height
	right_child.dist = root.height - right_child.height

	left_child.new_dist = True
	right_child.new_dist = True
	return tree_nodes

# Scale all nodes in the tree following a lognormal distribution
# (logmean = -1/2, sd = 1) which has a mean of 1.
def lognormal(tree_nodes):
	scaler = numpy.exp(numpy.random.normal(loc = -0.5))
	for node in tree_nodes:
		node.height = node.get_farthest_node(topology_only=False)[1]
		node.height *= scaler
		node.dist *= scaler
		#node.new_dist = True
	return tree_nodes
