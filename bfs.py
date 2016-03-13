#from dsyntnode import *
def bfs_search(root,lexeme):

	list_objects_no_processed = [root]
	list_hash_no_processed = [root.__hash__]
	list_hash_visited = []

	

	while len(list_objects_no_processed) != 0:

		first = list_objects_no_processed[0]
		
		list_hash_visited.append(first.__hash__)
		del list_objects_no_processed[0]

		

		if lexeme == first.gettag_lexeme():
			return first

		for neib in first.getLeafs():
			if neib.__hash__ not in list_hash_visited and neib.__hash__ not in list_hash_no_processed:
				list_objects_no_processed.append(neib)
				list_hash_no_processed.append(neib.__hash__)

	return None

def bfs_search2(root,class_):

	list_objects_no_processed = [root]
	list_hash_no_processed = [root.__hash__]
	list_hash_visited = []

	while len(list_objects_no_processed) != 0:
		first = list_objects_no_processed[0]
		list_hash_visited.append(first.__hash__)
		del list_objects_no_processed[0]

		

		if class_ == first.gettag_class():
			return first

		for neib in first.getLeafs():
			if neib.__hash__ not in list_hash_visited and neib.__hash__ not in list_hash_no_processed:
				list_objects_no_processed.append(neib)
				list_hash_no_processed.append(neib.__hash__)

	return None


# root = Dsyntnode('root')
# v1 = Verb('tataravo')
# root.addLeaf(v1)
# v2 = Verb('bisavo1')
# v3 = Verb('bisavo2')
# v1.addLeaf(v2)
# v1.addLeaf(v3)
# v4 = Verb('neto1')
# v5 = Verb('neto2')
# v6 = Verb('neto3')
# v7 = Verb('neto4')
# v2.addLeaf(v4)
# v2.addLeaf(v5)
# v3.addLeaf(v6)
# v3.addLeaf(v7)
# v10 = Verb('A')
# v11 = Verb('B')
# v9 = Verb('C')
# v8 = Verb('D')
# v15 = Verb('E')
# v13 = Verb('F')
# v14 = Verb('G')
# v12 = Verb('H')
# v4.addLeaf(v8)
# v4.addLeaf(v9)
# v5.addLeaf(v10)
# v5.addLeaf(v11)
# v6.addLeaf(v12)
# v6.addLeaf(v13)
# v7.addLeaf(v14)
# v8.addLeaf(v15)

# print bfs_search(root,'C')






