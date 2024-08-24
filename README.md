# Nepali Translator

Neural Machine Translation (NMT) on the Nepali-English language pair. You can try it out [here](https://translation.ilprl.ku.edu.np/nep-eng/default).

The parallel data we prepared can be found [here](https://drive.google.com/open?id=1UThfJKJFvDgTu263DNbz-WPNLqoARZ_0).

`data_cleaning` directory has the scripts that implement the cleaning methods discussed in the report.

`translator` directory has a working interface for the translator. 

## Updates

Towards the end of 2019 some additional work was carried out under the project, described [here](https://lt4all.elra.info/proceedings/lt4all2019/pdf/2019.lt4all-1.94.pdf). The model checkpoints reported in the paper are [here](https://drive.google.com/drive/folders/1zrfYJy62LfVp5RHv81ycyMaCbk6HMLN3). The training data has two parts: a) [real parallel data](https://huggingface.co/datasets/sharad461/ne-en-parallel-208k), b) [synthetic parallel data](https://huggingface.co/datasets/sharad461/ne-en-synthetic-1.6m)

As of Feb 2021, there are a few compatibility issues between the model files and the more recent versions of the packages. To fix these, use the following versions of the packages: `torch-1.3.0` `fairseq-0.9.0` `portalocker-2.0.0` `sacrebleu-1.4.14` `sacremoses-0.0.43` `sentencepiece-0.1.91`.


## Results

**Find the more recent results in the paper linked above.**

The BLEU scores of 7.6 and 4.3 (for supervised methods) that Guzman et al report in their paper are on their `devtest` set. There are actually two more sets they release: the validation set called `dev` set and the recently released (October 2019) `test` set. In the report linked above, we report only the scores on the `dev` set. We reproduce their model using their [implementation](https://github.com/facebookresearch/flores/) to score it. Here we report the scores on both `dev` and `devtest` sets.

#### On `dev` set
|Models   |Corpus size  |NE-EN   |EN-NE   |
|---|---|---|---|
|Guzman et al. (2019)   |564k   |5.24   |2.98   |
|This work   |150k   |12.26   |6.0   |

#### On `devtest` set
|Models   |NE-EN   |EN-NE   |
|---|---|---|
|Guzman et al. (2019)   |7.6   |4.3  |
|This work   |14.51   | 6.58 |

The results on `devtest` are from models that use vocab sizes of 2500.

## Requirements

* `torch-1.3.0`
* `fairseq-0.9.0`
* `sentencepiece-0.1.91`
* `sacremoses-0.0.43`
* `sacrebleu-1.4.14`
* `flask`
* `indic_nlp_library`

Fairseq is used for training, sentencepiece is used to learn BPE over the corpus, sacremoses for treating English text, sacrebleu for scoring the models, flask for the interface. For handling the Nepali text, we use the [Indic NLP Library](https://github.com/anoopkunchukuttan/indic_nlp_library).

All the libraries can be installed using `pip`.

To be able to run the translator interface, Indic NLP Library needs to be cloned to `translator/app/modules/`.

There are other libraries like `python-docx` and `lxml` used by the cleaning scripts.

## Preparing the translator
After training a model using the fairseq implementation of Transformer, copy the checkpoint file to `translator/app/models/` and rename it `en-ne.pt` or `ne-en.pt` based on the translation direction of the checkpoint file. The checkpoint files that realize the results in the report are available [here](https://drive.google.com/open?id=1Ix8lPhheLym_4Hpk3v-8cbf7oJ9YW4Eg). Copy the `.pt` files to `translator/app/models`.

After requirements and models are in place, run `python app/app.py` from `translator` directory.

Details on the training itself can be obtained from fairseq [repo](https://github.com/pytorch/fairseq) or [documentation](https://fairseq.readthedocs.io). The [FLORES github](https://github.com/facebookresearch/flores/) is also useful.

## Sample translations

### NE-EN
| Type | Sentence |
|---|---|
| Source  | ठूला गोदामहरुले, यस क्षेत्रका साना साना धेरै निर्माता हरु द्वारा बनाईएका जुत्ताहरु भण्डार गर्न थाले  । |
| Reference  | Large warehouses began to stock footwear in warehouses , made by many small manufacturers from the area .   |
| System  | Large warehouses began to store shoe made by small producers of this area . |

| Type | Sentence |
|---|---|
| Source  | प्राविधिक लेखकहरूले पनि व्यापारिक, पेशागत वा घरेलु प्रयोगका लागि विभिन्न कार्यविधिहरूका बारे लेख्दछन्। |
| Reference  | Technical writers also write various procedures for business , professional or domestic use . |
| System  | Technical authors also write about various procedures for commercial , professional or domestic use . |

### EN-NE
| Type | Sentence |
|---|---|
| Source  | Obama's language is sophisticated , Putin speaks directly and prefers to use punctuation and statistics , but both have the same ability to win the audience's heart . |
| Reference  | ओबामाको भाषा परिस्कृत छ , पुटिन ठाडो भाषामा तुक्का र तथ्याङ्क प्रयोग गरेर बोल्न रुचाउँछन् , तर दुवैसँग श्रोताको हृदयलाई तरंगित गर्ने समान क्षमता छ । |
| System  | ओबामाको भाषा परिस्कृत छ , पुटिन प्रत्यक्ष रूपमा वाचन र तथ्याङ्क प्रयोग गर्न प्राथमिकता दिन्छ , तर दुवै श्रोताको मुटु जित्न एउटै क्षमता छ । |

| Type | Sentence |
|---|---|
| Source  | Litti Chokha is prepared by stuffing buckwheat flour mixed with various spices in dough and toasting it in fire , and is served with spice paste . |
| Reference  | लिट्टी चोखा - लिट्टी जुन आंटा भित्र सत्तू तथा मसला हालेर आगोमा सेकेर बनाईन्छ , को चोखे सँग पस्किइन्छ । |
| System  | लोती चोखोका विभिन्न मसला मिसाएर बकवाहेट फूल मिसाएर तयार पारिन्छ र यसलाई आगोमा टाँस्न र मसला टाँस्ने सेवा गरिन्छ । |

## Citation
If you use any part of this project in your work, please cite this [paper](https://lt4all.elra.info/proceedings/lt4all2019/pdf/2019.lt4all-1.94.pdf).

For the completion of sixth semester in Computer Science program at Kathmandu University. July 2019.
