Improving the Detection of Multilingual Online Attacks with Rich Social Media Data from Singapore
---
**This repository contains a new multilingual dataset of online attacks introduced in an anonymous ACL 2023 submission.**

Using the multilingual city-state of Singapore as a starting point, we collected a large corpus of Reddit comments in Indonesian, Malay, Singlish and other dialects, and provide fine-grained hierarchical labels for online attacks. For more information on the data collection and annotation processes, a full analysis of the annotated data as well as a presentation of baseline and experimental classification models please see the paper. 

We publish the corpus with rich metadata (to be found in `0_resources/0_dataset/`),  an automatic English translation (`0_resources/1_dataset_translated/`) as well as additional unlabelled data for domain adaptation (`0_resources/3_unlabelled_data/`).

An analysis of the dataset can be found in Jupyter notebook `1_dataset_analysis.ipynb`, and baseline as well as experimental model results in `2_model_evaluation.ipynb` and `3_error_analysis.ipynb`. 

To execute the scripts, create a new virtual environment and install the required packages listed in `requirements.txt`.