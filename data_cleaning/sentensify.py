from nltk import sent_tokenize
from functions import _read, write_lines
# English 
lines = _read("global.en")

new = []

for line in lines:
	new += sent_tokenize(line)

write_lines(new, "global.en")

# Nepali
lines = _read("global.ne")

import re

new = []

for line in lines:
	new += re.split("।\s", line)

write_lines(new,"global.ne")