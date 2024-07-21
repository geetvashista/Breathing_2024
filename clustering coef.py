import numpy as np
import bct
from scipy import stats

# buds_clust_coef = bct.clustering_coef_wu(buds)

# load data

Beta_buds = np.load('Beta_buds_wpli.npy')
Beta_sham = np.load('Beta_sham_wpli.npy')

Alpha_buds = np.load('Alpha_buds_wpli.npy')
Alpha_sham = np.load('Alpha_sham_wpli.npy')

Theta_buds = np.load('Theta_buds_wpli.npy')
Theta_sham = np.load('Theta_sham_wpli.npy')

# Load senser data

Buds_master = np.load('sensor_space_buds.npy')
Sham_master = np.load('sensor_space_sham.npy')

Buds_master = np.mean(Buds_master, axis= 1)
Sham_master = np.mean(Sham_master, axis= 1)

Beta_buds = Buds_master[:, :, :, 1]
Beta_sham = Sham_master[:, :, :, 1]

Alpha_buds = Buds_master[:, :, :, 2]
Alpha_sham = Sham_master[:, :, :, 2]

Theta_buds = Buds_master[:, :, :, 3]
Theta_sham = Sham_master[:, :, :, 3]

del Buds_master
del Sham_master


# clustering coefficient

#### Theta #####
Theta_buds_clustering_temp = []
for i in range(0, 14):
    temp_array = bct.clustering_coef_wu(Theta_buds[i, :, :])
    Theta_buds_clustering_temp.append(temp_array)
    del temp_array
Theta_buds_clustering = np.array(Theta_buds_clustering_temp)
del Theta_buds_clustering_temp

Theta_sham_clustering_temp = []
for i in range(0, 14):
    temp_array = bct.clustering_coef_wu(Theta_sham[i, :, :])
    Theta_sham_clustering_temp.append(temp_array)
    del temp_array
Theta_sham_clustering = np.array(Theta_sham_clustering_temp)
del Theta_sham_clustering_temp

    # Zeroing negative phasing
# Theta_buds_Betweenness[Theta_buds_Betweenness<0] = 0
# Theta_sham_Betweenness[Theta_sham_Betweenness<0] = 0

    # Stats
T_val, p_val_theta = stats.ttest_rel(Theta_buds_clustering, Theta_sham_clustering)
np.nan_to_num(p_val_theta, copy=False, nan=1)
clustering_Theta_fdc = stats.false_discovery_control(p_val_theta)

### Alpha ###

Alpha_buds_clustering_temp = []
for i in range(0, 14):
    temp_array = bct.clustering_coef_wu(Alpha_buds[i, :, :])
    Alpha_buds_clustering_temp.append(temp_array)
    del temp_array
Alpha_buds_clustering = np.array(Alpha_buds_clustering_temp)
del Alpha_buds_clustering_temp

Alpha_sham_clustering_temp = []
for i in range(0, 14):
    temp_array = bct.clustering_coef_wu(Alpha_sham[i, :, :])
    Alpha_sham_clustering_temp.append(temp_array)
    del temp_array
Alpha_sham_clustering = np.array(Alpha_sham_clustering_temp)
del Alpha_sham_clustering_temp

    # Zeroing negative phasing
# Alpha_buds_Betweenness[Alpha_buds_Betweenness<0] = 0
# Alpha_sham_Betweenness[Alpha_sham_Betweenness<0] = 0

# Stats
T_val, p_val_alpha = stats.ttest_rel(Alpha_buds_clustering, Alpha_sham_clustering)
np.nan_to_num(p_val_alpha, copy=False, nan=1)
clustering_alpha_fdc = stats.false_discovery_control(p_val_alpha)

### Beta ####

Beta_buds_clustering_temp = []
for i in range(0, 14):
    temp_array = bct.clustering_coef_wu(Beta_buds[i, :, :])
    Beta_buds_clustering_temp.append(temp_array)
    del temp_array
Beta_buds_clustering = np.array(Beta_buds_clustering_temp)
del Beta_buds_clustering_temp

Beta_sham_clustering_temp = []
for i in range(0, 14):
    temp_array = bct.clustering_coef_wu(Beta_sham[i, :, :])
    Beta_sham_clustering_temp.append(temp_array)
    del temp_array
Beta_sham_clustering = np.array(Beta_sham_clustering_temp)
del Beta_sham_clustering_temp

    # Zeroing negative phasing
# Beta_buds_Betweenness[Beta_buds_Betweenness<0] = 0
# Beta_sham_Betweenness[Beta_sham_Betweenness<0] = 0

# Stats
T_val, p_val_beta = stats.ttest_rel(Beta_buds_clustering, Beta_sham_clustering)
np.nan_to_num(p_val_beta, copy=False, nan=1)
clustering_Beta_fdc = stats.false_discovery_control(p_val_beta)

# Extras

band = p_val_theta

temp_list = list(band)
index = []
for i in band:
    if i <= 0.05:
        index.append(temp_list.index(i))
print(index)
print([band[i] for i in index])


temp = 0
for i in p_val_alpha:
    if i <= 0.05:
        temp += 1
print(temp)

T_sham_temp = np.average(Theta_sham_clustering, axis=0)
T_buds_temp = np.average(Theta_buds_clustering, axis=0)
A_sham_temp = np.average(Alpha_sham_clustering, axis=0)
A_buds_temp = np.average(Alpha_buds_clustering, axis=0)
B_sham_temp = np.average(Beta_sham_clustering, axis=0)
B_buds_temp = np.average(Beta_buds_clustering, axis=0)

print(B_sham_temp[283])
print(B_buds_temp[283])