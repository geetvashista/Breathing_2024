import pathlib
import mne
import numpy as np
from mne.beamformer import apply_lcmv_epochs
import os
import time

# Start a timer. This isn't really necessary

start = time.time()


# Setting verables

directory = r'C:\Users\em17531\Desktop\Breathing_Cleaned_data'
filter = mne.beamformer.read_beamformer(r'C:\Users\em17531\Desktop\Breathing_sorce_loc_files\Beamformer_filter')


# Loading needed data

data = []
list_of_participants = []

folder = pathlib.Path(directory).glob('*')
for file in folder:
    list_of_participants.append(os.path.basename(file).replace('_Cleaned', ''))
    data.append(mne.read_epochs(file))


# Creating a new info object

ch_names = np.load(r'C:\Users\em17531\Desktop\Breathing_sorce_loc_files\Breathing_sorce_loc_files\ch_names.npy')

temp = data[0]
new_names = dict(
    (ch_name, ch_name.rstrip(".").upper().replace("Z", "z").replace("FP", "Fp"))
    for ch_name in temp[0].ch_names
)
del temp
info = mne.create_info(list(new_names.values()), sfreq=250, ch_types='eeg')


# importing and preparing parcellation map

labels = mne.read_labels_from_annot("fsaverage", "HCPMMP1", "both")
# DON'T FORGET TO GET RID OF THE FIRST TWO LABELS
# Use del labels[0]
del labels[0]
del labels[0]

# Clean up for memory

del directory
del file
del folder
del ch_names
del new_names

# Core Beamformer function

def network_soruce_parcellation(data):
    participant_index = 0
    for participant in data:
        # Preping matriecs
        temp_sham = participant['2'].get_data()
        sham_epoch = mne.EpochsArray(temp_sham, info=info)
        sham_epoch.set_eeg_reference(projection=True)

        temp_bud = participant['1'].get_data()
        buds_epoch = mne.EpochsArray(temp_bud, info=info)
        buds_epoch.set_eeg_reference(projection=True)

        # Applying filter

        stc_buds = apply_lcmv_epochs(buds_epoch, filter)
        stc_sham = apply_lcmv_epochs(sham_epoch, filter)

        # Converting to scaler

        vec_buds = stc_buds[0].magnitude()
        vec_sham = stc_sham[0].magnitude()

        # Parcellation for sham

        dec = {}
        for k in labels:
            index = labels.index(k)
            temp = str(labels[index])
            dec[temp] = vec_sham.in_label(k).data  # change here from buds to sham as needed

        j = 0
        while True:
            temp = dec[str(labels[j])]
            dec[str(labels[j])] = np.mean(temp, axis=0)
            j += 1
            if j >= 360:
                break

        list = [i for i in dec.values()]
        list_2 = [np.expand_dims(i, axis=0) for i in list]
        temp_sham = np.concatenate(list_2)

        # Save source matrix

        name = str(list_of_participants[participant_index])

        np.save(
            name + '_Sham_matrix',
            temp_sham
        )

        # Parcellation for sham

        dec = {}
        for k in labels:
            index = labels.index(k)
            temp = str(labels[index])
            dec[temp] = vec_buds.in_label(k).data  # change here from buds to sham as needed

        j = 0
        while True:
            temp = dec[str(labels[j])]
            dec[str(labels[j])] = np.mean(temp, axis=0)
            j += 1
            if j >= 360:
                break

        list = [i for i in dec.values()]
        list_2 = [np.expand_dims(i, axis=0) for i in list]
        temp_bud = np.concatenate(list_2)

       # Saving matrix
        np.save(
            name + '_Buds_matrix',
            temp_bud
        )
        participant_index += 1


# calling function

network_soruce_parcellation(data)


# Stop timer and print run time

end = time.time()
print("The time of execution of above program is :",
      (end-start), "_s")
