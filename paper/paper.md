---
title: '`psi-collect`: A Python module for post-storm image collection and cataloging'
tags:
  - Python
  - coastal
  - storm 
  - morphology
  - hurricane
  - severe weather
  - NOAA
  
authors:
  - name: Matthew C. Moretz
    affiliation: 1
  - name: Daniel Foster
    affiliation: 1
  - name: John Weber
    affiliation: 1
  - name: Rinty Chowdhury
    affiliation: 1
  - name: Shah Nafis Rafique
    affiliation: 1
  - name: Evan B. Goldstein
    orcid: 0000-0001-9358-1016
    affiliation: 2
  - name: Somya D. Mohanty
    orcid: 0000-0002-4253-5201
    affiliation: 1
affiliations:
 - name: Department of Computer Science, The University of North Carolina at Greensboro
   index: 1
 - name: Department of Geography, Environment, and Sustainability, The University of North Carolina at Greensboro
   index: 2
date: <day> <month> <year>
bibliography: paper.bib
---

# Summary
 
Major storms along the coastline often leave deposits of sediment and debris. In developed settings, these deposits require significant clean-up, but this clean-up erases their signature and therefore precludes their study. Synoptic post-event aerial imagery is often the only curated record of these impacts. In the US, a key source for this imagery is the Emergency Response Imagery collected by the US National Oceanographic and Atmospheric Administration (NOAA, 2020). This imagery is often flown before significant clean up occurs, and allows for critical insight into storm impacts along developed and undeveloped coastlines. 

The NOAA post event imagery for storm events is typically large, both in terms of the number of individual image files and the size of each file. For example, Hurricane Florence (2018) has over 29,000 JPEG images, with an average size of 7.7 Mb. Extracting information from this library of synoptic imagery requires obtaining and processing these images. NOAA ERI is currently available through WTM services, or a GUI interface directing users to the relevant tar and zip files (NOAA ERI). To enable efficiently obtaining these images for use in a reproducible computational workflow we developed `psi-collect`, a python module for downloading the NOAA ERI images via a command line interface. 

The key functionality of `psi-collect` is it allows users to download specific tar and zip files based on storm name, date of image acquisition, image type (JPEG, TIFF). The module also functions as a tool for managing a user’s library of images — users can quickly understand which storms they have downloaded. A cataloging tool is also supplied, which allows users to build CSV files that display key information for each image such as image name, acquisition data, file size, and latitude and longitude for each corner of image (extracted from the associated `.geom` file). This catalog can be used for statistical and spatial analysis. 
  
# Statement of Need

`psi-collect` enables scientists to download NOAA response imagery via python in a variety of ways (via date, storm), and obtain metrics on downloaded images though the cataloging functions. We envision that `psi-collect` will be used to develop reproducible computational workflows to analyze post event imagery, e.g., automated classification and/or analysis of impacts from specific storms. For example images can be used to: assess damage to the built environment  (XXX), assess impact using the Sallenger (2000) Storm Impact Scale (e.g., Goldstein et al., 2020), measure the morphology of storm deposits (e.g., Lazarus, 2016), and study how human development controls the shape of sediment and debris deposits (e.g., Rogers et al., 2015).

# Acknowledgements

EBG acknowledges funding from NSF (Award #1939954), The Leverhulme Trust (RPG-2018-282), and an Early-Career Research Fellowship from the Gulf Research Program of the National Academies of Sciences, Engineering, and Medicine. The content is solely the responsibility of the authors and does not necessarily represent the official views of the Gulf Research Program of the National Academies of Sciences, Engineering, and Medicine.


# References
