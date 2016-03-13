from dsyntnode import *
from parser import *

def build_root():
	root = Dsyntnode('root')
	v1 = Verb('tataravo')
	v1.settag_rel("I")
	root.addLeaf(v1)

	v2 = Adverb('bisavo1')
	v2.settag_rel("I")
	v3 = Verb('bisavo2')
	v3.settag_rel("II")
	v3.settag_mode("ind")
	v1.addLeaf(v2)
	v1.addLeaf(v3)


	v4 = Verb('neto1')
	v4.settag_mode("cond")
	v5 = Preposition('neto2')
	v6 = Verb('neto3')
	v7 = Verb('X')
	v7.settag_rel("III")
	v2.addLeaf(v4)
	v2.addLeaf(v5)
	v3.addLeaf(v6)
	v3.addLeaf(v7)


	v10 = Adverb('A')
	v11 = Common_Noun('B')
	v9 = Verb('C')
	v8 = Verb('D')
	v8.settag_mode("imp")
	v8.settag_rel("II")
	v15 = Verb('E')
	v13 = Common_Noun('X')
	v14 = Verb('G')
	v12 = Verb('H')
	v12.settag_mode("cond")
	v12.settag_rel("III")
	v4.addLeaf(v8)
	v4.addLeaf(v9)
	v5.addLeaf(v10)
	v5.addLeaf(v11)
	v6.addLeaf(v12)
	v6.addLeaf(v13)
	v7.addLeaf(v14)
	v8.addLeaf(v15)

	return root

def build_complex_root():
	"""
		in order to see the tree used in this test, access http://mshang.ca/syntree/
		and use as input:  [[V6[[N7[[AJ4[[V4[[N1 ][V1 ]]][N3 ]]][AV4[[N4[[AV1 ][P1 ]]][P2 ]]]]][N9[[AV6[[P5 ][AJ3[[N2 ][V2 ]]][N8[[P4 ][AV5[[P3 ][N5[[AV2 ]]]]]]]]][P6[[V5[[V3 ][N6[[AV3 ][AJ1 ]]]]]]][AJ2 ]]]]]]
		or just print it
	"""
	root = Dsyntnode('root')
	

	#leafs
	n1 = Noun('N1')
	n2 = Noun('N2')
	n3 = Noun('N3')
	v1 = Verb('V1')
	v2 = Verb('V2')
	v3 = Verb('V3')
	p1 = Preposition("P1")
	p1.settag_rel('II')
	p2 = Preposition("P2")
	p3 = Preposition("P3")
	p4 = Preposition("P4")
	p5 = Preposition("P5")
	p5.settag_rel('II')
	av1 = Adverb('AV1')
	av2 = Adverb('AV2')
	av3 = Adverb('AV3')
	aj1 = Adjective('AJ1')
	aj2 = Adjective('AJ2')
	aj2.settag_rel('II')

	#deep 1
	n4 = Noun('N4')
	n4.addLeaf(av1)
	n4.addLeaf(p1)
	n5 = Noun('N5')
	n5.addLeaf(av2)
	n6 = Noun('N6')
	n6.addLeaf(av3)
	n6.addLeaf(aj1)
	n6.settag_rel('II')
	v4 = Verb('V4')
	v4.addLeaf(n1)
	v4.addLeaf(v1)
	aj3 = Adjective('AJ3')
	aj3.addLeaf(n2)
	aj3.addLeaf(v2)

	#deep 2
	v5 = Verb('V5')
	v5.addLeaf(v3)
	v5.addLeaf(n6)
	av4 = Adverb('AV4')
	av4.addLeaf(n4)
	av4.settag_rel('III')
	av4.addLeaf(p2)
	av5 = Adverb('AV5')
	av5.addLeaf(p3)
	av5.addLeaf(n5)
	av5.settag_rel('III')
	aj4 = Adjective('AJ4')
	aj4.addLeaf(v4)
	aj4.addLeaf(n3)

	#deep3
	n7 = Noun('N7')
	n7.addLeaf(aj4)
	n7.addLeaf(av4)
	n8 = Noun('N8')
	n8.addLeaf(p4)
	n8.addLeaf(av5)
	n8.settag_rel('I')
	p6 = Preposition('P6')
	p6.addLeaf(v5)
	
	#deep4
	av6 = Adverb('AV6')
	av6.addLeaf(p5)
	av6.addLeaf(aj3)
	av6.settag_rel('I')
	av6.addLeaf(n8)
	
	#deep5
	n9 = Noun('N9')
	n9.addLeaf(av6)
	n9.addLeaf(p6)
	n9.addLeaf(aj2)

	#deep6
	v6 = Verb('V6')
	v6.addLeaf(n7)
	v6.settag_rel('I')
	v6.addLeaf(n9)
	
	root.addLeaf(v6)
	
	return root

def assert_getAllNodesByTag():
	errors_message = []
	root = build_complex_root()

	


	test0 = root.getAllNodesByTag('class','nothing')
	if len(test0) != 0:
		errors_message.append('getAllNodesByTag(): Should return 0, but was returned %d' % len(test0))

	test01 = root.getAllNodesByTag('class','Verb')
	if len(test01) != 0:
		errors_message.append('getAllNodesByTag(): Should return 0(not case sensitive), but was returned %d' % len(test01))

	test1 = root.getAllNodesByTag('class','verb')
	if len(test1) != 6:
		errors_message.append('getAllNodesByTag(): Should return 6, but was returned %d' % len(test1))

	test2 = root.getAllNodesByTag('class','noun')
	if len(test2) != 9:
		errors_message.append('getAllNodesByTag(): Should return 9, but was returned %d' % len(test2))

	test3 = root.getAllNodesByTag('rel','II')
	if len(test3) != 4:
		errors_message.append('getAllNodesByTag(): Should return 4 for rel=II, but was returned %d' % len(test3))

	test4 = root.getAllNodesByTag('rel','I')
	if len(test4) != 3:
		errors_message.append('getAllNodesByTag(): Should return 3 for rel=I, but was returned %d' % len(test4))

	test5 = root.getAllNodesByTag('rel','III')
	if len(test5) != 2:
		errors_message.append('getAllNodesByTag(): Should return 2 for rel=III, but was returned %d' % len(test5))

	test6 = root.getAllNodesByTag('rel','V')
	if len(test6) != 0:
		errors_message.append('getAllNodesByTag(): Should return 0 for rel=III, but was returned %d' % len(test6))


	if root.getAllNodesByTag('class','noun')[0] is not root.getAllNodesByTag('class','noun')[0]:
		errors_message.append('getAllNodesByTag(): this function has to return a reference not a copy')

	a = root.getAllNodesByTag('class','noun')[0]
	b = root.getAllNodesByTag('class','noun')[0]

	a.settag_lexeme('X')

	if b.gettag_lexeme() != 'X':
		errors_message.append('getAllNodesByTag(): this function has to return a reference not a copy')






	if len(errors_message) == 0:
		print "OK ---- getAllNodesByTag"
	else:
		print "FAIL -- getAllNodesByTag"

	return errors_message

def assert_eq():

	errors_message = []

	root = Dsyntnode('root')
	v1 = Verb('avo')
	root.addLeaf(v1)
	v2 = Verb('filho1')
	v3 = Verb('filho1')
	v1.addLeaf(v2)
	v1.addLeaf(v3)
	v4 = Verb('A')
	v5 = Verb('A')
	v6 = Verb('A')
	v7 = Verb('A')
	v2.addLeaf(v4)
	v2.addLeaf(v5)
	v3.addLeaf(v6)
	v3.addLeaf(v7)

	if v4 != v6:
		errors_message.append('__eq__(): v4 & v6 should be equals: parents equals does matter')

	v3.settag_lexeme('filho2')

	if v4 == v6:
		errors_message.append('__eq__(): v4 & v6 should be differents: parents differents does matter')

	v3.settag_lexeme('filho1')
	v4.settag_tense("past")
	v6.settag_tense("pres")

	if v4 == v6:
		errors_message.append('__eq__(): v4 & v6 should be differents: tense are different "%s" for v4 and "%s" for v6' % (v4.gettag_tense(),v6.gettag_tense()))

	v6.settag_tense("past")
	v2.addLeaf(Verb('A'))

	if v4 != v6:
		errors_message.append('__eq__(): v4 & v6 should be equals: the number of parent sons does not matter')


	v4.addLeaf(Verb('B'))
	v6.addLeaf(Verb('B'))

	if v4 != v6:
		errors_message.append('__eq__(): v4 & v6 should be equals: the number of sons does matter')

	v6.addLeaf(Verb('C'))
	if v4 == v6:
		errors_message.append('__eq__(): v4 & v6 should be differents: the sons have to be equals')

	v6.addLeaf(Verb('B'))

	v3.settag_lexeme('filho2')

	if v4 == v6:
		errors_message.append('__eq__(): v4 & v6 should be differents: the path until the root have to be equal')

	if len(errors_message) == 0:
		print "OK ---- __eq__"
	return errors_message

def assert_copy():
	errors_message = []
	root = Dsyntnode('root')
	v1 = Verb('tataravo')
	root.addLeaf(v1)
	v2 = Adverb('bisavo1')
	v3 = Verb('bisavo2')
	v1.addLeaf(v2)
	v1.addLeaf(v3)
	v4 = Verb("neto")
	v2.addLeaf(v4)
	v5 = Verb("son")
	v4.addLeaf(v5)

	r2 = root.copy()

	result =  (id(r2) != id(root)) and (id(r2.getLeafs()) != id(root.getLeafs()))

	if not result:
		errors_message.append('copy(): objects copied share the same local memory')

	if r2.__str__() != "root[[tataravo[[bisavo1[[neto[[son ]]]]][bisavo2 ]]]]":
		errors_message.append('copy(): the tree are not equals\n expected %s, \nreturned %s' % 
			("root[[tataravo[[bisavo1[[neto[[son ]]]]][bisavo2 ]]]]",r2.__str__()))		


	test2 = root.getLeafs()[0].getLeafs()[0].copy()
	if test2.__str__() != "bisavo1[[neto[[son ]]]]":
		errors_message.append('copy(): Should not copy the grandparents expected %s, \nreturned %s' % 
			("bisavo1[[neto[[son ]]]]",r2.__str__()))	

	test3 = test2.copy()
	test3.settag_rel("III")

	
	
	if test3 == test2:
		errors_message.append('copy(): The trees have different relations, they should be differents')
	
	root = Dsyntnode('root')
	b = Verb('A')
	c = Noun('B')
	root.addLeaf(b)
	b.addLeaf(c)
	root_copy = root.copy()
	
	if b.getParent().__str__() != 'root[[A[[B ]]]]':
		errors_message.append('copy():\n   expected: root[[A[[B ]]]]\n   returned: %s' % b.getParent())



	if len(errors_message) == 0:
		print "OK ---- copy"
	else:
		print "FAIL -- copy"

	
	return errors_message

def assert_getNode():
	root = build_root()
	errors_message = []

	test1 = root.getNode('tataravo')
	if test1 == None:
		errors_message.append('getNode(): One of the top nodes was not found')

	elif test1.gettag_lexeme() != 'tataravo':
		errors_message.append('getNode(): expected: tataravo returned: %s' % test1.gettag_lexeme())


	test2 = root.getNode('E')
	if test2 == None:
		errors_message.append('getNode(): One of leafs nodes was not found')

	elif test2.gettag_lexeme() != 'E':
		errors_message.append('getNode(): expected: E returned: %s' % test2.gettag_lexeme())


	test3 = root.getNode('neto3')
	if test3 == None:
		errors_message.append('getNode(): One of nodes in the middle of the tree was not found')

	elif test3.gettag_lexeme() != 'neto3':
		errors_message.append('getNode(): expected: neto3 returned: %s' % test3.gettag_lexeme())


	test4 = root.getNode('neto10')
	if test4 != None:
		errors_message.append('getNode(): The node "neto10" does not exist in the tree but was found the node %s' % test4.gettag_lexeme())

	#BFS
	root = Dsyntnode('root')
	v1 = Verb('avo')
	root.addLeaf(v1)
	v2 = Verb('A')
	v3 = Adjective('B')
	v1.addLeaf(v2)
	v1.addLeaf(v3)
	v4 = Verb('C')
	v5 = Verb('C')
	v6 = Verb('C')
	v7 = Verb('C')
	v2.addLeaf(v4)
	v2.addLeaf(v5)
	v3.addLeaf(v6)
	v3.addLeaf(v7)
	v8 = Verb('B')
	v4.addLeaf(v8)

	test5 = root.getNode('B')

	if test5 == None:
		errors_message.append('getNode(): Expected: B returned: None')

	elif test5.__name__ == "Verb":
		errors_message.append('getNode(): The search is not a BFS: expected a Adjective returned:Verb')

	if len(errors_message) == 0:
		print "OK ---- getNode"
	return errors_message

def assert_insertNode():
	root = build_root()
	errors_message = []
	y = Verb("Y")

	test1 = root.insertNode('X',y)

	if not test1:
		errors_message.append('insertNode():test1 A node should be inserted')
	
	result1_expected = "root[[tataravo[[bisavo1[[neto1[[D[[E ]]][C ]]][neto2[[A ][B ]]]]][bisavo2[[neto3[[H ][X ]]][X[[G ][Y ]]]]]]]]"
	if root.__str__() != result1_expected:
		errors_message.append('insertNode():result1 The node was inserted but the in the wrong node expected \n:%s,\nbut was returned \n:%s' % (result1_expected,root.__str__()))




	node2 = Noun("bisavo1")
	test2 = root.insertNode('tataravo',node2)
	if not test2:
		errors_message.append('insertNode():test2 A node should be inserted')

	result2_expected = "root[[tataravo[[bisavo1[[neto1[[D[[E ]]][C ]]][neto2[[A ][B ]]]]][bisavo2[[neto3[[H ][X ]]][X[[G ][Y ]]]]][bisavo1 ]]]]"
	if root.__str__() != result2_expected:
		errors_message.append('insertNode():result1 The node was inserted but the in the wrong node expected \n:%s,\nbut was returned \n:%s' % (result2_expected,root.__str__()))





	node3 = Noun("X")
	test3 = root.insertNode('bisavo1',node3)
	if not test3:
		errors_message.append('insertNode():test3 A node should be inserted')

	result3_expected = "root[[tataravo[[bisavo1[[neto1[[D[[E ]]][C ]]][neto2[[A ][B ]]][X ]]][bisavo2[[neto3[[H ][X ]]][X[[G ][Y ]]]]][bisavo1 ]]]]"
	if root.__str__() != result3_expected:
		errors_message.append('insertNode():result1 The node was inserted but the in the wrong node expected \n:%s,\nbut was returned \n:%s' % (result3_expected,root.__str__()))



	if len(errors_message) == 0:
		print "OK ---- insertNode"

	return errors_message

def assert_removeNode():
	root = build_root()
	errors_message = []
	#TODO remove root which has more than 1 leaf

	result = root.removeNode('E')
	
	if type(result) != bool:
		errors_message.append('removeNode():the return result have to be a boolean')

	result1_expected = "root[[tataravo[[bisavo1[[neto1[[D ][C ]]][neto2[[A ][B ]]]]][bisavo2[[neto3[[H ][X ]]][X[[G ]]]]]]]]"
	if root.__str__() != result1_expected:
		errors_message.append('removeNode():removeLeaf expected \n:%s,\nbut was returned \n:%s' % (result1_expected,root.__str__()))

	
	result2_expected = "root[[tataravo[[bisavo1[[D ][C ][neto2[[A ][B ]]]]][bisavo2[[neto3[[H ][X ]]][X[[G ]]]]]]]]"
	root.removeNode("neto1")
	if root.__str__() != result2_expected:
		errors_message.append('removeNode():remove Node with leafs expected \n:%s,\nbut was returned \n:%s' % (result2_expected,root.__str__()))


	result3_expected = "root[[tataravo[[D ][C ][neto2[[A ][B ]]][bisavo2[[neto3[[H ][X ]]][X[[G ]]]]]]]]"
	root.removeNode("bisavo1")
	if root.__str__() != result3_expected:
		errors_message.append('removeNode():remove Node with leaf more than 2 levels sexpected \n:%s,\nbut was returned \n:%s' % (result3_expected,root.__str__()))


	result4_expected = "root[[tataravo[[D ][C ][neto2[[A ][B ]]][bisavo2[[neto3[[H ][X ]]][G ]]]]]]"
	root.removeNode("X")
	if root.__str__() != result4_expected:
		errors_message.append('removeNode():remove node in the end with leafs expected \n:%s,\nbut was returned \n:%s' % (result4_expected,root.__str__()))	
	
	
	result5_expected = "root[[tataravo[[D ][C ][A ][B ][bisavo2[[neto3[[H ][X ]]][G ]]]]]]"
	root.removeNode("neto2")
	if root.__str__() != result5_expected:
		errors_message.append('removeNode():remove node with leafs in the middle expected \n:%s,\nbut was returned \n:%s' % (result5_expected,root.__str__()))	


	result6_expected = "root[[tataravo[[D ][C ][B ][bisavo2[[neto3[[H ][X ]]][G ]]]]]]"
	root.removeNode("A")
	if root.__str__() != result6_expected:
		errors_message.append('removeNode():remove leaf expected \n:%s,\nbut was returned \n:%s' % (result6_expected,root.__str__()))	

	root.removeNode('bisavo2')
	root.removeNode('C')
	root.removeNode('D')
	root.removeNode('B')
	root.removeNode('G')
	root.removeNode('tataravo')

	result7_expected = "root[[neto3[[H ][X ]]]]"
	if root.__str__() != result7_expected:
		errors_message.append('removeNode():remove root which as just one leaf \n:%s,\nbut was returned \n:%s' % (result7_expected,root.__str__()))	

	if len(errors_message) == 0:
		print "OK ---- removeNode"
	else:
		print "FAIL -- removeNode"

	return errors_message

def assert_replaceNode():
	errors_message = []
	
	root = Dsyntnode('root')
	a = Verb('A')
	b = Verb('A')
	c = Verb('A')
	d = Noun('A')
	e = Common_Noun('A')
	f = Verb('B')
	g = Verb('B')
	h = Verb('B')
	i = Noun('B')
	j = Common_Noun('B')

	root.addLeaf(a)
	root.addLeaf(f)
	a.addLeaf(g)
	a.addLeaf(c)
	f.addLeaf(b)
	f.addLeaf(h)
	g.addLeaf(i)
	d.addLeaf(d)
	b.addLeaf(e)
	b.addLeaf(j)

	
	root_copy = root.copy()
	r1 = Verb('C')

	root_copy.replaceNode('A',r1,True)
	

	if root_copy.hasNode('A'):
		errors_message.append('replaceNode():the node was note replaced')

	if root_copy.__str__() != 'root[[C[[B[[B ]]][C ]]][B[[C[[C ][B ]]][B ]]]]':
		errors_message.append('replaceNode():\n   expected root[[C[[B[[B ]]][C ]]][B[[C[[C ][B ]]][B ]]]]\n   returned %s\n' % root_copy.__str__())		

	r1 = Verb('A')	
	root_copy.getLeafs()[0].replaceNode('C',r1)
	
	if root_copy.__str__() != 'root[[A[[B[[B ]]][C ]]][B[[C[[C ][B ]]][B ]]]]':
		errors_message.append('replaceNode():\n   expected root[[A[[B[[B ]]][C ]]][B[[C[[C ][B ]]][B ]]]]\n   returned %s\n' % root_copy.__str__())		

	if len(errors_message) == 0:
		print "OK ---- replaceNode"
	else:
		print "FAIL -- replaceNode"

	return errors_message

def assert_inObj():
	errors_message = []
	v1 = Verb('A')
	v2 = Verb('A')
	n1 = Noun('A')

	

	if not v1.inObj(v2):
		errors_message.append('\nobjIN():test1 - v1 and v2 must be equals')

	if not v1.inObj(n1):
		errors_message.append('\nobjIN():test1 - v1 should be in n1')

	if not n1.inObj(v1):
		errors_message.append('\nobjIN():test1 - n1 should be in v1')

	if not v1.inObj(v2):
		errors_message.append('\nobjIN():test1 - v1 should be in v2')

	v1.settag_tense('past')

	if v1.inObj(v2):
		errors_message.append('\nobjIN():test1 - v1 should not be in v2')

	if not n1.inObj(v1):
		errors_message.append('\nobjIN():test1 - n1 should be in v1')

	v1.settag_rel('I')
	if not n1.inObj(v1):
		errors_message.append('\nobjIN():test1 - n1 should be in v1')

	n1.settag_rel('II')
	if n1.inObj(v1):
		errors_message.append('\nobjIN():test1 - n1 should not be in v1')

	v1.settag_tense("pres")
	if v1.inObj(v2):
		errors_message.append('\nobjIN():test1 - v1 should not be in v2')

	if not v2.inObj(v1):
		errors_message.append('\nobjIN():test1 - v2 should be in v1')

	if len(errors_message) == 0:
		print "OK ---- inObj"
	else:
		print "FAIL -- inObj" 

	return errors_message

def assert_subTreeOf():
	"""
		listDSS
			V1 
			V1[[V2 ][N1 ]]
			V1[[V2[[V3 ][V4 ]]][N1 ]]
			V1[[V2[[V3 ]]][N1 ]]
			V1[[V2[[V3[[N2 ]]]]][N1 ]]
			V1[[V2[[V3 ][V4 ]]][N1[[N3 ][N4 ]]]]
			V1[[V2[[V3[[N2 ]]][V4 ]]][N1[[N3 ][N4 ]]]]

	"""
	errors_message = []
	listDSS = Parser().xml2Tree('test_sub_tree.xml')
	asserts_matrix_file = open('asserts_matrix_sub_tree.txt').read()
	asserts_matrix = []

	asserts_matrix_file = asserts_matrix_file.split("\n")
	for line in asserts_matrix_file:
		table = {'T':True,'F':False}
		
		asserts_matrix.append([table[value] for value in line.split(";")])

 	error_in_matrix = False
	for l in xrange(len(listDSS)):
		for l2 in xrange(len(listDSS)):
			dss1 = listDSS[l]
			dss2 = listDSS[l2]

			if (dss1.subTreeOf(dss2) != None) != asserts_matrix[l][l2]:
				error_in_matrix = True


	if error_in_matrix:
		errors_message.append('\nsubTreeOf(): There are some errors in the matrix asserts')

	

	v1 = Verb('A')
	n1 = Noun('B')
	v1.addLeaf(n1)

	root = Dsyntnode('root')
	root.addLeaf(v1)

	v2 = Verb('A')
	n2 = Noun('B')
	v2.addLeaf(n2)
	
	root2 = Dsyntnode('root')
	root2.addLeaf(v2)

	result1 = root.getLeafs()[0].subTreeOf(root2.getLeafs()[0])

	if result1 == None:
		errors_message.append('\nsubTreeOf():it should return some tree')

	if result1 != None and result1.__str__() != 'A[[B ]]':
		errors_message.append('\nsubTreeOf():result1 \nexpected:A[[B ]]\nreturned:%s\n' % result1.__str__())

	if result1 == root.getLeafs()[0]:
		errors_message.append('\nsubTreeOf():result1 the nodes should not be equals')

	if len(errors_message) == 0:
		print "OK ---- subTreeOf"

	v1 = Verb('A')
	n1 = Noun('A')
	v2 = Verb('A')
	v1.addLeaf(n1)
	v1.addLeaf(v2)

	av1 = Verb('A')
	an1 = Noun('A')
	av2 = Verb('A')
	av1.addLeaf(av2)
	av1.addLeaf(an1)
	

	if (v1.subTreeOf(av1) == None) or (av1.subTreeOf(v1) == None):
		errors_message.append('\nsubTreeOf():The order of the tree should not do difference')

	av3 = Verb('B')
	av1.addLeaf(av3)

	if v1.subTreeOf(av1) == None:
		errors_message.append('\nsubTreeOf():v1 have to be a subset of av1')

	if av1.subTreeOf(v1) != None:
		errors_message.append('\nsubTreeOf():av1 have not to be a subset of v1')


	v1 = Verb('A')
	n1 = Noun('A')
	n2 = Noun('A')
	v1.addLeaf(n1)
	v1.addLeaf(n2)

	av1 = Verb('A')
	an1 = Noun('A')
	av1.addLeaf(an1)

	#TODO
	# how to solve this problem??????????????????
	#     		        	  v 	   							     v
	#             the pattern | have to find 2 subtrees in the tree / \  
	#	          			  n 								   n   n





	



	
	return errors_message

def assert_patternIn():
	
	errors_message = []
	root = build_complex_root()

	##################################
	#
	#		Simple Tests 
	#
	##################################

	classes = ['Verb','Noun','Preposition','Adjective','Adverb']
	expected = [6,9,6,4,6]

	for index in xrange(len(classes)):
		c = classes[index]
		class_ = None
		exec('class_ = %s("nil")' % (c))

		result0 = len(class_.patternIn(root,True))
		if  result0 != expected[index]:
			errors_message.append('\npatternIn():deep=0 class=%s \nexpected %d\nreturned %d' % (c,expected[index],result0))


	##################################
	#
	#		Medium Tests
	#
	##################################

	#TODO do more complicated tests

	#----------------------pattern_test_1
	pattern1 = Verb('nil')
	n1_test = Noun('nil')
	pattern1.addLeaf(n1_test)
	expected1 = ['V6[[N7 ]]','V4[[N1 ]]','V5[[N6 ]]']#,'V6[[N9 ]]'] # VNN|VN problem
	result_t1 = pattern1.patternIn(root,True)


	for f in result_t1:
		if f.__str__() not in expected1:
			errors_message.append('\npatternIn():deep=1 pattern1 the \nvalue "%s" not in %s' % (f.__str__(),str(expected1)))


	if len(result_t1) != len(expected1):
		errors_message.append('\npatternIn():deep=1 pattern1\nexpected 3\nreturned %d' % len(result_t1))

	#----------------------pattern_test_2
	pattern2 = Verb('nil')
	n3_test = Noun('nil')
	pattern2.addLeaf(n3_test)
	aj1_test = Adjective('nil')
	n3_test.addLeaf(aj1_test)
	expected2 = ['V6[[N7[[AJ4 ]]]]','V5[[N6[[AJ1 ]]]]']#,'V6[[N9[[AJ2 ]]]]'] # VNN|VN problem
	result_t2 = pattern2.patternIn(root,True)

	for f in result_t2:
		if f.__str__() not in expected2:
			errors_message.append('\npatternIn():deep=1 pattern1 the \nvalue "%s" not in %s' % (f.__str__(),str(expected2)))
	
	if len(result_t2) != len(expected2):
		errors_message.append('\npatternIn():deep=1 pattern2\nexpected 3\nreturned %d' % len(result_t2))

	#----------------------pattern_test_3
	#pattern_test3
	pattern3 = Adverb('nil')
	n2_test = Noun('nil')
	p1_test = Preposition('nil')
	p2_test = Preposition('nil')
	n2_test.addLeaf(p2_test)
	pattern3.addLeaf(p1_test)
	pattern3.addLeaf(n2_test)
	result_t3 = pattern3.patternIn(root,True)
	expected3 = ['AV4[[P2 ][N4[[P1 ]]]]','AV6[[P5 ][N8[[P4 ]]]]']

	for f in result_t3:
		if f.__str__() not in expected3:
			errors_message.append('\npatternIn():deep=1 pattern1 the \nvalue "%s" not in %s' % (f.__str__(),str(expected3)))

	
	if len(result_t2) != len(expected2):
		errors_message.append('\npatternIn():deep=1 pattern2\nexpected 2\nreturned %d' % len(result_t2))


	##################################
	#
	#		Complex Tests
	#
	##################################
	
	if len(errors_message) == 0:
		print "OK ---- patternIn"

	return errors_message

def assertFactory_cast():
	errors_message = []
	d = Dsyntnode('A')
	d.tag_rel = 'I'

	v = Verb('run')
	v.tag_rel = 'III'
	v.tag_mood = "II"
	v.tag_mood = "b"
	v.tag_mode = "ind"
	v.tag_tense = "pres"
	v.tag_question = "+"
	v.tag_polarity = "neg"

	n = Noun('desk')
	n.tag_rel = 'III'
	n.tag_gender = "fem"
	n.tag_number = "sg"
	n.tag_person = "2nd"

	cn = Common_Noun('person')
	cn.tag_rel = 'III'
	cn.tag_gender = "mas"
	cn.tag_number = "pl"
	cn.tag_person = "2nd"
	cn.tag_article = "no-art"
	cn.tag_ref = "some"

	pn = Proper_Noun('Diego')
	pn.tag_rel = 'III'
	pn.tag_gender = "fem"
	pn.tag_number = "sg"
	pn.tag_person = "1st"
	pn.tag_article = "def"
	pn.tag_ref = "some"

	f = Factory()


	result1 = f.cast(d,'verb')
	if not isinstance(result1,Verb):
		errors_message.append('\nFactory_cast():result1 the new class has to be a Verb')


	if result1.gettag_mode() != 'nil':
		errors_message.append('\nFactory_cast():result1 the mode tag has to be nil')

	if result1.gettag_rel() != 'I':
		errors_message.append('\nFactory_cast():result1 the mode tag has to be I')
	
	result2 = f.cast(d,'noun')
	if not isinstance(result2,Noun):
		errors_message.append('\nFactory_cast():result2 the new class has to be a Noun')

	result3 = f.cast(d,'Common_Noun')
	if not isinstance(result3,Noun):
		errors_message.append('\nFactory_cast():result2 the new class has to be a Common_Noun')

	result4 = f.cast(v,'Dsyntnode')
	if not isinstance(result4,Dsyntnode):
		errors_message.append('\nFactory_cast():result4 the new class has to be a Dsyntnode')

	if result4.gettag_rel() != 'III':
		errors_message.append('\nFactory_cast():result4  the tag rel has to be III')

	if 'tag_tense' in result4.getTags():
		errors_message.append('\nFactory_cast():result4 the tag tense should not exist')

	if result4.__name__ != 'Dsyntnode':
		errors_message.append('\nFactory_cast():result4 the class has to be a Dsyntnode')
	
	result5 = f.cast(v,'Common_Noun')
	if not isinstance(result5,Common_Noun):
		errors_message.append('\nFactory_cast():result5 the new class has to be a Common_Noun')

	if 'tag_tense' in result5.getTags():
		errors_message.append('\nFactory_cast():result5 the tag tense should not exist')

	if result5.__name__ != 'Common_Noun':
		errors_message.append('\nFactory_cast():result5 the class has to be a Common_Noun')

	if len(errors_message) == 0:
		print "OK ---- Factory_cast"

	else:
		print "FAIL ---- Factory_cast"

	return errors_message
	
def testALL():
	errors = []
	errors.extend(assert_subTreeOf())
	errors.extend(assert_getNode())
	errors.extend(assert_eq())
	errors.extend(assert_copy())
	errors.extend(assert_insertNode())
	errors.extend(assert_removeNode())
	errors.extend(assert_replaceNode())
	errors.extend(assert_patternIn())
	errors.extend(assert_inObj())
	errors.extend(assert_getAllNodesByTag())
	errors.extend(assertFactory_cast())

	

	if len(errors) == 0:
		print "No errors were found"
	else:
		print "Were found %d errors" % len(errors)

		for e in errors:
			print e

	

#TODO write heads				
testALL()