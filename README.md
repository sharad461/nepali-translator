# Nepali Translator

Neural Machine Translation (NMT) on the Nepali-English language pair. 

Contributions of this project: adding to and cleaning the parallel data that is publicly available and improving the baseline achieved by [Guzman et al (2019)](https://www.aclweb.org/anthology/D19-1632/). They collected the data for the [parallel corpus filtering task for WMT19](http://www.statmt.org/wmt19/parallel-corpus-filtering.html). On the September 2019 update to their paper, they add scores they obtained using multilingual MT methods (leveraging Hindi parallel and monolingual data), but their scores for fully-supervised Nepali-English MT still stand at (BLEU) 7.6 (NE-EN) and 4.3 (EN-NE) - both of which our models surpass in this project.

The report is available [here](https://drive.google.com/open?id=16F4e1Wr3ElosFnoVfZrEId4N0be2JPG4).

The clean parallel data can be downloaded from [here](https://drive.google.com/open?id=1UThfJKJFvDgTu263DNbz-WPNLqoARZ_0).

`data_cleaning` directory has the scripts that implement the cleaning methods discussed in the report.

`translator` directory has a working interface for the translator. 

## Results

The BLEU scores of 7.6 and 4.3 (for supervised methods) that Guzman et al report in their paper are on their `devtest` set. There are actually two more sets they release: the validation set called `dev` set and the recently released (October 2019) `test` set. In the report linked above, we report only the scores on the `dev` set. We reproduce the their model using their [implementation](https://github.com/facebookresearch/flores/) to score it. 

Here we report the scores on both `dev` and `devtest` sets.

### On `dev` set
|Models   |Corpus size  |NE-EN   |EN-NE   |
|---|---|---|---|
|Guzman et al. (2019)   |564k   |5.24   |2.98   |
|This work   |150k   |12.26   |6.0   |

### On `devtest` set

## Requirements

* `fairseq`
* `sentencepiece`
* `sacremoses`
* `sacrebleu`
* `flask`
* `indic_nlp_library`

Fairseq does the heavy-lifting for training the models, sentencepiece is used to learn BPE over the data, sacremoses for treating English text, sacrebleu for scoring the models, flask for the interface. For handling the Nepali text, we use the [Indic NLP Library](https://github.com/anoopkunchukuttan/indic_nlp_library).

Install all the libraries using `pip install`. Indic NLP Library, you need to clone to `translator/app/modules/`.

There are other libraries like `python-docx` and `lxml` used by the cleaning scripts.

## Training models
After training a model using the fairseq implementation of Transformer, copy the checkpoint file to `translator/app/models/` and rename it `en-ne.pt` or `ne-en.pt` based on the translation direction of the checkpoint file. The checkpoint files that realize the results in the report are available [here](https://drive.google.com/open?id=1Ix8lPhheLym_4Hpk3v-8cbf7oJ9YW4Eg). Copy the `.pt` files to `translator/app/models`.

After requirements and models are in place, run `python app/app.py` from `translator` directory.

Details on the training itself can be obtained from fairseq [repo](https://github.com/pytorch/fairseq) or [documentation](https://fairseq.readthedocs.io).

## Sample translations

### NE-EN
| Source  | ठूला गोदामहरुले, यस क्षेत्रका साना साना धेरै निर्माता हरु द्वारा बनाईएका जुत्ताहरु भण्डार गर्न थाले  । |
| Reference  | Large warehouses began to stock footwear in warehouses , made by many small manufacturers from the area .   |
| System  | Large warehouses began to store shoe made by small producers of this area . |

| Source  | प्राविधिक लेखकहरूले पनि व्यापारिक, पेशागत वा घरेलु प्रयोगका लागि विभिन्न कार्यविधिहरूका बारे लेख्दछन्। |
| Reference  | Technical writers also write various procedures for business , professional or domestic use . |
| System  | Technical authors also write about various procedures for commercial , professional or domestic use . |

### EN-NE

## Citation
If you use any part of this project in your work, please cite:

```bibtex
@inproceedings{,
  title={Nepali Translator},
  author={Duwal, Sharad and Manandhar, Amir and Maskey, Saurav and Hada, Subash},
  year={2019}
}
```

For the completion of sixth semester in Computer Science program at Kathmandu University. July 2019.
