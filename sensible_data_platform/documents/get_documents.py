import os

def getText(name, lang):
	path = os.path.dirname(os.path.abspath(__file__))
	text = open(path+'/'+name+'_'+lang+'.txt').read()
	return text
