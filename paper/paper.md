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

date: 1 February 2020
bibliography: paper.bib
---

# Summary
 
Major storms along the coastline can damage infrastructure and leave deposits of sediment and debris. Synoptic aerial imagery
is often used to assess damage and impacts from storm events. A key source for this imagery in the US is the Emergency
Response Imagery (ERI) collected by the the National Geodetic Survey (NGS) Remote Sensing Division of the US National 
Oceanographic and Atmospheric Administration [@NOAA2020]. This imagery aids in recovery efforts as well as rapid assessment of 
storm impacts along developed and undeveloped coastlines [@Madore2018]. 

Post-event imagery is typically large, both in terms of the number of individual image files and the size of each file. For 
example, Hurricane Florence (2018) has over 29,000 JPEG images, with an average size of 7.7 Mb. The first steps for extracting 
information from these data involve acquiring and processing images. NOAA ERI is currently available as a Web Map 
Tile Service or via download using a graphical user interface 
[directing users to the relevant tar and ZIP archive; @NOAA2020]. To enable users to download NOAA ERI images via command line 
for use in reproducible computational workflows, we developed a Python module (`psi-collect`). 

The key functionality of `psi-collect` is it allows users to download specific tar and ZIP archives based on storm name,
date of image acquisition (day, month, and/or year), and/or image type (JPEG, TIFF). Users can also filter and select specific 
files using regular expressions. The module includes an automatic resumption feature in the event that a download 
is interrupted. Each tar and ZIP archive is checked for integrity of contents upon download completion to ensure that 
data are accurate and intact.

The module also functions as a tool for managing a user’s library of images — users can quickly understand which storms
they have downloaded. A cataloging tool is also supplied, which allows users to build CSV files that display key
information for each image such as image name, acquisition data, file size, and latitude and longitude for each corner
of image (extracted from the associated `.geom` file). This catalog can be used for statistical and spatial analyses. 

`psi-collect` addresses four issues experienced by researchers working with large collections of NOAA post storm aerial 
imagery. First, users previously needed to manually navigate to each storm and individually download the multiple image 
`.tar`/ `.zip` archives. Download could be done with the graphical user interface, or via another technique (e.g., `wget` on 
Linux). Even though `wget` is a command line method for retrieving the data, users would still be required to manually 
navigate and include individual web addresses for each storm archive (e.g., there are 15 individual archives for Hurricane 
Florence). `psi-collect` dynamically traverses pages and downloads archives when given specific filtering/sub-setting criteria 
(i.e., downloading all archives from Hurricane Florence).

Second, the individual image archives are large, and downloads often freeze or terminate early. Some browsers or software 
tools may be capable of resuming partial downloads, but this is case specific and depends on the retrieval workflow. 
Terminated downloads may require users to determine the missing archive, and re-initiate a download. `psi-collect` implements 
both automatic resumption and post-download integrity checks to manage download interruption.

Third, we have observed that download speeds can be slow. `psi-collect` handles queuing of downloads, and cataloging what 
downloads exist on a user's local computer. These features aid users when multiple archives are needed.

Fourth, `psi-collect` implements a soft locking mechanism allowing users to simultaneously download archives on multiple 
computers that upload to a single network file system or integrate with a distributed file systems (e.g., Hadoop). The locking 
system creates a text file with the same named as the archive, but with an additional ending ('xxxx.tar.lock'). This file 
has information about what user is downloading that archive, download progress, and how large the archive will be when 
downloading is complete (and the archive is fully uploaded). This file is updated regularly as the download progresses. 
  
# Statement of Need

`psi-collect` enables scientists to download NOAA Emergency Response Imagery via Python in a variety of ways (via date, 
storm),and obtain metrics on downloaded images though the cataloging functions. We envision that `psi-collect` could be 
used to develop reproducible computational workflows to analyze post-event imagery. For example, images can be used to: assess 
damage to the built environment [e.g., @Thomas2014], categorize impact in the context of the @Sallenger2000 Storm 
Impact Scale [e.g., @Liu2014; @Goldstein2020], evaluate forecasts of storm impact [@Morgan2019], measure the morphology 
of storm deposits [e.g., @Overbeck2015; @Lazarus2016], and study how human development controls the shape of sediment and 
debris deposits [e.g., @Rogers2015].

# Acknowledgements

We thank Chris Leaman for a thoughtful review and several contributions to the code during the review process. 
EBG acknowledges funding from NSF (Award #1939954), The Leverhulme Trust (RPG-2018-282), and an Early-Career Research
Fellowship from the Gulf Research Program of the National Academies of Sciences, Engineering, and Medicine. The content
is solely the responsibility of the authors and does not necessarily represent the official views of the Gulf Research
Program of the National Academies of Sciences, Engineering, and Medicine.


# References
