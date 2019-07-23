from functions import _read, write_lines
import re

a, b = _read("1.en"), _read("1.ne")

# For English

# Joins an incomplete line to the line above
i = 1
while i < len(a):
	if re.match("^([a-z0-9])+[^0-9i\.\)]", a[i]):
		a[i-1] = a[i-1].strip() + ' ' + a[i].strip()
		del(a[i])
	else:
		i += 1

# Joins a numeral line to the next line
i = 0
while i < len(a)-1:
	if len(a[i]) < 3 and re.match("^([a-z0-9]){1,2}[\.\)]\s*", a[i]):
		a[i] = a[i].strip() + ' ' + a[i+1].strip()
		del(a[i+1])
	i += 1

write_lines(a, "1_bpf.en")

# For Nepali

# Removes lines with only purnabiraams
i = 0
while i < len(b):
	if re.match("^\।", b[i]):
		del(b[i])
	i += 1

# Joins a numeral line to the next line
i = 0
while i < len(b)-1:
	if len(b[i]) < 3 and re.match("^([a-z0-9]){1,2}[\.\)]\s*", b[i]):
		b[i] = b[i].strip() + ' ' + b[i+1].strip()
		del(b[i+1])
	i += 1

write_lines(b, "1_bpf.ne")