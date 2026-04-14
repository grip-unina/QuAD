# ReWIND Dataset

<p align="center"> <img src="../docs/rewind.svg" alt="ReWIND" width="55%" /> </p>

***ReWIND*** is a collection of in-the-wild real and AI-generated images that were shared on-line and became viral on social networks. The widespread circulation of these images allowed us to scrape the web to find multiple instances (*near-duplicates*) of each source image with different and unknown degradations.
The dataset contains 162 sources (87 real / 75 fake) with at least 10 near-duplicates, for a total of 9646 instances in different formats (JPEG, WebP and PNG).

A complete list of sources with the exact amount of images is summarized in the following Table:

| Source | # Real/Fake sources | # Real/Fake near-duplicates |
| ---: | :---: | :---: |
| B-Free [[1]](https://arxiv.org/abs/2412.17671) | 20 / 15 | 1261 / 1851 |
| FOSID [[2]](https://arxiv.org/abs/2408.11541) |- / 3 | - / 517 |
| AMMeBa [[3]](https://arxiv.org/abs/2405.11697) |44 / 39 | 1929 / 2135 |
| Fact-Check Tool [[4]](https://toolbox.google.com/factcheck/explorer/)| - / 18 | - / 776 |
| RRDataset [[5]](https://arxiv.org/abs/2509.09172) | 23 / - | 1177 / - |
| **Total** | **87 / 75** | **4367 / 5279** |

[[1]](https://arxiv.org/abs/2412.17671) *Fabrizio Guillaro et al., A Bias-Free Training Paradigm for More General AI-generated Image Detection. (CVPR Workshops 2026)* \
[[2]](https://arxiv.org/abs/2408.11541) *Dimitrios Karageorgiou et al., Evolution of Detection Performance throughout the Online Lifespan of Synthetic Images. (ECCV 2024)* \
[[3]](https://arxiv.org/abs/2405.11697) *Nicholas Dufour et al., AMMeBa: A Large-Scale Survey and Dataset of Media-Based Misinformation In-The-Wild. (ArXiv 2024)* \
[[4]](https://toolbox.google.com/factcheck/explorer/) *Google Fact-Check tool*\
[[5]](https://arxiv.org/abs/2509.09172) *Chunxiao Li et al., Bridging the Gap Between Ideal and Real-world Evaluation: Benchmarking AI-Generated Image Detection in Challenging Scenarios. (ICCV 2025)*

Further details can be found in Section 3 of the paper.

## CSV Files Description

The `ReWIND_*.csv` CSVs in the repository contain information about ReWIND images, including the Image Quality Assessment (IQA) scores and the GenAI detection scores (*logits*) for each image (values > 0 indicate fake images, values < 0 indicate real images).
Specifically:
- **ReWIND.csv** provides information with the *uncalibrated* detection scores.
- **ReWIND_*calibrated_AT*.csv** provides information with detection scores *calibrated with QuAD* (fitting with 50% of AncesTree images).
- **ReWIND_*calibrated_LOO*.csv** provides information with detection scores *calibrated with QuAD* (fitting with ReWIND images using **leave-one-out strategy**).

The CSVs also include the following metadata for each image:
| Column | Description |
| :--- | :--- |
| `filename` | Path to the image. |
| `src_dataset` | Dataset of the source image. |
| `src` | ID of the source image. |
| `label` | Whether the image is real or AI-generated. |
| `format` | File format of the current image. |
| `date` | Publication date of the image. |
| `w`, `h` | Width and height of the image. |
| `size` | Total number of pixels (width × height). |
| `estimated_QF` | An estimation of the last Quality Factor (QF) applied on the image (`200` means not compressed). |
| `md5` | MD5 checksums for integrity verification. |

**Note**: unfortunately, date information is not available for all images.\
**Note**: some near-duplicates from certain sources belong to different datasets but share the same source ID for grouping purposes (e.g., Gaza2 appears in both AMMeBa and FOSID).

## Download ReWIND

[![ReWIND](https://img.shields.io/badge/-ReWIND-ffab03.svg?style=for-the-badge&logo=files&logoColor=ffffff)](https://www.grip.unina.it/download/prog/QuAD/ReWIND.zip)

Download ReWIND (md5sum `14d7f7de383421ee017de052ce2095b4`) at the link above and unzip the files.
The archive (~1.4 GB) contains all the images **except for AMMeBa**, which we cannot redistribute as the dataset does not provide the images directly. 
For AMMeBa, the images can be downloaded using the links in `ammeba_urls.csv`, which also includes MD5 checksums for integrity verification.

## Directory structure

After downloading, you should have a structure like this:
```
data_ReWIND
├── ReWIND
│   ├── ammeba
│   ├── FOSID
│   ├── google_factcheck
│   ├── RRDataset
│   └── viral_bfree
├── ReWIND.csv
├── ReWIND_calibrated_AT.csv
├── ReWIND_calibrated_LOO.csv
└── ...
```

## Bibtex

If you use this dataset, please cite:

```
@inproceedings{Guillaro2026quality,
  title={Quality-Aware Calibration for AI-Generated Image Detection in the Wild},
  author={Guillaro, Fabrizio and De Rosa, Vincenzo and Cozzolino, Davide and Verdoliva, Luisa},
  booktitle={IEEE/CVF conference on Computer Vision and Pattern Recognition (CVPR) Workshops},
  year={2026}
}
```


## License

Copyright (c) 2026 Image Processing Research Group of University Federico II of Naples ('GRIP-UNINA'). 

All rights reserved.

This software should be used, reproduced and modified only for informational and nonprofit purposes.

By downloading and/or using any of these files, you implicitly agree to all the
terms of the license, as specified in the document LICENSE.txt
(included in this package)