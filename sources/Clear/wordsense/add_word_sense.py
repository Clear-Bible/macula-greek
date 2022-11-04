# require lxml 4.9.1
from lxml import etree
import os
import pandas as pd
from collections import OrderedDict

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

WORD_SENSES = "SensesNT.csv"

LOWFAT_SOURCE = "../../../Nestle1904/lowfat"
NODES_SOURCE = "../../../Nestle1904/nodes"

LOWFAT_DEST = "lowfat"
NODES_DEST = "nodes"

NAMESPACE = "{http://www.w3.org/XML/1998/namespace}id"

# Create a dictionary from the sense data mapping each strong
# number to all instances for which we have a generated sense.
def getSenseDataDict():

    senseDict = {}

    df = pd.read_csv(os.path.join(DIR_PATH, WORD_SENSES), dtype=str)

    for index, row in df.iterrows():

        strong = row['StrongNumber']
        sense = row['SenseNumber']
        # Create a key for each instance.
        try:
            
            instances = row['Instances'].split()
            if strong not in senseDict:
                senseDict[strong] = {}

            for inst in instances:
                senseDict[strong][inst] = sense

        # There were no instances.
        except:
            continue

    return senseDict


# Add leading 0s when len(strong) < 4.
def addZeros(strong):

    strongPadded = "" + strong
    l = 4 - len(strong)

    while l > 0:
        strongPadded = "0" + strongPadded 
        l -= 1

    return strongPadded


# Write the word sense data into the trees.
def addWordSenseDataToNodes(source, destination):
    
    source = os.path.join(DIR_PATH, source)
    destination = os.path.join(DIR_PATH, destination)
    senseDict = getSenseDataDict()
    files = sorted(os.listdir(source))
    missingData = {}

    # Only use the 27 manuscripts of the NT -- ignore other files.
    for filename in files[:27]:

        readpath = os.path.join(source, filename)
        writepath = os.path.join(destination, filename)

        tree = etree.parse(readpath)
        root = tree.getroot()
        
        for element in root.iter('Node'):
            # Only use Nodes with an xml:id.
            try:
                # Don't include the id prefix 'n'.
                id = element.attrib.get(NAMESPACE)[1:]
            except:
                continue
            # '0010' is at the end of nodes in Sense file.
            idPadded = id + '0010'
            strong = element.attrib.get('StrongNumber')
            strongPadded = addZeros(strong)

            try:
                senseNumber = senseDict[strongPadded][idPadded]
                element.set('Sense', senseNumber)

            except:

                if strongPadded not in missingData:
                    missingData[strongPadded] = id

                elif strongPadded in missingData:
                    missingData[strongPadded] += " " + id

        # Write updated xml tree to file. 
        tree.write(open(writepath, 'wb'))

    return missingData


# Write the word sense data into the trees.
def addWordSenseDataToLowfat(source, destination):
    
    source = os.path.join(DIR_PATH, source)
    destination = os.path.join(DIR_PATH, destination)
    senseDict = getSenseDataDict()
    files = sorted(os.listdir(source))
    missingData = {}

    # Only use the 27 manuscripts of the NT -- ignore other files.
    for filename in files[:27]:

        readpath = os.path.join(source, filename)
        writepath = os.path.join(destination, filename)

        tree = etree.parse(readpath)
        root = tree.getroot()
        
        for element in root.iter('w'):
            # Don't include the id prefix 'n'.
            id = element.attrib.get(NAMESPACE)[1:]
            # '0010' is at the end of nodes in Sense file.
            idPadded = id + '0010'
            strong = element.attrib.get('strong')
            strongPadded = addZeros(strong)

            try:
                senseNumber = senseDict[strongPadded][idPadded]
                element.set('sense', senseNumber)

            except:

                if strongPadded not in missingData:
                    missingData[strongPadded] = id

                elif strongPadded in missingData:
                    missingData[strongPadded] += " " + id

        # Write updated xml tree to file. 
        tree.write(open(writepath, 'wb'))

    return missingData


# missingDataFromNodes = addWordSenseDataToNodes(NODES_SOURCE, NODES_DEST)
# missingDataFromLowfat = addWordSenseDataToLowfat(LOWFAT_SOURCE, LOWFAT_DEST)

# print(f"\n\nNodes that are lacking word sense data: \n{missingDataFromNodes}\n")