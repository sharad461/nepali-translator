from functions import _read, write_lines, xml_to_text,\
 text_to_docx, check_repetition_pair

filename = "mono"

# write_lines(xml_to_text(filename), filename + ".ne")

write_lines(xml_to_text("mono"), "mono.txt")

# lines = check_repetition(_read("a.ne"))
