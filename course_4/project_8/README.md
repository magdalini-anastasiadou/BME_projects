# Project topic: Processing and Analysis of PPG/ECG
Course: Biomedical data acquisition and signal processing

Coordinator: Professor Kugiumtzis Dimitris

Students: Magdalini Anastasiadou & Chrysanthi Ntasioti

## Introduction
- The dataset for the project was [“BIDMC PPG and Respiration Dataset”](https://physionet.org/content/bidmc/1.0.0/).
- The dataset was acquired from 53 critically ill patients under hospital care. 
- Each recording lasted 8 minutes, containing
physiological signals such as Photoplethysmography (PPG), and
Electrocardiography (ECG), all sampled at 125 Hz. 

## Task
The aim of this project was to investigate the possibility of using PPG signals to monitor the
HR of critically ill patients, this is assessed compared to using ECG signals.

## Methodology
1. Pre-processing and Filtering

        a. Detrending
        b. High pass filter (cutoff frequency at 0.5 Hz to correct the baseline)
        c. Low pass filter (cutoff frequency at 50 Hz to decrease the noise)
        d. Normalization

<div style="display: flex; justify-content: space-around;">
    <img src="ekg_patient_21.jpg" alt="EKG Patient 21" style="width: 45%;"/>
    <img src="ppg_patient_21.jpg" alt="PPG Patient 21" style="width: 45%;"/>
</div>

2. HR Extraction

HR estimated at a rate of 4Hz from each signal and extracted from a sliding time window of 60 sec.
<div style="display: flex; justify-content: space-around;">
    <img src="ppg&ekg.jpg" alt="EKG & PPG" style="width: 100%;"/>
</div>

        a. ECG HR using Pan-Tompkins
        b. PPG HR using peak detection and SDSD minimization.

3. Comparison of Results

        a. Statistical
        b. Visual
        
<div style="display: flex; justify-content: space-around;">
    <img src="mae.png" alt="Mean Absolute Error" style="width: 45%;"/>
    <img src="hist_mae.png" alt="Histogram of MAE" style="width: 45%;"/>
</div>

<div style="margin-bottom: 20px;"></div>

<div style="display: flex; justify-content: space-around;">
    <img src="patient8.png" alt="Patient 8" style="width: 45%;"/>
    <img src="patient8_bland_altman.png" alt="Patient 8 Bland Altman" style="width: 45%;"/>
</div>

<div style="margin-bottom: 20px;"></div>

<div style="display: flex; justify-content: space-around;">
    <img src="patient35.png" alt="Patient 35" style="width: 45%;"/>
    <img src="patient35_bland_altman.png" alt="Patient 35 Bland Altman" style="width: 45%;"/>
</div>

<div style="margin-bottom: 20px;"></div>

<div style="display: flex; justify-content: space-around;">
    <img src="patien44.png" alt="Patient 44" style="width: 30%;"/>
    <img src="patient_44_bland_altman.png" alt="Patient 44 Bland Altman" style="width: 30%;"/>
    <img src="noise_patient_44.jpg" alt="Noise Patient 44" style="width: 30%;"/>
</div>


4. Conclusions

        a. PPG is promising in replacing ECG for HR monitoring
        b. The maximum absolute error:7.77 (Patient 19)
        c. More thorough analysis - critically ill patients
        d. PPG less accurate data for heart rate measurement compared to ECG 
