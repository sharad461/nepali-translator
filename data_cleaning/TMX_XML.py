from lxml import etree
from functions import summarize, write_lines

# Treats .TMX files from NNC Corpus

tmx_file = "NP8"

tree = etree.parse(tmx_file + ".tmx")
paragraphs = tree.findall(".//seg")

lines = []

en,ne = [],[]
counter = 1

for paragraph in paragraphs:
	line = ''.join(etree.tostring(paragraph, method="text", 
		encoding="unicode").split("\n")).strip()

	lines.append(line)

	if counter % 2 == 1:
		en.append(line)
	else:
		ne.append(line)

	counter += 1

summarize(lines)
summarize(en)
summarize(ne)

write_lines(en, tmx_file + ".en")
write_lines(ne, tmx_file + ".ne")

