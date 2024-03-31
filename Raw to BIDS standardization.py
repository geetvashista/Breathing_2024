import matplotlib
import pathlib
import mne
import mne_bids

matplotlib.use('Qt5Agg')


# Import raw data

file = pathlib.Path(r'C:\Users\em17531\Downloads\242\242\Acquisition 01.dat')
raw = mne.io.read_raw_curry(file, preload=True)


# Set line freq info

raw.info['line_freq'] = 50


# Set participant details

subject = '01'
task = 'breathing augmentation'


# BIDS write up

out_path = pathlib.Path(r'C:\Users\em17531\Desktop\BIDS')  # Change to desired output folder

bids_path = mne_bids.BIDSPath(subject=subject,
                              task=task,
                              root=out_path)

mne_bids.write_raw_bids(raw,
                        bids_path=bids_path,
                        format='BrainVision',
                        allow_preload=True,
                        overwrite=False
                        )

# Note that the format of the raw data in the BIDS organization is now BrainVision, not curry.
