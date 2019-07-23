import re
from functions import _read, write_lines

# Split N N C Nepali
lines = _read("3.ne")

new = []

for line in lines:
	new += re.split("\।\s|\?\s|\/|\|", line.strip())

write_lines(new, "3_sentensify.ne")

# Split N N C English
lines = _read("3.en")

for line in lines:
	new += re.split("\.\s|\?\s|\/|\|", line.strip())

write_lines(new, "3_sentensify.en")