from functions import _read, write_lines, remove_blank_lines

file = "mono"

lines = _read(file + ".en")

write_lines(remove_blank_lines(lines), file + ".en")