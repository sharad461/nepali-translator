from functions import _read, write_lines, xml_to_text, summarize, length_filter
import os

directory = "mono/"

lines = []

for file in os.listdir(directory):
	lines += xml_to_text(directory + os.path.splitext(file)[0])


lines = length_filter(lines, 25)

print("Total: ")
summarize(lines)

write_lines(lines, "e-h.ne")