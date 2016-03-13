#PROBLEM WITH MODALS 
#START THE NEXT STEP (QUESTION ANSWERING)

import random
import os
import config_MD
from dsyntnode import *
from parser import *
from bfs import *
from qa import *

class ContentPlanner:

	def __init__(self,xmlDsyntsFile="sample_2.xml"):
		print "\n\n%sCONTENT PLANNER%s\n\n" % ('='*30,'='*30)

		self.parser_dsynt = Parser()
		XML_DIR = config_MD.PATH_TREE+'XML_Files'+os.sep
		self.parser_dsynt.xml2Tree(XML_DIR+xmlDsyntsFile)
		self.listOfDSS = self.parser_dsynt.getListOfTrees()
		


	def setListDSS(self,listOFdsynts):
		self.listOfDSS = listOFdsynts

	def getListDSS(self):
		return self.listOfDSS 

	#TODO: Need review, find a way to do it automatically by reading a script
	def applyTagQuestion(self,dss,type_question=''):
		"""
			 find the first verb and noun in the tree.
			 build the tree as following

			 		   ********** Framework **********
							   ________
							  |'' or BE| +(polarity = neg) ?(question=+)
							   --------
								|
							 ___ ___
							| P | D |  P=prononoun D= Dsynt
							 --- ---
								  |
								 ___
								| , | 
								 ---

					********** Example **********

						 _____												
						| sat |				         ________			
						 -----				        |'' or BE| 			
						   |				         --------			
					 ____ ___						 / \		
					|crow|on |					_____   ___			
					 ---- ---				   | CROW| |sat|
						   |		===>	    -----   ---
						 ______						  /  |  \
						|branch|				  ____  ___  ___	
						 ------				     |crow||on || , |
						   |				      ----  ---  ---	
						 ____							 |
						|tree|						   ______
						 ----						  |branch|
													   ------
													     |
													   ____
													  |tree|
													   ----


		"""
		blankVerb = Verb('nil') 
		searchVerbs = dss.getAllNodesByTag('class','verb')
		searchNouns = dss.getAllNodesByTag('class','common_noun')

		#print searchVerbs,searchNouns,dss.gettag_class()
		#the dsynt have to have a noun and verb
		if searchVerbs == [] or searchNouns == []:
		    return dss 

		firstVerb = searchVerbs[0]
		firstNoun = searchNouns[0]

		#set the blankVerb atributes by coping the values of firstVerb
		blankVerb.setATTRfrom(firstVerb) 
		blankVerb.settag_polarity('neg') #for the tag question "do not the crow"
		blankVerb.settag_question('+') #is a question  "do not the crow?"
		blankVerb.settag_lexeme('') #have to be blank. It is a trick. "do not '' the crow?"
		
		if type_question == 'BE':
			blankVerb.settag_lexeme('be')

		pronoun_TQ = Common_Noun('nil')
		pronoun_TQ.setATTRfrom(firstNoun)
		pronoun_TQ.settag_rel('II') #why have to be II ?????? TODO

		blankVerb.addLeaf(pronoun_TQ)

		comma = Symbol(',')
		comma.settag_rel('APPEND')

		dss.addLeaf(comma)
		blankVerb.addLeaf(dss)



		print dss,'MODIFIED'
		return blankVerb

	
	def identifyTypeTagQuestion(self,dss):
		

		if dss.getNode('be') != None:
			return 'BE'

		if len(dss.getAllClass('modal')) != 0:
			return 'MODAL'

		return 'DO'


	def searchSuject(self,dss):
		searchS = dss.getAllNodesByTag('rel','I')

		for c in searchS:
			if c.gettag_class() == 'proper_noun':
				return c

			if c.gettag_class() == 'common_noun':
				return c

			if c.gettag_class() == 'noun':
				return c

		return None

						

	#TODO using also for positive question
	def getTagQuestion(self,dss,onlytag=False):
		"""
			1 - Identify the type of tag question
			2 - Search the main verb
			3 - Search the subject
			4 - Return the tag question
		"""

		typeTagQuestion = self.identifyTypeTagQuestion(dss)

		
		searchModals = dss.getAllNodesByTag('class','modal')
		searchVerbs = dss.getAllNodesByTag('class','verb')

		subject = self.searchSuject(dss)
		
		if (searchVerbs == [] and searchModals == []) or subject == None:
			print 'back'*40
			return dss 

		firstVerb = searchVerbs[0]

		comma = Symbol(',','APPEND')

		
		N = Factory().instanceClass(subject.gettag_class())
		N.setATTRfrom(subject)
		N.settag_lexeme('<PRONOUN>')
		N.addLeaf(Particle('not','ATTR'))
		N.settag_article('no-art')

		if typeTagQuestion != 'MODAL':
			mainVerb = Verb('nil')
			mainVerb.setATTRfrom(firstVerb)
			

			if typeTagQuestion =='DO':
				mainVerb.settag_lexeme('')

		else:
			mainVerb = Modal('nil')
			mainVerb.setATTRfrom(searchModals[0])
			N.settag_rel('APPEND')

		mainVerb.settag_rel('APPEND')
		mainVerb.settag_question('+')


		
		mainVerb.addLeaf(N)
		firstVerb.addLeaf(comma)
		firstVerb.addLeaf(mainVerb)

		if not onlytag:
			root = Dsyntnode('X')
			
			root.addLeaf(comma)
			root.addLeaf(mainVerb)

			return root

		return firstVerb
	

	def outputKEVIN(self):
		newList = []

		dic = {}
		for indexdss in xrange(len(self.listOfDSS)):
			dss = self.listOfDSS[indexdss]
			if dss.getComplexity() <= 4:
				dss = self.getTagQuestion(dss)

			dic[str(indexdss)] = self.parser_dsynt.treeDSS2xml(dss)


		return dic

	def extractQA(self):
		newList = []
		QeA = QA('crow','fox')
		for indexdss in xrange(len(self.listOfDSS)):

			dss = self.listOfDSS[indexdss] 
			#print dss
			#newList.append(dss.copy())
			if dss.getComplexity() <= 4:
				
				q,a = QeA.generateQeA(dss,'random')
				

				if q != None and a != None:
					newList.append(q)
					newList.append(a)
				else:
					newList.append(dss.copy())

			print QeA.whotalk


				

		return self.parser_dsynt.tree2xml(newList)




		

cp = ContentPlanner("sample_2.xml")
xmlSTRING = cp.extractQA()

#------------Write the output into the specific directory in order to be processed by the realpro
XML_EST_DIR = config_MD.PATH +'data#xml#dev#test_question.xml'.replace('#',os.sep)
writeXML = open(XML_EST_DIR,'w')


for line in xmlSTRING:
  writeXML.write(line)
writeXML.close()