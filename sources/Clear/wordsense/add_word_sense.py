import os
import csv
import pandas as pd
from collections import OrderedDict

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

WORD_SENSES_FILE = "SensesNT.csv"
WRITE_FILE = 'greek-wordsenses.tsv'

header = ['macula_greek_word_id', 'sense_number']

# Source and destination sense data paths.
source_path = os.path.join(DIR_PATH, WORD_SENSES_FILE)
dest_path = os.path.join(DIR_PATH, WRITE_FILE)

# Create a dictionary from the sense data mapping each strong
# number to all instances for which we have a generated sense.
def get_sense_data_dict(source_path:str=source_path) -> dict:

    sense_dict = {}
    # Read the sense csv into a dataframe with string values. 
    df = pd.read_csv(source_path, dtype=str)

    for index, row in df.iterrows():

        strong = row['StrongNumber']
        sense = row['SenseNumber']
        # Create a key for each instance.
        try:
            
            instances = row['Instances'].split()
            if strong not in sense_dict:
                sense_dict[strong] = {}

            for inst in instances:
                sense_dict[strong][inst] = sense

        # There were no instances.
        except:
            continue

    return sense_dict


# Sense ids look like: 430030160120010.
# Reformat to have n prefix and no '0010' suffix.
# E.g., 'n43003016012'
def get_id_formatted(id:str) -> str:

    id_formatted = 'n' + id[:-4]
    return id_formatted


def write_sense_data_formatted(source_path:str=source_path, dest_path:str=dest_path):

    with open(source_path, 'r') as source:

        sense_data_dict = get_sense_data_dict()
        # Get the total number of word ids in the sense data dictionary. 
        word_ids_count = sum(
            [len(sense_data_dict[strong]) for strong in sense_data_dict.keys()])

        rows = []

        # Iterate over the sense data dictionary, adding ids and senses to rows. 
        for strong, ids in sense_data_dict.items():
            for id, sense in ids.items():
                id_formatted = get_id_formatted(id)
                rows.append([id_formatted, sense])

        # Ensure the correct amount of word ids. 
        assert word_ids_count == len(rows)
        
        # Write the results. 
        with open(dest_path, 'w') as tsvfile:

            writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')

            writer.writerow(header)
        
            for row in rows:
                writer.writerow(row)

write_sense_data_formatted()