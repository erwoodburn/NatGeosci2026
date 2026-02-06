Data from “Warming and snow loss increase reliance on old groundwater in a Colorado River headwater”
This repository contains the data and code associated with the paper titled "Warming and snow loss increase reliance on old groundwater in a Colorado River headwater", published in Nature Geoscience. 
Data Reference
Data was developed on GitHub and published on ESS-DIVE for long term preservation. The files on GitHub and ESS-DIVE are up-to-date. Per the Watershed Function SFA’s data usage policy, we ask that you cite this data from the ESS-DIVE repository. 

Cite this data as follows:
> Siirila-Woodburn E ; Nicholas T ; Newcomer M ; Rudisill W (2026): Data From: "Warming and snow loss increase reliance on old groundwater in a Colorado River headwater". Watershed Function SFA, ESS-DIVE repository. Dataset. http://doi.org/10.15485/3013287 

Manuscript Reference
This repository contains the data and code associated with the paper:
Siirila-Woodburn, E.R., et al., (2026) Warming and snow loss increase reliance on old groundwater in a Colorado River headwater, Nature Geoscience. (Full citation to be determined after publication).

Contents & Usage
ASO/: ​​Contains the bash and python scripts used to convert airborne snow observatory (ASO) data (ASO, 2023) in various data formats (georeferenced tiff file, NetCDF, UTM, and to latitude/longitude) then regrided to the ParFlow equivalent grid. Output data are in regrid_regll_data.zip and subsequently visualized and analyzed in plot_and_compare.py for Supplementary Figures A14 and A15. The wksht_ASO_comparison.xlsx spreadsheet is used to calculate the data for Supplementary Figure A16. 

EcoSLIM/: Contains the scripts and input files to run the EcoSLIM particle tracking simulations (/run_scripts) and the post-processing python script (/plot_scripts/eco_agedist_plots.ipynb). 

Jasechko et al./: Contains the jupyter notebook (Extract_Elevation.ipynb) to determine the outlet elevations of the 260 watersheds used in Jasechko et al. (2016), and the corresponding table, Table_S1_Watersheds_alt.csv. Used to create Supplementary Information Figure A2. 

PLM_Wells/: Contains the QA/QC-ed groundwater level time series of the PLM-1 and PLM-6 Monitoring Wells from Faybishenko et al. (2023), reformatted to water years used for Supplementary Figures A19 and and A20. 

ParFlow/: Contains the input files and run scripts to run ParFlow-CLM (/run_scripts), the python and tcl scripts to create and distribute the ParFlow forcing simulation files (/forcing), and various scripts and intermediary files to analyze the model outputs (/post_process).

SQUIRE/: Contains the processing scripts and intermediary files for the Surface QUantitatIve pRecipitation Estimation (SQUIRE) data (Grover, 2023) used to generate Supplementary Figure A18. 

USGS_Streamflow/: Contains the raw and gap-filled United States Geological Survey streamflow data (U.S. Geological Survey, 2026) used at the Almont station (site number 09112500). Gap-filling is performed in the R script with data from the Taylor station (site number 09110000). (/USGS_09112500_EAST_RIVER_AT_ALMONT_GAP_FILLED/code_almont_streamflow_gap_fill.Rmd).

discharge/: Contains the gap-filled discharge data at the Watershed Function SFA East River pumphouse site (Newcomer et al., 2022) used to generate Supplementary Figure A13 and to compute hourly Nash-Sutcliffe model efficiency coefficients (NSE) in Table A4.

snotel_and_flux_tower/: Contains the snow telemetry data (U.S. Department of Agriculture, 2024) from the Butte (site ID 380) and Schofield (site ID 737) stations, reformatted by water year, accessed with the snotelr R package. Used to create Supplementary Figure A17. Also contains the flux tower observational data (FluxTower_Pumphouse_ESS-DIVE.ET_only.h.txt) from Ryken et al. (2022) and sap flux transpiration data (MaxB_Transpiration_5Sites.daily_sums.h.txt) from Ryken (2021), used to create Supplementary Figures A22 and A23, respectively. 

References
Airborne Snow Observatory, ASO (2023): accessed 2023-11-15 at https://data.airbornesnowobservatories.com/

Faybishenko, B. Versteeg, R. Williams, K, Carroll, R., Dong, W., Tokunaga, T., O'Ryan, D. (2023): QA/QC-ed Groundwater Level Time Series in PLM-1 and PLM-6 Monitoring Wells, East River, Colorado (2016-2022). Watershed Function SFA, ESS-DIVE repository. Dataset. doi:10.15485/1866836 accessed via https://data.ess-dive.lbl.gov/datasets/doi:10.15485/1866836 on 2023-04-18

Grover, Maxwell, et al. (2023): “Surface QUantitatIve pRecipitation Estimation (SQUIRE) (XPRECIPRADARSQUIRE), 2021-12-01 to 2023-03-31, ARM Mobile Facility (GUC), Gunnison, CO; Supplemental Facility 2 (S2).” Atmospheric Radiation Measurement (ARM) User Facility, doi:10.5439/1884979. Accessed 2024-10-04

Jasechko, S., Kirchner, J. W., Welker, J. M. & McDonnell, J. J. (2016): Substantial proportion of global streamflow less than three months old. Nat. Geosci. 9, 126–129 (2016). https://doi.org/10.1038/ngeo2636

Newcomer, M., Carroll, R. Williams, K. (2022): Machine Learning Assisted Gap-Filled Discharge Data for the East River Community Watershed, Colorado, for Water Years 2014-2021. Watershed Function SFA, ESS-DIVE repository. Dataset. doi:10.15485/1868939 accessed via https://data.ess-dive.lbl.gov/datasets/doi:10.15485/1868939 on 2026-01-16

Ryken, A. (2021): Constraining Evapotranspiration and Understanding ET Drivers and Limitations in a Mountain Headwaters System. Colorado School of Mines ProQuest Dissertations & Theses,  2021. 28412923.

Ryken, A. C., Gochis, D. & Maxwell, R. M. (2022): Unravelling groundwater contributions to evapotranspiration and constraining water fluxes in a high‐elevation catchment. Hydrol. Process. 36, e14449 

U.S. Department of Agriculture, Natural Resource Conservation Service, National Water and Climate Center. Water and Climate Information System, Report Generator. Air and Water Database accessed via https://nwcc-apps.sc.egov.usda.gov/ on 2024-10-24

U.S. Geological Survey (2026): USGS Water Data for the Nation: U.S. Geological Survey National Water Information System database, accessed 2023-03-01, at https://doi.org/10.5066/F7P55KJN.

Contact and Corresponding Author
Erica R. Siirila-Woodburn
Earth and Environmental Sciences Area, Lawrence Berkeley National Laboratory
erwoodburn@lbl.gov 
Acknowledgements
This work was supported by the Watershed Function Science Focus Area at Lawrence Berkeley National Laboratory funded by the U.S. Department of Energy, Office of Science, Biological and Environmental Research under Contract No. DE-AC02-05CH11231 for authors ERSW, NT, MN, PJDF, MS, RC, KHW, and EB. This work was supported by the U.S. Department of Energy, Office of Science, Office of Biological and Environmental Research, and the Atmospheric System Research Program under U.S. Department of Energy Contract No. DE-AC02-05CH11231 for authors ERSW, WR, DF, and KHW. This research used resources of the National Energy Research Scientific Computing Center (NERSC), a U.S. Department of Energy Office of Science User Facility operated under Contract No. No. DE-AC02-05CH11231 using awards m2398 and m4098 for 2023-2025. The authors thank Dr. Anna Ryken for providing the flux tower and sap flux data used in the Supplemental Information Fig. A22 and Fig. A23.
