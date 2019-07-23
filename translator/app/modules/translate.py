import sentencepiece
from sacremoses import MosesDetokenizer, MosesTokenizer
import sys, os

sys.path.extend(["app/modules/indic_nlp_library/src",]) # coming all the way from app.py
from indicnlp.tokenize import indic_tokenize, indic_detokenize
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory

factory = IndicNormalizerFactory()
normalizer = factory.get_normalizer(
    "ne", remove_nuktas=False,
)

def bpencode(sentence, srctolang):
	sp = sentencepiece.SentencePieceProcessor()
	
	if srctolang == "ne_en": sp.Load("app/ne_en_bpe20000/sentencepiece.bpe.model")
	elif srctolang == "en_ne": sp.Load("app/en_ne_bpe5000/sentencepiece.bpe.model")

	return " ".join(sp.EncodeAsPieces(sentence))

def detok(sentence, lang):
	if lang == "en": return MosesDetokenizer(lang="en").detokenize(sentence.split())
	elif lang == "ne":
		return indic_detokenize.trivial_detokenize(sentence, "ne")

def tok(sentence, lang):
	if lang == "en": return " ".join(MosesTokenizer(lang="en").tokenize(sentence))
	elif lang == "ne": 
		line = normalizer.normalize(sentence)
		return " ".join(indic_tokenize.trivial_tokenize(line, "ne"))

if __name__ == '__main__':
	a = tok("यस बेला श्रीषा साँच्चै नै खुशी, देखिन्छिन्। ", lang="ne")
	print(a)
	print(detok(a, lang="ne"))