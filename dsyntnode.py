from bfs import *
from tagstypes import *


#
#  when the tag is nil it's means that that tag does not have any regular value
#
class Dsyntnode(object):
	__name__ = "Dsyntnode"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		self.tag_lexeme = tag_lexeme
		self.parent = None
		self.tag_rel = tag_rel
		self.leafs = []
		self.class_ = self.__name__.lower()

	def gettag_lexeme(self):
		return self.tag_lexeme

	def settag_lexeme(self,tag_lexeme):
		self.tag_lexeme = tag_lexeme

	def settag_rel(self,tag_rel):

		if tag_rel not in TAG_RELATION_VALUES:
			print "[%s]%d%s" % (tag_rel,len(tag_rel),""==tag_rel)
			raise NameError("Tag rel informed does not exit in RealPro")

		self.tag_rel = tag_rel

	def gettag_rel(self):
		return self.tag_rel

	def gettag_class(self):
		return self.class_

	def addLeaf(self,leaf):
		leaf.setParent(self)
		self.leafs.append(leaf)

	def insertLeaf(self,index,leaf):
		leaf.setParent(self)
		self.leafs.insert(index,leaf)

	# #ambiguity problem: using bsf to find the nearest lexeme
	# #@old_lexeme = the lexeme of the old node that will be replaced
	# #@node = will replace the old node
	# def replaceLeaf(self,old_lexeme,node):
	# 	"""
	# 		Replace a leaf of a node.
	# 		The leaf which will be replaced is a son of which call this function
	# 		Is used old_lexeme, because is the only one that ussually is not dublicated in the same node 

	# 	"""
		
	# 	for index in xrange(len(self.getLeafs())):
			
	# 		if self.leafs[index].gettag_lexeme() == old_lexeme:
				
	# 			for l in self.leafs[index].getLeafs():
	# 				node.addLeaf(l)
	# 			self.leafs[index] = node
	# 			return True
	# 	return False

	def getLeafs(self):
		return self.leafs

	def setParent(self,parent):
		self.parent = parent

	def getParent(self):
		return self.parent

	def getTags(self):
		"""
		 Return all atributes that the class has, which start with 'tag_'
		"""
		all_variables = vars(self)
		tags = []
		
		for variable in all_variables:
			if "tag_" in variable:
				tags.append(variable)

		return tags

	#ambiguity problem: using bsf to find the nearest lexeme
	def getNode(self,lexeme):
		return bfs_search(self,lexeme)

	def getFirstNodeByTag(self,tag_name,tag_value):
		nodes = self.getAllNodesByTag(tag_name,tag_value)

		if nodes == []:
			return None
		return nodes[0]

	#for class the tag_value has to be the exact value in __name__
	def getAllNodesByTag(self,tag_name,tag_value):
		"""
			return a reference of the object
		"""

		if tag_name == "class":
			return self.getAllClass(tag_value)

		tag_name_normalized = 'tag_'+tag_name
		tag_name_value = getattr(self,tag_name_normalized)
		
		
		if self != None:
			listOfNodes = []

			if tag_name_normalized in self.getTags() and tag_name_value == tag_value:
				listOfNodes = [self]
			
			for r in self.getLeafs():
				result = r.getAllNodesByTag(tag_name,tag_value)
				if result != []:
					listOfNodes.extend(result)
			
			return listOfNodes

		else:
			return []

	

	#class_type has to be the exact value in __name__
	def getAllClass(self,class_type):
		#print class_type,self.gettag_class()

		if len(self.getLeafs()) > 0:
			result = []

			if class_type == self.gettag_class():
				result = [self]


			for r in self.getLeafs():
				sub_result = r.getAllClass(class_type)

				if sub_result != []:
					result.extend(sub_result)
			
			return result

		elif class_type == self.gettag_class():
			return [self]

		else:
			return []

	def walkTree(self):

		if len(self.getLeafs()) == 0:
			return self.gettag_lexeme()+" "

		else:
			result = self.gettag_lexeme()+"["
			for r in self.getLeafs():
				result += "["+r.walkTree()+"]"
			return result+"]"

	#TODO modify this method
	def walkTreeFull(self):
		if len(self.getLeafs()) == 0:
			return str(vars(self))
		else:
			result = str(vars(self))+"["
			for r in self.getLeafs():
				result += "["+r.walkTreeFull()+"]"
			return result+"]"

	def hasNode(self,lexeme):
		return self.getNode(lexeme) != None

	#@asUnique=True promove only one node. Then increase the tree as showed bellow in the figures 1.b and 1.d
	#TODO review it
	#TODO write tests
	def promoveNode(self,node,asUnique=False):
		"""

			___ 					___ 			 ___  		 			 ___
		   | A |				   | A |			| A |			   		| A |
		    ---						---  		 	 ---  		 			 ---
			 |						 |				  |						  |
			___ 					___ 		 	 ___  ___ 				 ___
		   | B |				   | B | 			| B || X |		     	| X |
		    ---						---  two promo.	 ---  --- three promo.   ---
		     |		one promotion	 |		====>	  |		       ====>      |				...
		     |          ====>		___  			 ___ ___ 				 ___
		___ ___ ___ 			   | X |			| C | D |				| B |
	   | C | D | X |				---  			 --- --- 				 --- 
		--- --- ---					 |										  |
							   	  ___ ___ 									___ ___
							     | C | D | 								   | C | D | 
								  --- --- 		 							--- --- 
		 Figure 1.a 			Figure 1.b 			Figure 1.c 			 Figure 1.d
		"""


		#1 - add C and D as leafs of X (the parent of C and D are changed automatically in the addLeaf function)
		#2 - Change the leafs of B to only X
		#--------not as unique------
		#3 - 

		B = node.getParent()

		if B == None or not B.hasNode(node.gettag_lexeme()):
			return False


		leafs_index = 0

		for leafs_index in xrange(len(B.getLeafs())):
			#print len(B.getLeafs())
			leafOfB = B.getLeafs()[min(leafs_index,len(B.getLeafs())-1)]

			if leafOfB.gettag_lexeme() != node.gettag_lexeme():
				leafOfB.setParent(None)
				node.addLeaf(leafOfB)
				print "before",len(B.getLeafs())
				B.removeSon(leafOfB.gettag_lexeme())
				print "after",len(B.getLeafs())

		return True

	#ambiguity problem: using bsf to find the nearest lexeme
	def insertNode(self,parent_lexeme,node):
		nodeFound = self.getNode(parent_lexeme)

		if nodeFound != None:
			nodeFound.addLeaf(node)
			return True
		return False

	#what about the patternIn?
	def replaceAlls(self,old_lexeme,tag_name,tag_value):
		#print parent_lexeme,self.gettag_lexeme(),parent_lexeme==self.gettag_lexeme()

		if self.gettag_lexeme() == old_lexeme:
			setattr(self,tag_name,tag_value)
			return True

		elif len(self.getLeafs()) == 0:
			return False
			
		else:
			result = False
			for r in self.getLeafs():
				result = r.replaceAlls(old_lexeme,tag_name,tag_value) or result
			return result

	#TODO review this function
	def replaceNode(self,old_lexeme,new_node,recursively=False):
		
		oldnodes = self.getAllNodesByTag('lexeme',old_lexeme)

		if len(oldnodes) == 0:
			return False

		if not recursively:
			if self.gettag_lexeme() != old_lexeme:
				return False
			else:
				parent = self.getParent()
				for leaf in self.getLeafs():
					new_node.addLeaf(leaf)
				indexNewNode = self.getIndex()
				
				parent.removeSon(old_lexeme)
				parent.insertLeaf(indexNewNode,new_node)
		else:

			for oldnode in oldnodes:

				parent = oldnode.getParent()
				copynode = new_node.copy()
				for leaf in oldnode.getLeafs():
					copynode.addLeaf(leaf)
				
				indexNewNode = oldnode.getIndex()
				if parent != None:
					# print '-'*20
					# print 'SELF',self
					# print 'NEWNODE',new_node
					# print 'COPYNODE',copynode
					# print 'ORIGINAL PARENT      ',parent
					parent.removeSon(old_lexeme)
					# print '     AFTER REMOVE SON',parent
					parent.insertLeaf(indexNewNode,copynode)
					# print '     AFTER INSERT SON',parent
					# print '-'*20
				#else:


		return True

	def isLeaf(self):
		return len(self.getLeafs()) == 0

	
	def popSon(self):
		return self.getLeafs().pop()

	#ambiguity problem
	def removeSon(self,lexeme):

		for index_leaf in xrange(len(self.getLeafs())):

			if self.getLeafs()[index_leaf].gettag_lexeme() == lexeme:
				del self.getLeafs()[index_leaf]
				return True

		return False

	#remove all leafs
	def removeLeafs(self):

		for l in self.leafs:
			l.setParent(None)

		for l in self.leafs:
			print l.getParent()

		self.leafs = []

	#return the index of the node in the list of his parent sons
	#if itself does not has a parent the value returned will be -1
	def getIndex(self):

		if self.getParent() != None:
			for index in xrange(len(self.getParent().getLeafs())):
				if self == self.getParent().getLeafs()[index]:
					return index

		return -1

	#ambiguity problem: using bsf to find the nearest lexeme
	def removeNode(self,lexeme):
		"""
			differently of popSon and removeSon, removeNode remove a node of a tree and reorganize it


			___ 			  ___ 				   ___  		 		 ___
		   | A |		     | A |				  | A |			   		| A |
		    ---				  ---  		 		   ---  		 		 ---
			 |				   |			 		|					  |
			___ 		___   ___  ___ 		 	 ___ ___ 				___ ___
		   | X | ====> | C | | D || E |			| X | C |   ====>      | D | C |
		    ---			---   ---  ---           --- ---	            --- ---
		     |			 	                      |     |				     |
		     |          			 			___	  ___ ___ 			  ___  ___
		___ ___ ___ 			   	   		   | D | | E | F |		     | E || F |
	   | C | D | E |			 				---   --- --- 			  ---  --- 
		--- --- ---					
		 Figure 2.a 			Figure 2.b 			Figure 2.c 			 Figure 2.d
		"""
		if self.isLeaf():
			return True#self.removeSon(lexeme)

		node = self.getNode(lexeme)
		

		if node == None:
			return False
		
		print '===========================',self

		for leafs_index in xrange(len(node.getLeafs())):

			leaf = node.getLeafs()[leafs_index]
			leaf.setParent(node.getParent())
			node.getParent().insertLeaf(node.getIndex(),leaf)

		print '=========================',self

		for index_leaf in xrange(len(node.parent.getLeafs())):
			
			if node.parent.getLeafs()[index_leaf].gettag_lexeme() == lexeme:
				print '===============',self
				for shift_index in xrange(index_leaf,len(node.getParent().getLeafs())-1):
					print '========',self
					node.getParent().getLeafs()[shift_index] = node.getParent().getLeafs()[shift_index + 1]
					print '========',self
				node.parent.getLeafs().pop()
				print '========',self,'NODE',node

				print 'before',node,len(node.getLeafs())
				#node.removeLeafs() TODO
				node.leafs = []
				print 'after',node,'PARENT',node.getParent()
				return True#node


	
	def getDepth(self):
		"""
			A node of no leafs has depth 0
		"""

		if self == None:
			return 0

		else:
			subDepths = [0]

			for r in self.getLeafs():
				subDepths.append(r.getDepth() + 1)

			return max(subDepths)

	def getHight(self):
		if self.getParent() == None:
			return 0

		else:
			return self.getParent().getHight() + 1

	def getComplexity(self):
		return self.getDepth() + self.getHight()

	#TODO review that
	def getPath(self):

		if self.getParent() == None:
			return ''

		else:
			return self.getParent().getPath()+','+self.getParent().gettag_lexeme()

	#TODO review that
	def toDic(self):
		items = {}

		for tag in self.getTags():
			tag_in_xml = '@'+tag.split("_")[1] #tag_rel to @rel
			items[tag_in_xml] = getattr(self,tag)
		items['@class'] = self.__name__
		return items


	def getDSSTree(self):

		if self == None:
			return None

		while self.getParent() != None:
			self = self.getParent()

		if len(self.getLeafs()) > 1:
			raise NameError("The Dsynt Tree has more than 1 root")

		#print self.getLeafs()
		return self.getLeafs()[0]

	#TODO write documentation
	def diff(self,obj):
		
		if ('__name__' not in dir(obj)) and ('__name__' not in dir(self)):
			return ""
		elif ('__name__' not in dir(obj)):
			return "None"

		elif obj.__name__ != self.__name__:
			return "Names"

		elif obj.gettag_lexeme() != self.gettag_lexeme():
			return "Lexemes: %s != %s" %(obj.gettag_lexeme(),self.gettag_lexeme())

		elif len(obj.getTags()) != len(self.getTags()):
			return "Tags: %d != %d" % (len(obj.getTags()),(self.getTags()))

		elif len(obj.getLeafs()) != len(self.getLeafs()):
			return "Leafs: %d != %d" % (len(obj.getLeafs()),len(self.getLeafs()))

		elif obj.getPath() != self.getPath():
			return "Paths: %s != %s" % (obj.getPath(),self.getPath())

		elif not self.inObj(obj):
			return "Tags differents"

		else:
			isEqual = True
			
			
			for index_leaf in xrange(len(self.getLeafs())):
				isEqual = isEqual and (self.leafs[index_leaf] == obj.getLeafs()[index_leaf])
				if not isEqual:
					result = "Leafs: %s != %s" % (self.leafs[index_leaf].gettag_lexeme(),obj.getLeafs()[index_leaf].gettag_lexeme())
					result += "|"+self.leafs[index_leaf].diff(obj.getLeafs()[index_leaf])
					return result
			
			if isEqual:
				return ""
			else:
				return "Tags Values: differents"

	#TODO explain better
	def inObj(self,obj):
		"""
			If all atributes not nil of self are equal to obj the result will be TRUE
			this functions reject the type of class. It analize only the atributes
			Example

			X.article = 'A'
			X.lexeme  =  'B'
			X.rel     = 'nil'

			Y.article = 'A'
			Y.lexeme = 'nil'
			Y.rel = 'D'
			Y.mode = 'nil'

			Z.lexeme = 'A'
			Z.article = 'A'
			Z.rel = 'D'

			X.inObj(Y) = False
			Y.inObj(X) = False

			X.inObj(Z) = False
			Z.inObj(X) = False

			Y.inObj(Z) = True
			Z.inObj(Y) = False


		"""

		for tag in self.getTags():
			if getattr(self,tag) != 'nil' and not hasattr(obj,tag):
				return False

			elif getattr(self,tag) != 'nil':
				if getattr(self,tag) != getattr(obj,tag):
					return False

		return True

	#@ANALISE_TYPE_CLASS 
	#			Consider the type of the class in the comparations
	#TODO explain better
	def subTreeOf(self,tree,ANALISE_TYPE_CLASS=False):
		"""
			Verify if a tree is a subtree of another and return the subtree of .
			This function return a subtree, by using the patterns.
			
			TODO: write an example by shows xml files

			Example.

				A.subTreeOf(B)
				all atributes of the nodes respectives of B are compied to A


						TREE(B) 						 Subtree pattern(A)
				     ____________ 						 ______________
					|Noun rel:'x'|						|Verb rel:'nil'|			
				     ------------						 --------------
							|							 |        |					
					 ____________				 ______________    ________________													
					|Verb rel:'a'|				|Verb rel:'nil'|  |Noun tense:'nil'|		
					 ------------ 				 --------------    ----------------					
					  |        |
		    ____________    _________________														
		   |Verb rel:'b'|  |Noun tense:'past'|	
		    ------------    -----------------					
					
		          Figure 3.a 							Figure 3.b 	

						Subtree after copy atributes
				   	     ______________
						|Verb rel:'a'|			
				    	 --------------
						 |           |					
				 ______________    _________________													
				|Verb rel:'b'  |  |Noun tense:'past'|		
				 --------------    -----------------	

				 Figure 3.c 					
					  
		    													
		   
		    



		"""
																			# A OR NOT B
																			# A = tree.gettag_class() == self.gettag_class()
																			# B = ANALISE_TYPE_CLASS
																			#
																			#  A  B   A OR NOT B
																			#  T  T  	   T
																			#  T  F        T
																			#  F  T        F
																			#  F  F        T
		
		if self.inObj(tree) and len(self.getLeafs()) == 0 and ((tree.gettag_class() == self.gettag_class()) or (not ANALISE_TYPE_CLASS)):
			node = Factory().instanceClass(self.gettag_class())
			node.setATTRfrom(tree)

			return node

		elif len(self.getLeafs()) > len(tree.getLeafs()):
			return None

		elif self.inObj(tree) and (tree.gettag_class() == self.gettag_class() or (not ANALISE_TYPE_CLASS)):
			node = Factory().instanceClass(self.gettag_class())
			node.setATTRfrom(tree)
			count = 0
			

			for f in self.getLeafs():
				subtree = None
				index_leafs = 0

				while subtree == None and index_leafs < len(tree.getLeafs()):
					t = tree.getLeafs()[index_leafs]
					subtree = f.subTreeOf(t,ANALISE_TYPE_CLASS)
					index_leafs += 1
					
				
				if subtree != None:
					node.addLeaf(subtree)
			
			if len(node.getLeafs()) == len(self.getLeafs()):
				return node

			return None
		else:
			return None
		
		
	#@ANALISE_TYPE_CLASS 
	#			Consider the type of the class in the comparations
	#TODO explain better
	def patternIn(self,tree,ANALISE_TYPE_CLASS=False):
		"""
			Diferently from subTreeOf, pattern find all subtrees that exist in a tree.

			**** See the test of this function(file:test_dsyntnode.py) for best understanding"
		"""
		listOfpatterns = []

		
		if len(tree.getLeafs()) == 0:
			sub = self.subTreeOf(tree,ANALISE_TYPE_CLASS)
			if sub != None:
				return [sub]
			else:
				return []

		else:

			result = []
			sub = self.subTreeOf(tree,ANALISE_TYPE_CLASS)
			
			if sub != None:
				result = [sub]

			for r in tree.getLeafs():
				temp = self.patternIn(r,ANALISE_TYPE_CLASS)
				if temp != []:
					
					for t in temp:
						result.append(t)
			
			return result

		return listOfpatterns

	def getDIFF(self,obj):
		differences = []

		for tag in self.getTags():
			if tag != "nil" and (hasattr(obj,tag) and getattr(obj,tag) != "nil"):
				if getattr(self,tag) != getattr(obj,tag):
					differences.append(tag)

		return differences

	def __ne__(self,obj):
		
		return not (self == obj)

	def __eq__(self,obj):
		
		return len(self.diff(obj)) == 0
		
		
	def __str__(self):
		return self.walkTree()

	#the copy is botton-down. Thus, everything from the node to the leafs are copied, but not his grantparents
	def copy(self):

		copyNode = Factory().instanceClass(self.gettag_class())

		for l in self.getLeafs():
			copyNode.addLeaf(l.copy())

		copyNode.setATTRfrom(self)
		

		if self.getParent() != None:
			parent = Factory().instanceClass(self.getParent().gettag_class())
			parent.setATTRfrom(self.getParent())
			copyNode.setParent(parent)
			copyNode.getParent().setParent(None)

		return copyNode

	def setATTRfrom(self,obj):

		for tag in self.getTags():
			if hasattr(obj,tag):
				setattr(self,tag,getattr(obj,tag))

class Symbol(Dsyntnode):
	__name__ = "Symbol"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		super(Symbol, self).__init__(tag_lexeme,tag_rel)

class Particle(Dsyntnode):
	__name__ = "Particle"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		super(Particle, self).__init__(tag_lexeme,tag_rel)


class ATTR(Dsyntnode):
	__name__ = "ATTR"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		super(ATTR, self).__init__(tag_lexeme,tag_rel)


class Verb(Dsyntnode):
	
	__name__ = "Verb"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		super(Verb, self).__init__(tag_lexeme,tag_rel)
		self.tag_mood = "nil"
		self.tag_mode = "nil"
		self.tag_tense = "nil"
		self.tag_question = "nil"
		self.tag_polarity = "nil"

	def settag_mood(self,mood):
		self.tag_mood = mood

	def gettag_mood(self):
		return self.tag_mood

	def settag_mode(self,mode):

		if mode == "":
			return

		if mode not in TAG_MODE_VALUES:
			raise NameError("mode informed to the verb does not exist in RealPro")

		self.tag_mood = mode

	def gettag_mode(self):
		return self.tag_mode

	def settag_tense(self,tense):
		if tense == "":
			return

		if tense not in TAG_TENSE_VALUES:
			raise NameError("The tense informed does not exist in RealPro")

		self.tag_tense = tense

	def gettag_tense(self):
		return self.tag_tense

	def settag_question(self,question):
		self.tag_question = question

	def gettag_question(self):
		return self.tag_question

	def settag_polarity(self,polarity):
		if polarity == "":
			return

		self.tag_polarity = polarity

	def gettag_polarity(self):
		return self.tag_polarity

class Modal(Verb):
	__name__ = "Modal"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		super(Modal, self).__init__(tag_lexeme,tag_rel)
class Adverb(Dsyntnode):

	__name__ = "Adverb"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		super(Adverb, self).__init__(tag_lexeme,tag_rel)
		self.tag_position = "nil"

	def settag_position(self,position):
		self.tag_position = position


	def gettag_position(self):
		return self.tag_position

class Noun(Dsyntnode):
	
	__name__ = "Noun"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		super(Noun, self).__init__(tag_lexeme,tag_rel)
		self.tag_gender = "nil"
		self.tag_number = "nil"
		self.tag_person = "nil"

	def settag_gender(self,gender):
		self.tag_gender = gender

	def gettag_gender(self):
		return self.tag_gender

	def settag_number(self, number):
		self.tag_number = number

	def gettag_number(self):
		return self.tag_number

	def settag_person(self,person):
		self.tag_person = person

	def gettag_person(self):
		return self.tag_person

class Common_Noun(Noun):

	__name__ = "Common_Noun"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		super(Common_Noun, self).__init__(tag_lexeme,tag_rel)
		self.tag_article = "nil"
		self.tag_ref = "nil"
		self.tag_pro = ""

	def settag_article(self,article):
		self.tag_article = article

	def gettag_article(self):
		return self.tag_article

	def settag_ref(self,ref):
		self.tag_ref = ref

	def gettag_ref(self):
		return self.tag_ref

	def settag_pro(self,pro):
		self.tag_pro = pro

	def gettag_pro(self):
		return self.tag_pro

class Proper_Noun(Common_Noun):
	__name__ = "Proper_Noun"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		super(Proper_Noun, self).__init__(tag_lexeme,tag_rel)

class Coordinating_Conj(Dsyntnode):
	__name__ = "Coordinating_Conj"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		super(CoordinatingConj, self).__init__(tag_lexeme,tag_rel)

class Preposition(Dsyntnode):
	__name__ = "Preposition"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		super(Preposition, self).__init__(tag_lexeme,tag_rel)

class Adjective(Dsyntnode):
	__name__ = "Adjective"

	def __init__(self,tag_lexeme,tag_rel="nil"):
		super(Adjective, self).__init__(tag_lexeme,tag_rel)
		self.tag_starting_point="nil"

	def settag_starting_point(self,starting_point):
		self.tag_starting_point = starting_point

	def gettag_starting_point(self):
		return self.tag_starting_point

class Factory: #TODO clean up it

	#TODO - write a code to not be necessary parse the all parameters of a class.

	def fillClass(self,mark_xml):
		if mark_xml['@lexeme'].lower() in ['can','might','could','should','would','ought','need','may']:
			mark_xml['@class'] = 'Modal'
			return True
		return False

	def xml2Dsyntnode(self,mark_xml):

		if '@class' not in mark_xml:
			#TODO to can not be here

			if not self.fillClass(mark_xml):
				mark_xml['@class'] = 'Dsyntnode'
				#raise NameError("The tag @class does not exist in the mark ||<%s>||" % str(mark.values()))

		DSSnode = self.instanceClass(mark_xml['@class'])

		#set the atributs of the class
		for tag in DSSnode.getTags():
			tag_in_xml = '@'+tag.split("_")[1] #tag_rel to @rel
			#print tag_in_xml, tag_in_xml in mark_xml,mark_xml
			if tag_in_xml in mark_xml:
				#print 1/0
				#setattr(DSSnode,tag,mark_xml[tag_in_xml])
				exec("DSSnode.set%s('%s')" % (tag,mark_xml[tag_in_xml]))
		#print DSSnode.walkTreeFull()


		return DSSnode

	def instanceClass(self,class_type):
		newClass = None
		class_type = class_type.upper()
		
		if class_type != 'ATTR':
			class_type = class_type[0].upper()+class_type[1:].lower()

			if "_" in class_type: #change Common_noun to Common_Noun|Coordinating_Conj to Coordinating_Conj:
				class_type = class_type.split("_")
				class_type = "%s_%s%s" % (class_type[0],class_type[1][0].upper(),class_type[1][1:])

		exec("newClass = %s('')" % (class_type))

		return newClass

	def cast(self,obj,newTypeClass):
		newClass = self.instanceClass(newTypeClass)

		for tag in obj.getTags():
			if tag in newClass.getTags():
				setattr(newClass,tag,getattr(obj,tag))

		return newClass
