# AncesTree Dataset

<p align="center"> <img src="../docs/AncesTree.svg" alt="AncesTree" width="85%" /> </p>

***AncesTree*** is a tree of progressive degradations used to generate near-duplicate image instances. Starting from a clean image (from the source dataset of real/fake images), multiple degradation operations are applied across levels (L = 1 to L = 5). Each branch represents a sequential processing pipeline consisting of random cropping, resizing, and compression for a total of 124 near-duplicate samples for each image.
The total number of near-duplicates is 136,400.

Further details can be found in Section 3 of the paper.

## CSV Files Description

The `AncesTree_*.csv` CSVs in the repository contain information about AncesTree images, including the Image Quality Assessment (IQA) scores and the GenAI detection scores (*logits*) for each image (values > 0 indicate fake images, values < 0 indicate real images).
Specifically:
- **AncesTree_dev.csv** provides information about the development set with the *uncalibrated* detection scores.
- **AncesTree_test.csv** provides information about the test set with the *uncalibrated* detection scores.
- **AncesTree_test_*calibrated*.csv** provides information about the test set, with detection scores *calibrated with QuAD*.

The CSVs also include the following metadata for each image:
| Column | Description |
| :--- | :--- |
| `filename` | Path to the current degraded image. |
| `parent` | Path to the parent image from which the current image was directly derived. |
| `src` | Path to the original source image (the root of the tree). |
| `level` | Depth level in the tree (`1`: closest to the root, `5`: most degraded). |
| `op_node` | The specific pipeline of operations applied to the *parent* to obtain the current image. |
| `op_tot` | The cumulative list of all operations applied since the *source* image. |
| `num_ops` | Total count of operations applied since the source image. |
| `type` | The origin or generator of the source image. |
| `label` | Whether the image is real or AI-generated. |
| `split` | Whether the image belongs to the development set or test set. |
| `format` | File format of the current image. |
| `w`, `h` | Width and height of the image. |
| `size` | Total number of pixels (width × height). |
| `last_QF` | The Quality Factor (QF) of the *last* known compression operation applied to the image (`200` if the image has never been compressed). |
| `current_QF` | The compression QF applied by the current pipeline (`200` if no compression is applied on the current node). |

**Note**: to compensate for the higher perceived quality of WEBP images, due to the better compression efficiency of WEBP codec compared to JPEG, we add an offset of `+4` in the columns `last_QF` and `current_QF` for images compressed using WEBP.

Every image is accompanied by an `.npz` file with the same name containing more details, such as the specific parameters of each operation applied on the image.

## Download AncesTree

[![AncesTree](https://img.shields.io/badge/-AncesTree-ffab03.svg?style=for-the-badge&logo=files&logoColor=ffffff)](https://www.grip.unina.it/download/prog/QuAD/AncesTree/)

Download AncesTree at the link above and unzip the files in an `AncesTree` subfolder.
The archives are:
- **real_raise.zip** (~5 GB): it contains the tree for the real RAISE images.
- **stable_diffusion_models.zip** (~21 GB): it contains the tree for SD1.4, SD2, SD-XL, SD3 images.
- **commercial_models.zip** (~18 GB): it contains the tree for DALL-E 2, DALL-E 3, Midjourney v5, Firefly images.
- **other_models.zip** (~7 GB): it contains the tree for Latent Diffusion and FLUX images.

You can verify the integrity of the downloads using the [checksums](https://www.grip.unina.it/download/prog/QuAD/checksum.txt).


## Download source images (optional)

Real images come from the RAISE dataset. For each real image, 10 synthetic images are generated using the caption of its real counterpart by SD1.4, SD2, SD-XL, Midjourney v5, DALL-E 2, DALL-E 3, Firefly, Flux, SD3, and Latent Diffusion. With this approach, real and fake images are aligned in terms of semantic content to mitigate possible biases. 
We consider a total of 100 real images and 1,000 synthetic images as sources.

To download the source images, use the following links and then unzip the downloaded files in a `source` subfolder.
- **RAISE, FLUX, Stable Diffusion 3.5, Latent Diffusion**: (first three provided by *B-Free* [[1]](https://arxiv.org/abs/2412.17671)), use [this link](https://www.grip.unina.it/download/prog/B-Free/extended_synthbuster/). You can verify the integrity using the checksums in the `checksum.txt` at the same link.
- **Stable Diffusion 1.4, Stable Diffusion 2, Stable Diffusion XL, Midjourney v5, DALL-E 2, DALL-E 3, Firefly**: provided by *Synthbuster* [[2]](https://ieeexplore.ieee.org/abstract/document/10334046), use [their repository](https://github.com/qbammey/synthbuster)

[[1]](https://arxiv.org/abs/2412.17671) *Fabrizio Guillaro et al., A Bias-Free Training Paradigm for More General AI-generated Image Detection. (CVPR Workshops 2026)* \
[[2]](https://ieeexplore.ieee.org/abstract/document/10334046) *Quentin Bammey, Synthbuster: Towards detection of diffusion model generated images. IEEE Open Journal of Signal Processing, 2023* 

The subset of 100 source images for each folder used in AncesTree, along with the IQA score and detection scores (not calibrated), is listed in `sources.csv`.

To correctly reflect the naming in the CSV, ensure that the subfolders in the `source` folder are named as follows:
`real_raise_1024`, `stable-diffusion-1-4`, `stable-diffusion-2`, `stable-diffusion-xl`,  `sd3_large`, `latent-diffusion`, `midjourney-v5`,  `dalle2`, `dalle3`, `firefly`, `flux`.

## Directory structure

After downloading, you should have a structure like this:
```
data_AncesTree
├── AncesTree
│   ├── dalle2
│   ├── dalle3
│   ...
│   └── stable-diffusion-xl
├── source
│   ├── dalle2
│   ├── dalle3
│   ...
│   └── stable-diffusion-xl
├── code
├── AncesTree_dev.csv
├── AncesTree_test.csv
├── AncesTree_test_calibrated.csv
├── sources.csv
└── ...
```

## Custom AncesTree (code)

You can build your own AncesTree on a custom source dataset by running the script `code/run_ancestree.py`.
It will generate a degradation tree for each image, saving the degraded images and the corresponding `.npz` metadata on disk and creating a `custom_tree.csv` metadata CSV.

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