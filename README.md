# c5v
C5V Modeling Tool: Cornell COVID-19 Caseload Calculator with Capacity and Ventilators

How to Use the Cornell COVID Caseload Calculator C5V (Desktop Version):

Model created by 
Nathaniel Hupert MD, MPH,       Weill Cornell Medicine
Peter L. Jackson PhD,           Singapore University of Technology and Design
Michael G. Klein PhD,           San Jose State University
John A. (“Jack”) Muckstadt PhD, Cornell University

Implemented by Lior Shtayer & Vruj Patel, Weill Cornell Medical College 

For physicians and other COVID-19 responders who would like a tool to help hospital leaders think about hospital caseload projections in a structured way, here is the latest version of one that we have been developing at Cornell (by Nathaniel Hupert at Weill Cornell Medicine with Peter L. Jackson at Singapore University of Technology and Design, Michael G. Klein at San Jose State University, and John A. (“Jack”) Muckstadt at Cornell University) since mid-January, 2020.

For questions about the Cornell COVID Caseload Calculator C5V, please contact Walt Beadling at walt@cayugapartners.com or 610-841-1618.

This tool is designed to make an easily modifiable projection of med/surge and ICU bed requirements over an outbreak of specified type, for a specified catchment area (and market share of that area, to model your hospital system).

This model requires some things that are very hard to pin down, but may be informed by the work of any dynamics of infectious disease modelers in your midst (for those of you fortunate enough to have some).

The following model is a desktop version of several iterations of C5V which aims at simplifying and updating the hospitalizations and ICU fraction section to reflect current estimates for COVID-19. 

The inputs are:

    Catchment area population in (what are now month-old) CDC age strata
    Market share of that catchment area you are interested in modeling
    Overall population attack or infection rate (note that there is a big debate going on in the modeling community about whether this number is VERY high with a small clinically apparent fraction, thus explaining the speed of spread, or not quite so high with a larger clinically apparent fraction)
    Percent symptomatic (same comment)
    Hospitalization fraction of symptomatics (based on CDC parameters but modifiable to fit your local circumstances)
    ICU-bound fraction (same, and also “tunable” between the CDC’s “Mild Attack Scenario” and “Severe Attack Scenario” so that you can, e.g., make the Severe scenario have a higher ICU admission rate than the Mild scenario)

And:

    Time of peak of epidemic curve (technically the mode of the chosen gamma distribution)
    Shape of the overall epidemic curve, from “flat” (even though it is not very flat) to quite peaked.
    Length of stay in both a medical/surgical and ICU bed defined by minimum and maximum days, with the model pulling a UNIFORM distribution from that (not optimal, but avoids having to use a macro)
    Mortality fraction in both locations
    Increase (>100%) or decrease (<100%) in LOS for those who die

The distributed version is called “hypothetical” because I put in a purely fictional population.

Modeling methodology

The Cornell COVID Caseload Calculator C5V combines mathematical calculation and deterministic simulation to provide estimates of both

A) the rate at which patients in a designated catchment area may present for hospitalization due to the initial 2020 wave of SARS-CoV-2 causing COVID-19 disease, and

B) the simulated hospital load caused by those patients to both medical/surgical and intensive care units, with specific attention paid to identifying the magnitude and timing of the peak daily hospital census for regular and critical care beds throughout the catchment area. 

Critical user input to run the model includes actual or estimated age-structured catchment population; overall (final) infection rate; percent (a)symptomatic cases; symptomatic case hospitalization and  critical care ratios (both starting from U.S. Centers for Disease Control and Prevention (CDC) estimates); day of peak of epidemic curve; and shape of epidemic curve.  The latter two may be estimated from epidemiological models (e.g., the Oxford-Cornell COVID INTERNATIONAL MODEL), and may be checked by day-to-day correlation with actual hospital admission rates for medical/surgical and critical care beds.

Next Steps

We are working diligently to accomplish the following:

    Web Python version (led by Michael Klein at San Jose State)
    Linkage with a country-specific, live data-driven R-based epidemic curve generator developed by the CoMo Collaborative’s COVID19 International Model (led by Lisa White at Oxford)
