import os
import config_MD
file_d = open(config_MD.PATH+"data#realpro#dev#test_question.txt".replace('#',os.sep)).read()


sentences = file_d.split('.')

# 0  Did I sit on the tree's branch ?
# 1  Was the cheese in the I beak ?
# 2  Did I observe you ?
# 3  Did I try to discover for the fox to get the cheese ?
# 4  Did I come ?
# 5  Did I stand under the tree ?
# 6  Did I look toward you ?
# 7  Did I say the fox saw you ?
# 8  Did you say the I beauty was incomparable ?
# 9  Did I feel for you to flatter the crow ?
# 10  Did the cheese fall ?
# 11  Did I snatch the cheese ?
# 12  Did you say sing TO I was able ?
# 13  Did you say I needed the wits ?
# 14    ?
# [Finished in 0.0s]

def replaceN(sentence):
	sentence = sentence.replace("  "," ")
	sentence = sentence.replace("s not","sn't")
	sentence = sentence.replace("es not","sn't")
	sentence = sentence.replace("o not","on't")
	sentence = sentence.replace("n not","n't")
	sentence = sentence.replace("did not","didn't")
	sentence = sentence.replace("  "," ")

	return sentence

count = 0
for indexSentence in xrange(len(sentences)):
	sentence = sentences[indexSentence]
	sentence = replaceN(sentence)
	
	# if indexSentence % 2 == 0:
	# 	print 'ORIGINAL :',
	# else:
	# 	print 'MODIFIED :',
	count += 1
	for sp in sentence.split('.'):
		
		sp = sp.replace(" ,",",")

		# punct = "?"
		# if ',' in sp:
		# 	punct = '?'
		print sp#,punct
		
	

	