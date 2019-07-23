import nltk

eng = _read("bible_dup.en-ne.en")
nep = _read("bible_dup.en-ne.ne")

sent_pairs = [(en, ne) for en, ne in zip(eng, nep)]

new = []
for pair in sent_pairs:
	if len(pair[0].split()) > 80 or len(pair[1].split()) > 80: 
		new_en_sentences = nltk.sent_tokenize(pair[0].strip())
		new_ne_sentences = pair[1].split("। ")

		if len(new_en_sentences) > len(new_ne_sentences):
			new_ne_sentences += ["\n"]*(len(new_en_sentences) - 1)
		else:
			new_en_sentences += ["\n"]*(len(new_ne_sentences) - 1)
		new.append((new_en_sentences, new_ne_sentences))
	else:
		new.append(([pair[0]], [pair[1]]))

new_eng, new_nep = [], []
for (en, ne) in new:
	new_eng += en
	new_nep += ne

with open("bible.en", "w", encoding="utf-8") as f:
	for line in new_eng:
		f.write(line + "\n")

with open("bible.ne", "w", encoding="utf-8") as f:
	for line in new_nep:
		f.write(line + "\n")