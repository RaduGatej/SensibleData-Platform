import os

def getText(name):
	path = os.path.dirname(os.path.abspath(__file__))
	text = open(path+'/'+name+'.txt').read()
	return text
