from dsyntnode import *
import xmltodict
from collections import OrderedDict


class Parser:

	def __init__(self):
		self.FILE_HEAD_NAME = "dsynts-list" #default
		self.TREE_HEAD_NAME = "dsynts" #default
		self.ELEMENT_HEAD_NAME = "dsyntnode" #default
		self.STOP_NODE = 'root' #TODO in the future remove that
		self.dssTrees = []
		self.xmlObjects = None

	def getListOfTrees(self):
		return self.dssTrees

	def tree2Dic(self,listOfTrees):
		if len(listOfTrees) == 1:
			return self.treeDSS2Dic(listOfTrees[0])
		else:
			ordDict = OrderedDict({self.FILE_HEAD_NAME:OrderedDict({self.TREE_HEAD_NAME:[]})})

			for indexdss in xrange(len(listOfTrees)):
				dss = listOfTrees[indexdss]
				dicDSS = OrderedDict({})
				self.treeDSS2Dic(dss,dicDSS)
				dicDSS['@id'] = '%d' % (indexdss)
				ordDict[self.FILE_HEAD_NAME][self.TREE_HEAD_NAME].append(dicDSS)

			return ordDict

	def treeDSS2Dic(self,root,dic):
		if root.getParent() == None: #.gettag_lexeme() == self.STOP_NODE: 

			if self.ELEMENT_HEAD_NAME in dic:
				dic[self.ELEMENT_HEAD_NAME] = OrderedDict(root.toDic())
	
		if len(root.getLeafs()) > 1:
			
			if type(dic) == list:
				dic.append(OrderedDict(root.toDic()))
				dic[-1][self.ELEMENT_HEAD_NAME] = []

				for l in root.getLeafs():
					self.treeDSS2Dic(l,dic[-1][self.ELEMENT_HEAD_NAME])
			else:
				
				if self.ELEMENT_HEAD_NAME in dic:

					dic[self.ELEMENT_HEAD_NAME][self.ELEMENT_HEAD_NAME] = []
					for l in root.getLeafs():
						self.treeDSS2Dic(l,dic[self.ELEMENT_HEAD_NAME][self.ELEMENT_HEAD_NAME])
				else:
					dic[self.ELEMENT_HEAD_NAME] = OrderedDict(root.toDic())
					dic[self.ELEMENT_HEAD_NAME][self.ELEMENT_HEAD_NAME] = []
					for l in root.getLeafs():
						self.treeDSS2Dic(l,dic[self.ELEMENT_HEAD_NAME][self.ELEMENT_HEAD_NAME])

		elif len(root.getLeafs()) == 1:
			
			if type(dic) == list:
				dic.append(OrderedDict(root.toDic()))
				self.treeDSS2Dic(root.getLeafs()[0],dic[-1])

			else:
				dic[self.ELEMENT_HEAD_NAME] = OrderedDict(root.toDic())
				self.treeDSS2Dic(root.getLeafs()[0],dic[self.ELEMENT_HEAD_NAME])

		else:
			
			if type(dic) == list:
				dic.append(OrderedDict(root.toDic()))
			else:
				dic[self.ELEMENT_HEAD_NAME] = OrderedDict(root.toDic())

	#give a string of xml return a tree strucuture dsynt
	def string2DSStree(self,xml_stream):
		"""
		INPUT:

		<dsynts id="0">
			<dsyntnode polarity="nil" mood="ind" lexeme="sit" question="+" rel="II" mode="nil" tense="past" class="Verb">
				<dsyntnode lexeme="&lt;PRONOUN&gt;" gender="fem" number="sg" person="2nd" rel="I" article="no-art" ref='"anon_noun1579028:crow(CharacterGender.Female)_1"' class="Proper_Noun">
				</dsyntnode>
				<dsyntnode lexeme="on" class="Preposition" rel="ATTR">
					<dsyntnode lexeme="branch" gender="neut" number="sg" person="" rel="II" article="def" ref="$anon_prop a part of something(noun13163250:branch(), anon_noun13104059:tree()_1)_1$" class="Common_Noun">
						<dsyntnode lexeme="tree" gender="neut" number="sg" person="" rel="I" article="no-art" ref="anon_noun13104059:tree()_1" class="Common_Noun">
						</dsyntnode>
					</dsyntnode>
				</dsyntnode>
			</dsyntnode>
		</dsynts>

		OUTPUT = sit[[<PRONOUN> ][on[[branch[[tree ]]]]]]
		"""

		tree = Dsyntnode(self.STOP_NODE)
		self.xmlDSS2Tree(tree,xmltodict.parse(xml_stream)['dsynts'])

		return tree.getLeafs()[0]


	def xmlDSS2Tree(self,root,obj_xml):
		
		if dir(obj_xml)[0] == '_OrderedDict__map':
			
			if '@lexeme' in obj_xml.keys() and Factory().xml2Dsyntnode(obj_xml) != None:
				newLeaf = Factory().xml2Dsyntnode(obj_xml)
				

				root.addLeaf(newLeaf)

				if self.ELEMENT_HEAD_NAME in obj_xml.keys() and len(root.getLeafs()) > 0:
					root = root.getLeafs()[-1]

			for key,value in obj_xml.iteritems():

				if key == self.ELEMENT_HEAD_NAME:
					self.xmlDSS2Tree(root,obj_xml[key])
			
		elif type(obj_xml) == list:

			for i in obj_xml:
				self.xmlDSS2Tree(root,i)

	def xml2Tree(self,xml_file_name):
		
		with open(xml_file_name) as xmlfile:
			self.xmlObjects = xmltodict.parse(xmlfile.read())
			self.FILE_HEAD_NAME  = self.xmlObjects.keys()[0]
			print "parsing xml to tree strucuture...."

			self.TREE_HEAD_NAME = self.xmlObjects[self.FILE_HEAD_NAME].keys()[0]


			if type(self.xmlObjects[self.FILE_HEAD_NAME][self.TREE_HEAD_NAME]) == list: #the file has more than 1 tree
				self.ELEMENT_HEAD_NAME = self.xmlObjects[self.FILE_HEAD_NAME][self.TREE_HEAD_NAME][0].keys()[1]
			else:
				self.ELEMENT_HEAD_NAME = self.xmlObjects[self.FILE_HEAD_NAME][self.TREE_HEAD_NAME].keys()[1]



			for dssXMLindex in xrange(len(self.xmlObjects[self.FILE_HEAD_NAME][self.TREE_HEAD_NAME])):
				tree = Dsyntnode(self.STOP_NODE)
				XMLtreeDSS = self.xmlObjects[self.FILE_HEAD_NAME][self.TREE_HEAD_NAME][dssXMLindex]
				self.xmlDSS2Tree(tree,XMLtreeDSS)
				print tree
				self.dssTrees.append(tree.getDSSTree())

				self.assertParse(self.dssTrees[-1])

		return self.dssTrees

	def treeDSS2xml(self,root):
		
		ordDict = OrderedDict({self.FILE_HEAD_NAME:OrderedDict({self.TREE_HEAD_NAME:OrderedDict({})})})
		self.treeDSS2Dic(root,ordDict[self.FILE_HEAD_NAME][self.TREE_HEAD_NAME])
		return xmltodict.unparse(ordDict)

	def tree2xml(self,listOfTrees):
		if len(listOfTrees) == 1:
			return self.treeDSS2xml(listOfTrees[0])
		else:
			ordDict = OrderedDict({self.FILE_HEAD_NAME:OrderedDict({self.TREE_HEAD_NAME:[]})})
			
			for indexdss in xrange(len(listOfTrees)):
				dss = listOfTrees[indexdss]
				dicDSS = OrderedDict({})
				print '-------------',dss
				self.treeDSS2Dic(dss,dicDSS)
				dicDSS['@id'] = '%d' % (indexdss)
				ordDict[self.FILE_HEAD_NAME][self.TREE_HEAD_NAME].append(dicDSS)

			#print ordDict

			return self.cleanUpXML(xmltodict.unparse(ordDict))

	#in the future think in a more intelligent way to do that
	def cleanUpXML(self,xmlSTRING):

		xmlSTRING = xmlSTRING.replace("></dsyntnode></dsyntnode></dsyntnode></dsyntnode></dsyntnode></dsynts><dsynts id",">\n      </dsyntnode>\n     </dsyntnode>\n    </dsyntnode>\n   </dsyntnode>\n  </dsyntnode>\n </dsynts>\n <dsynts id")
		xmlSTRING = xmlSTRING.replace("></dsyntnode></dsyntnode></dsyntnode></dsyntnode></dsynts><dsynts id",">\n     </dsyntnode>\n    </dsyntnode>\n   </dsyntnode>\n  </dsyntnode>\n </dsynts>\n <dsynts id")
		xmlSTRING = xmlSTRING.replace("></dsyntnode></dsyntnode></dsyntnode></dsynts><dsynts id",">\n    </dsyntnode>\n   </dsyntnode>\n  </dsyntnode>\n </dsynts>\n <dsynts id")
		xmlSTRING = xmlSTRING.replace("></dsyntnode></dsyntnode></dsynts><dsynts id",">\n   </dsyntnode>\n  </dsyntnode>\n </dsynts>\n <dsynts id")

		xmlSTRING = xmlSTRING.replace("></dsyntnode></dsyntnode></dsyntnode></dsyntnode></dsyntnode>",">\n         </dsyntnode>\n        </dsyntnode>\n       </dsyntnode>\n      </dsyntnode>\n     </dsyntnode>")
		xmlSTRING = xmlSTRING.replace("></dsyntnode></dsyntnode></dsyntnode></dsyntnode>",">\n        </dsyntnode>\n       </dsyntnode>\n      </dsyntnode>\n     </dsyntnode>")
		xmlSTRING = xmlSTRING.replace("></dsyntnode></dsyntnode></dsyntnode>",">\n       </dsyntnode>\n      </dsyntnode>\n     </dsyntnode>")
		xmlSTRING = xmlSTRING.replace("></dsyntnode></dsyntnode>",">\n      </dsyntnode>\n     </dsyntnode>")
		xmlSTRING = xmlSTRING.replace("></dsyntnode><dsyntnode ",">\n       </dsyntnode>\n       <dsyntnode ")
		xmlSTRING = xmlSTRING.replace("><dsyntnode ",">\n       <dsyntnode ")
		xmlSTRING = xmlSTRING.replace('b">\n       <dsyntnode','b">\n         <dsyntnode')
		xmlSTRING = xmlSTRING.replace('">\n       <dsyntnode','">\n      <dsyntnode')

		# xmlSTRING = xmlSTRING.replace('<dsynts-list><dsynts ','<dsynts-list>\n  <dsynts ')
		# xmlSTRING = xmlSTRING.replace('></dsynts><dsynts','>\n  </dsynts>\n  <dsynts')
		# for i in xrange(xmlSTRING.count('<dsynts id=')):
		# 	xmlSTRING = xmlSTRING.replace('<dsynts id="%d"><dsyntnode ' % i,'<dsynts id="%d">\n    <dsyntnode ' % i)
		# xmlSTRING = xmlSTRING.replace('</dsyntnode></dsyntnode></dsyntnode></dsyntnode>\n  </dsynts>','\n            </dsyntnode>\n          </dsyntnode>\n        </dsyntnode>\n      </dsyntnode>\n  </dsynts>')		
		# xmlSTRING = xmlSTRING.replace('</dsyntnode></dsyntnode></dsyntnode>\n  </dsynts>','\n          </dsyntnode>\n        </dsyntnode>\n      </dsyntnode>\n  </dsynts>')		
		# xmlSTRING = xmlSTRING.replace('</dsyntnode></dsyntnode>\n  </dsynts>','\n        </dsyntnode>\n      </dsyntnode>\n  </dsynts>')
		# #xmlSTRING = xmlSTRING.replace('></dsyntnode>','>\n      </dsyntnode>')
		# xmlSTRING = xmlSTRING.replace('</dsyntnode></dsyntnode><dsyntnode ','          </dsyntnode>\n        </dsyntnode>\n      <dsyntnode ')
		# xmlSTRING = xmlSTRING.replace('></dsyntnode><dsyntnode ','>\n        </dsyntnode>\n        <dsyntnode ')
		# xmlSTRING = xmlSTRING.replace('><dsyntnode ','>\n      <dsyntnode ')


		return xmlSTRING

	def assertParse(self,treeDSS):
		"""
			This method verify if the conversion XML format to Tree format, and Tree format to XML format 
			working well. In other words, if there is not loss of information between conversion.
		"""

		a = self.treeDSS2xml(treeDSS)
		a = xmltodict.parse(a)
		treeDSSparsed = Dsyntnode(self.STOP_NODE)
		self.xmlDSS2Tree(treeDSSparsed,a['dsynts-list']['dsynts'])
		t1 = treeDSS
		
		if treeDSS.__str__() != treeDSSparsed.getDSSTree().__str__():
			raise NameError('Error to parser XML. Blacket Trees are differents')

		if treeDSS != treeDSSparsed.getDSSTree():
			raise NameError('Error to parser XML. The tree structure are differents')

		print 'Verifying Tree: ',treeDSS
		print 'Depth = %d\n%s' % (treeDSS.getDepth(),"-"*80)

# xml_stream = """
# <dsynts id="0">
#       <dsyntnode polarity="nil" mood="ind" lexeme="sit" question="+" rel="II" mode="nil" tense="past" class="Verb">
#          <dsyntnode lexeme="&lt;PRONOUN&gt;" gender="fem" number="sg" person="2nd" rel="I" article="no-art" ref='"anon_noun1579028:crow(CharacterGender.Female)_1"' class="Proper_Noun">
#        </dsyntnode>
#        <dsyntnode lexeme="on" class="Preposition" rel="ATTR">
#       <dsyntnode lexeme="branch" gender="neut" number="sg" person="" rel="II" article="def" ref="$anon_prop a part of something(noun13163250:branch(), anon_noun13104059:tree()_1)_1$" class="Common_Noun">
#       <dsyntnode lexeme="tree" gender="neut" number="sg" person="" rel="I" article="no-art" ref="anon_noun13104059:tree()_1" class="Common_Noun">
#      </dsyntnode>
#     </dsyntnode>
#    </dsyntnode>
#   </dsyntnode>
#  </dsynts>"""
# p = Parser()
# print p.string2DSStree(xml_stream)
