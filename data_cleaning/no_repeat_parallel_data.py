from functions import _read, check_repetition_pair, check_repetition, \
write_lines

# BELOW IS THE CODE TO REMOVE REPETITIONS IN TWO PARALLEL SETS

# _a_en, _a_ne, _b_en, _b_ne = _read("a.en"), _read("a.ne"), \
# _read("b.en"), _read("b.ne")

# A = list(zip(_a_en, _a_ne))
# B = list(zip(_b_en, _b_ne))

# sents = list(set(A + B))

# g1, g2 = [], []

# for (en, ne) in sents:
# 	g1.append(en)
# 	g2.append(ne)

# write_lines(g1, "PR_improved.en")
# write_lines(g2, "PR_improved.ne")



# REMOVING REPETITIONS IN A SET

A, B = _read("globalvoices_improved.en"), _read("globalvoices_improved.ne")
lines = set(zip(A,B))

_A = []
final = set()
repetitions = []

count = 0

for (en, ne) in lines:
	if en not in _A:
		_A.append(en)
		final.add((en, ne))
	else:
		repetitions.append(en)
	count += 1

g1, g2 = [], []
# print(len(repetitions))
for (en, ne) in final:
	g1.append(en)
	g2.append(ne)

g1, g2 = check_repetition_pair(A,B)

write_lines(g1, "global.en")
write_lines(g2, "global.ne")