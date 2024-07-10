import pandas as pd
import numpy as np
import splusdata
import os
import time
import logging
import threading
from tqdm import tqdm # Progress bar

# Establish a connection with SPLUS Cloud using your username and password
conn = splusdata.connect('elosch', '@Hydra-Kentaurus1987')

# Load file containing the fields to be downloaded
# See 'Query_Fields.txt' for how to get this file
All_Fields   = pd.read_csv('fields_hydra.csv')

# Set the output folder name
Output_Dir   = 'Fields_delete/'

# Create output folder if it doesn't exist
if os.path.isdir(Output_Dir) == False:
    os.makedirs(Output_Dir)

# These lines are used to verify if there are any downloaded files already.
Fields_Downloaded = [s.replace('.csv', '') for s in os.listdir(Output_Dir) if s.endswith('.csv')]
Field_List        = np.setdiff1d(All_Fields, Fields_Downloaded) # Fields that will be downloaded
Field_List        = pd.DataFrame(Field_List, columns=['field']) # Transforming it into a DataFrame so we don't need to change the code

# Aperture you want to download (this is the {aperture} in the code below)
# aperture = 'petro'
# print('# Downloading fields with %s aperture' %aperture)

def thread_function(dataframe):
    for key, value in dataframe.iterrows():
        print('Starting '+f'{value.field}')
        try:
            # This query is for public data
            My_Query = f"""
            SELECT
            det.ID, det.RA, det.DEC, sgq.PROB_GAL, sgq.CLASS, pz.odds, pz.zml,
            g.g_petro, r.r_petro, det.SEX_FLAGS_DET

            FROM
            idr4_dual.idr4_detection_image AS det
            JOIN idr4_vacs.idr4_star_galaxy_quasar AS sgq ON (det.ID = sgq.ID)
            JOIN idr4_vacs.idr4_photoz AS pz ON (det.ID = pz.ID)
            JOIN idr4_dual.idr4_dual_g 	AS g 	ON (det.ID = g.ID)
            JOIN idr4_dual.idr4_dual_r 	AS r 	ON (det.ID = r.ID)

            WHERE
            (det.Field = '{value.field}')
            AND (g.g_petro < 30)
            AND (r.r_petro < 30)
            """

            # Make the query
            Result = conn.query(My_Query, publicdata=False)

            # Save the resulting table to the output folder as a csv
            Result.write(f'{Output_Dir}{value.field}.csv') # To save the resulting table

        # If a given field could not be downloaded for some reason, this will print the name of the field
        except:
            print(f"Error on {value.field}")

# To speed-up the download of data we use multithreading.
Num_Parallel = 5 # The number of files downloaded in parallel (but sometimes it will download this number -1)
Threads = np.arange(0, len(Field_List), 1) # The number of threads (each thread will be used to download a field)

print('# Number of fields: ', len(Field_List))
print('# Number of simultaneous downloads:', Num_Parallel)

# Create a dictionary to store the processes (threads)
Processes = {}

# Populating the dictionary with the processes (one thread per item of the dictionary, each thread downloads a field)
for i in range(len(Threads)-1):
    Processes[i] = threading.Thread(target=thread_function, args=(Field_List[Threads[i]: Threads[i+1]],))

# Starting the threads (downloading 5 at a time to not overload the cloud)
for list_of_fields in np.array_split(np.arange(0, len(Threads)), np.ceil(len(Threads)/Num_Parallel)):
    print('# Starting threads:', list_of_fields)
    for i in list_of_fields:
        Processes[i].start()
        time.sleep(1.5)

    for i in list_of_fields:
        Processes[i].join()
    print('# Finished threads:', list_of_fields)
    print()

# Concatenate fields
print('# Concatenating fields...')
Files = [s for s in os.listdir(Output_Dir) if s.endswith('.csv')] # Get list of fields that were downloaded

# In a loop, append each field as a Pandas DataFrame into the DFs list
DFs = []
for file in Files:
    DFs.append(pd.read_csv(Output_Dir+file))

# Concatenate the DFs
Concat_DF = pd.concat(DFs)

# Reset index
Concat_DF = Concat_DF.reset_index(drop=True)

# Save to file
Concat_DF.to_csv(Output_Dir+'Hydra-iDR4.csv', index=False) # Save as a final catalogue
print('# Done')
