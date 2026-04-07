---
layout: paper
paper: Quality-Aware Calibration for AI-Generated Image Detection in the Wild
github_url: https://github.com/grip-unina/QuAD
authors:  
  - name: Fabrizio Guillaro
    link: https://www.grip.unina.it/members/guillaro
    index: 1
  - name: Vincenzo De Rosa
    link: https://www.grip.unina.it/members/derosa
    index: 1
  - name: Davide Cozzolino
    link: https://www.grip.unina.it/members/cozzolino
    index: 1
  - name: Luisa Verdoliva
    link: https://www.grip.unina.it/members/verdoliva
    index: 1
affiliations: 
  - name: University Federico II of Naples, Italy
    index: 1
links:
    arxiv: https://arxiv.org/abs/XXXX.XXXX
    code: https://github.com/grip-unina/QuAD
---


<center>
 <img src="./teaser.svg" alt="teaser" width="100%" style="transform: scale(1.15);" />
</center>

Significant progress has been made in detecting synthetic images, however most existing approaches operate on a single image instance and overlook a key characteristic of real-world dissemination: as viral images circulate on the web, multiple near-duplicate versions appear and lose quality due to repeated operations like recompression, resizing and cropping. As a consequence, the same image may yield inconsistent forensic predictions based on which version has been analyzed.
In this work, to address this issue we propose **QuAD (Quality-Aware calibration with near-Duplicates)** a novel framework that makes decisions based on all available near-duplicates of the same image.
Given a query, we retrieve its online near-duplicates and feed them to a detector: the resulting scores are then aggregated based on the estimated quality of the corresponding instance. By doing so, we take advantage of all pieces of information while accounting for the reduced reliability of images impaired by multiple processing steps.
To support large-scale evaluation, we introduce two datasets: AncesTree, an in-lab dataset of 136k images organized in stochastic degradation trees that simulate online reposting dynamics, and ReWIND, a real-world dataset of nearly 10k near-duplicate images collected from viral web content. Experiments on several state-of-the-art detectors show that our quality-aware fusion improves their performance consistently, with an average gain of around 8\% in terms of balanced accuracy compared to plain average. 
Our results highlight the importance of jointly processing all the images available online to achieve reliable detection of AI-generated content in real-world applications.


## Bibtex

 ```
@InProceedings{guillaro2026quality,
    author    = {Guillaro, Fabrizio and De Rosa, Vincenzo and Cozzolino, Davide and Verdoliva, Luisa},
    title     = {Quality-Aware Calibration for AI-Generated Image Detection in the Wild},
    year      = {2026}
}
```

## Acknowledgments

coming soon




