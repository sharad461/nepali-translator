# Reads a file and breaks it down at line breaks to 
# return a list of sentences
_read = lambda x: open(x, "r", encoding="utf-8").read().split("\n")

def write_lines(lines, filename):
	'''
	Writes a list of sentences to a file
	'''
	with open(filename, "w", encoding="utf-8") as f:
		for line in lines:
			f.write(line + "\n")

def summarize(lines):
	print("Words: ", len(''.join(lines).split()))
	print("Lines: ", len(lines))

def xml_to_text(xml_file, tag=".//s"):
	'''
	Extracts text contained in NNC (Nepali 
	National Corpus) XML files and returns a 
	list of sentences/paragraphs

	Requires lxml
	
	Input: XML filename without extension
	Output: list of sentences/paragraphs

	'''
	from lxml import etree

	regxNS = "http://exslt.org/regular-expressions"

	tree = etree.parse(xml_file + ".xml")
	paragraphs = tree.findall(".//s")

	lines = []

	for paragraph in paragraphs:
		line = ''.join(etree.tostring(paragraph, method="text", 
			encoding="unicode").split("\n")).strip()

		# stack of postpositions and cardinal numbers (types I- and M- as 
		# described in Nelralec Tagset, Hardie et al)
		connectives = [] 

		for word in paragraph.xpath('.//w[re:test(@ctag, "^[IM][^M]")]', 
			namespaces={'re': regxNS}): connectives.append(word.text)

		for c in connectives: line = line.replace(' ' + c + ' ', c + ' ', 1)

		lines.append(line)
	
	summarize(lines)
	return lines

def text_to_docx(lines, filename):
	'''
	Converts a corpus file into a Document format (.docx)

	Requires docx library
	Also requires a font that can write Nepali Unicode,
	change doc.styles['Normal'].font.name to your prefered
	font that supports Nepali Unicode characters

	Input: list of sentences
	Output: filename.docx
	'''
	from docx import Document

	doc = Document()

	doc.styles['Normal'].font.name = "Nirmala UI"

	for line in lines:
		doc.add_paragraph(line)

	doc.save(filename + ".docx")
	summarize(lines)

def length_filter(lines, num):
	'''
	Returns a list of strings that have lesser words than `num`

	Input: list of sentences
	Output: list of sentences
	'''
	return [line for line in lines if len(line.split()) < num]

def check_repetition(lines):
	res = set(line for line in lines)
	print("{} vs {}".format(len(lines), len(res)))
	return list(res)

def check_repetition_pair(lines1, lines2):
	'''
	Checks for repeating sentence pairs and eliminates them
	
	Input: two lists, one for each language in a pair
	Output: two lists, without repeating sentence pairs

	'''
	sents = set(zip(lines1, lines2))

	print("{} vs {}".format(len(lines1), len(sents)))
	
	g1, g2 = [], []

	for (en, ne) in list(sents):
		g1.append(en)
		g2.append(ne)

	return g1, g2

def sent_tokenize_nepali(filename):
	'''
	Tokenizes Nepali text

	Input: filename with extension
	Output: list of tokenized sentences
	'''
	import re

	string = ' '.join(_read(filename))

	lines = re.split("\।|\?|\|", string)

	summarize(lines)

	return lines

def length_similarity(sent1, sent2):
	'''
	Checks the similarity between two sentences based on
	their lengths

	Refer to the report

	Input: two sentences
	Output: length similarity
	'''
	try:
		_a, _b = len(sent1.split()), len(sent2.split())
		s = (_b/_a) if _a > _b else (_a/_b)

		return s + ((1-s)/(1+abs(_a-_b)))
	except ZeroDivisionError:
		pass

def partition(lines, num):
	'''
	Partitions a list of sentences into a list of lists
	each with `num` elements only
	'''
	post = [] # list post partition

	a, b = 0, 0
	length = len(lines)

	while b != length-1:
		if b + num < length: b += num
		else: b = length-1
		post.append(lines[a:b])
		a += num

	return post

def remove_blank_lines(lines):
	import re

	s = []

	for line in lines:
		if line.strip():
			s.append(line)

	return s

def collect(dir_path, dest_name):
	'''
	Build parallel sets from resource files
	'''
	import os

	nepali, english = [], []

	for file in os.listdir(dir_path):
		f = os.path.splitext(file)

		if f[1] == ".ne": nepali.append(f[0])
		elif f[1] == ".en": english.append(f[0])
		else: pass

	assert len(english) == len(nepali), "Unequal number of files in the directory"

	eng, nep = [], []

	for file in english: eng += _read(dir_path + file + ".en")[:-1]
	for file in nepali: nep += _read(dir_path + file + ".ne")[:-1]

	write_lines(eng, dest_name + ".en")
	write_lines(nep, dest_name + ".ne")