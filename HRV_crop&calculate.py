# AUTHOR: Geet Vashista (gv.3721@hotmail.co.nz)
# DATE: 11/06/2024

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import neurokit2 as nk

# Setting some backend parameters
plt.matplotlib.use('Qt5Agg')

# Set parameters
file_path = r'C:\Users\em17531\Desktop\951.csv'  # File path to raw ECG data
ECG_column_name = 'Sensor-B:EEG'  # The header of the colum as a string in the raw file
sfreq = 2048  # Sampling frequency
Window_interval = 10  # Window size in seconds, Change as desired
Plot = True  # Set to True if a plot output is desired

# Get data
df = pd.read_csv(file_path)
data = df[ECG_column_name]
del df
del file_path
del ECG_column_name

# Def cropping window cropping function
def crop_into_windows(series, window_size):
    list = []
    start = 0
    stop = window_size
    for i in series:
       hold = series[start:stop]
       list.append(hold)
       start = start + window_size
       stop = stop + window_size
       if stop >= len(series):
           break
    return list

# Crop data into windows
windows = crop_into_windows(data, (sfreq * Window_interval))

# Def loop to find the HRV for each window
def HRV_time_over_windows(windows, sfreq):
    HRV_time = []
    for i in windows:
        # Find peaks
        peaks, info = nk.ecg_peaks(i, sfreq)

        # Find HRV
        hrv_time = nk.hrv_time(peaks=peaks, sampling_rate=sfreq, show=False)
        HRV_time.append(hrv_time)
    return HRV_time

# Calculate HRV by windows
HRV_by_windows = HRV_time_over_windows(windows, sfreq)

if Plot == True:
    # Plot HRV across windows
    # The 0 position is mean_NN, change as desired
    # See nk.hrv_time documentation for options
    # https://neuropsychology.github.io/NeuroKit/functions/hrv.html#hrv-time
    array = np.array(HRV_by_windows)
    plt.plot(array[:, 0, 0])
    plt.show()
