# Nepali Translator

Neural Machine Translation (NMT) on the Nepali-English language pair. 

Contributions of this project: adding to and cleaning the parallel data that is publicly available and improving the baseline for supervised methods achieved by [Guzman et al (2019)](https://www.aclweb.org/anthology/D19-1632/). They collected the data for the [parallel corpus filtering task for WMT19](http://www.statmt.org/wmt19/parallel-corpus-filtering.html). On the September 2019 update to their paper, they add scores they obtained using multilingual MT methods (leveraging Hindi parallel and monolingual data), but their scores for fully-supervised Nepali-English MT still stand at BLEUs 7.6 (NE-EN) and 4.3 (EN-NE) - both of which our models surpass in this project.

The report is available [here](https://drive.google.com/open?id=16F4e1Wr3ElosFnoVfZrEId4N0be2JPG4).

The clean parallel data can be downloaded from [here](https://drive.google.com/open?id=1UThfJKJFvDgTu263DNbz-WPNLqoARZ_0).

`data_cleaning` directory has the scripts that implement the cleaning methods discussed in the report.

`translator` directory has a working interface for the translator. 

## Results

The BLEU scores of 7.6 and 4.3 that Guzman et al report in their paper are on their `devtest` set. There are two more sets: the validation set called `dev` set and the recently (October 2019) released `test` set. In the report linked above, we report only the scores on the `dev` set. We reproduce the their model using their [implementation](https://github.com/facebookresearch/flores/) to score it on the `dev` set. Here we report the scores on both the sets.

#### On `dev` set
|Models   |Corpus size  |NE-EN   |EN-NE   |
|---|---|---|---|
|Guzman et al. (2019)   |564k   |5.24   |2.98   |
|This work   |150k   |12.26   |6.0   |

#### On `devtest` set

## Requirements
* `fairseq`
* `sentencepiece`
* `sacremoses`
* `[indic_nlp_library]`(https://github.com/anoopkunchukuttan/indic_nlp_library) [copy all files to `translator/app/modules/indic_nlp_library/`]
* `flask`

## Training models
After training a model using the fairseq implementation of Transformer, copy the checkpoint file to `translator/app/models/` and rename it `en-ne.pt` or `ne-en.pt` based on the translation direction of the checkpoint file. The checkpoint files that realize the results in the report are available [here](https://drive.google.com/open?id=1Ix8lPhheLym_4Hpk3v-8cbf7oJ9YW4Eg). Copy the `.pt` files to `translator/app/models`.

After requirements and models are in place, run `python app/app.py` from `translator` directory.

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
