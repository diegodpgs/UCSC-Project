import random
import os
import config_MD
from dsyntnode import *
from parser import *
from bfs import *

class QA:

	def __init__(self,char1,char2):
		self.parser_dsynt = Parser()
		self.wh_questions = ['who','what','where']#,'why','how']
		self.character1 = char1
		self.character2 = char2
		self.whotalk = self.character1

	def getSubject(self,dss):
		searchS = dss.getAllNodesByTag('rel','I')

		if len(searchS) == 0:
			return None

		if searchS[0].gettag_class() not in ['common_noun','proper_noun']:
			return None

		if searchS[0].gettag_gender() == 'neut':
			return None

		return searchS[0]

	def applyPossessivePronoun(self,dss):
		allProper = dss.getAllNodesByTag('class','proper_noun')
		allCommon = dss.getAllNodesByTag('class','common_noun')
		allnouns = []
		allnouns.extend(allProper)
		allnouns.extend(allCommon)
		
		for nouns in allnouns:
			if nouns.getParent().gettag_class() == 'common_noun' and nouns.gettag_gender() != 'neut':
				nouns.settag_lexeme('<POSSESSIVE_PRONOUN>')


	def createPersonages(self,dss):
		crows = dss.getAllNodesByTag('lexeme',self.character1)
		fox = dss.getAllNodesByTag('lexeme',self.character2)
		character = dss.getAllNodesByTag('rel','I')
		

		r = random.randint(0,100)

		for c in crows:
			char1 = Proper_Noun('')
			char1.setATTRfrom(c)
			char1.settag_lexeme('<PRONOUN>')
			char1.settag_article('no-art')

			if r % 2 == 0:
				char1.settag_person('2nd')
				
			else:
				char1.settag_person('1st')
				self.whotalk = self.character1
				

			c.replaceNode(self.character1,char1)


		for f in fox:
			char2 = Proper_Noun('')
			char2.setATTRfrom(f)
			char2.settag_lexeme('<PRONOUN>')
			char2.settag_article('no-art')

			if r % 2 == 0:
				char2.settag_person('1st')
				self.whotalk = self.character2
			else:
				char2.settag_person('2nd')
				

			f.replaceNode(self.character2,char2)

		

	def createSimpleAnswer(self,dss,acknowledge='random'):
		acks = ['yeah','of course','absolutely','yes','humrum','aham','yes yes']


		mainVerb = dss.getAllNodesByTag('class','verb')
		subject = dss.getAllNodesByTag('class','proper_noun')
		

		
		if mainVerb != [] and subject != []:

			v = Verb('')
			v.setATTRfrom(mainVerb[0])

			if v.gettag_question() == '+':
				v.settag_question('')


			if acknowledge == 'random':
				acknowledge = acks[random.randint(0,len(acks)-1)]

			adj_ack = Adjective(acknowledge)
			adj_ack.settag_rel('ATTR')
			adj_ack.settag_starting_point('+')
			comma = Symbol(',')
			comma.settag_rel('APPEND')

			
			adj_ack.addLeaf(comma)
			v.addLeaf(adj_ack)

			s = Proper_Noun('')
			s.setATTRfrom(subject[0])

			if s.gettag_person() =='2nd':
				s.settag_person('1st')
			else:
				s.settag_person('2nd')

			v.addLeaf(s)

			return v

		return None
			
	#fox,fox       Did I try to discover for me to get the cheese ?
	#crow,crow,fox Did I feel for me to flatter you ?

	def applySimpleQuestion(self,dss):
		allVerbs = dss.getAllNodesByTag('class','verb')
		subject = self.getSubject(dss)

		if subject == None:
				return False

		if allVerbs == []:
			return False

		firstVerb = allVerbs[0]

		if firstVerb.gettag_rel() == 'II':
			firstVerb.settag_question('+')

			# self.createPersonages(dss)

		return True

	def applyWhQuestion(self,dss,wh_question='who'):
		wh_pronoun = ['who','what']
		wh_preposition = ['when','where','why','how']

		allverbs = dss.getAllNodesByTag('class','verb')
		subject = self.getSubject(dss)

		if allverbs != [] and subject != None:

			mainVerb = allverbs[0]

			if wh_question in wh_pronoun:


				if mainVerb.gettag_rel() != 'II':
					return False
				subject.settag_pro('wh')
				# self.createPersonages(dss)
				mainVerb.settag_question('+')

			elif wh_question in wh_preposition:
				allprepositions = dss.getAllNodesByTag('class','preposition')

				if allprepositions == []:
					return False

				preposition = allprepositions[0]
				preposition.removeLeafs()
				preposition.settag_lexeme(wh_question)
				preposition.settag_rel('ATTR')

		else:
			return False


		return True

	def createWhAnswer(self,dss,wh_question='who'):
		wh_pronoun = ['who','what']
		wh_preposition = ['when','where']#,'why','how']

		if wh_question in wh_pronoun:
			subject = self.getSubject(dss)
			if subject == None:
				return None
			s = Factory().instanceClass(subject.gettag_class())
			s.setATTRfrom(subject)
			s.settag_pro('')
			s.settag_rel('II')

			verb = Verb('be')
			verb.settag_rel('II')
			verb.settag_tense('past')
			verb.addLeaf(s)
			return verb
		elif wh_question in wh_preposition:
			allprepositions = dss.getAllNodesByTag('class','preposition')
			if allprepositions != []:
				print allprepositions[0],'x'*40
				return allprepositions[0]



		return None

	#dss could be a tree_structure object or a xml string
	def generateQeA(self,dss,type_of_question='simple',acknowledge='random'):
		"""
			simple
					input  : " I ate an apple.
					output : "did i eat an apple?"
			wh-
					input  : " I ate an apple.
					output : "what i eat?"

			random: choose reandomicaly a type of question
		"""

		if type(dss) == str:
			dss = self.parser_dsynt.string2DSStree(dss)

		
		self.createPersonages(dss)
		
		answer = None

		if type_of_question == 'random':

			if random.randint(0,100) % 2 == 0:
				type_of_question = 'simple'
			else:
				type_of_question = 'wh'

		if type_of_question == 'simple':

				if not self.applySimpleQuestion(dss):
					return None,None

				answer   = self.createSimpleAnswer(dss,acknowledge)

		elif type_of_question == 'wh':
			wh = self.wh_questions[random.randint(0,len(self.wh_questions)-1)]
			answerDss = dss.copy()
			self.applyWhQuestion(dss,wh)
			answer = self.createWhAnswer(answerDss,wh)

		self.applyPossessivePronoun(dss)
		return dss,answer



	