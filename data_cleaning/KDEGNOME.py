from functions import _read, write_lines, length_similarity

eng, nep = _read("gnome_improved.en"), _read("gnome_improved.ne")

# from langdetect import DetectorFactory, detect

# DetectorFactory.seed = 0

# pairs = set(zip(eng, nep))

# sents = set()

# for (en, ne) in pairs:
# 	try:
# 		if len(ne.split()) > 3 and detect(ne) in ('hi', 'ne'):
# 			sents.add((en, ne))
# 	except Exception:
# 		pass

scores = []

sents = []

for (en, ne) in zip(eng, nep):
	score = length_similarity(en, ne)
	try:
		if score > 0.53:
			sents.append((en, ne))
	except TypeError:
		pass

print(len(scores))

g1, g2 = [], []

for (en, ne) in sents:
	g1.append(en)
	g2.append(ne)

write_lines(g1, "gnome_final.en")
write_lines(g2, "gnome_final.ne")