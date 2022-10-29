import os
import sys
import glob
import getpass
import splusdata
import pandas as pd

"""
Downloads a S-PLUS iDR4 query for a list of fields.
"""

###############################################################################
#
# User inputs
#
###############################################################################

###############################################################################
# Directory in your computer where you want the outputs to be saved.
# Be aware that this can result in huge amounts of data, depending on the query

save_path = "../CHANCES-target-selection/tables/gr_petro/"

###############################################################################
# Name to be added in the beginning of the output files names

base_name = "stripe82"

###############################################################################
# Query that will be run for each field. The name of the field will
# automaticaly replace the string {field}

query = """

SELECT
det.ID, g.g_petro, r.r_petro

FROM
idr4_dual.idr4_detection_image AS det
JOIN idr4_dual.idr4_dual_g     AS g     ON (det.ID = g.ID)
JOIN idr4_dual.idr4_dual_r     AS r     ON (det.ID = r.ID)

WHERE
(det.Field = \'{field}\')
AND (g.g_petro < 30)
AND (r.r_petro < 30)

"""

###############################################################################
# User and password for the splus.cloud
#
# Safest option:
# Leave it as None to be prompted to write it only when executing the script

splus_cloud_user = 'elosch'
splus_cloud_pass = '@Hydra-Kentaurus1987'

###############################################################################
# Additional inputs

overwrite = True  # Outputs will overwrite existing files

remove_individual = False  # Removes individual files after combining catalogs

###############################################################################
#
# Starting the script
#
###############################################################################

# Run message

message = """
###############################################################################
#                                                                             #
#      Download S-PLUS iDR4 data for a list of fields (or single field)       #
#                                                                             #
###############################################################################

The script you are about to run will send queries to the S-PLUS iDR4 database
and download the results.

### See below the query that will be run for each field:
-------------------------------------------------------------------------------
{query}
-------------------------------------------------------------------------------

### The output data will be stored in the following directory:

{save_path}

### If you want to make changes to this query, or change the output directory,
open and edit this file:

{script_file}

#####
If you are ready to run the script, press enter.
"""

script_file = __file__

print(message.format(query       = query,
                     save_path   = save_path,
                     script_file = script_file
                     ))
input("")

###############################################################################
# Get other inputs

field_list_error = """You must provide a .csv field list (or field name):

Usage:
$ python3 idr4_data_download.py *field_list*

Replace *field_list* with:
- The name of a field in S-PLUS iDR4
- A .csv file with S-PLUS iDR4 fields listed under the column named "Field"

Example:
$ python3 idr4_data_download.py iDR4_pointings.csv

*Check the iDR4 documentation in splus.cloud for the list of fields in iDR4
"""

try:
    fields_file = sys.argv[1]
except IndexError:
    raise ValueError(field_list_error)

###############################################################################
# Get username and password if not given as an input

if splus_cloud_user is None:
    print("Login to splus.cloud to access internal data")
    splus_cloud_user = input("user:")
    splus_cloud_pass = getpass.getpass("password:")

# Connect to the splus internal database
conn = splusdata.connect(splus_cloud_user, splus_cloud_pass)


###############################################################################
# Read field name or list of fields

extension = os.path.splitext(fields_file)[1]
if extension == ".csv":
    fields_data = pd.read_csv(fields_file, sep=',')
    fields = list(fields_data["Field"])

elif "." in fields_file:
    raise ValueError(f"Extension {extension} is not supported (use .csv)")

else:
    fields = [fields_file]

print("")
print(f"Running query for {len(fields)} Fields.")
print("")

###############################################################################
# Prepare output files names

all_filenames = []
for field in fields:

    save_file_name = f"{base_name}_{field}.csv"
    save_file      = os.path.join(save_path, save_file_name)

    all_filenames.append(save_file)

###############################################################################
# Run query for each field and save results

for field, field_file in zip(fields, all_filenames):

    print(f"Running {field}")

    # Get field query
    field_query=query.format(field = field)

    # Send query and retrieve result
    query_table = conn.query(query)

    # Save the file
    query_table.write(field_file , format='csv', overwrite=overwrite)

    print(f"{field} Finished.")
    print("")

###############################################################################
# Combine results

print("Combining individual catalogs.")

# os.chdir(save_path)

#combine all files in the list
combined_csv  = pd.concat([pd.read_csv(f) for f in all_filenames])

#export to csv
final_file = os.path.join(save_path, f"{base_name}.csv")
combined_csv.to_csv(final_file, index=False)

print("")

###############################################################################
# Remove individual files

if remove_individual:
    print("Removing individual files.")
    for field_file in all_filenames:
        cmd = f"rm {field_file}"
        print(cmd)
        os.system(cmd)

    print("")


print("Finished")
