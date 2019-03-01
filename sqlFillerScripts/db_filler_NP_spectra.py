#!/usr/bin/env python
import sqlite3;
import sys;

"""
Turns the given spectra file in to a a list of lists. each list contains 1 spectra (from Begin IONS to End IONS)
first variable is th path to the spectra file (Mgf format).
spectraPath = path to the spectra.
"""
def makeSpectraList(spectraPath):
    spectraList = [];
    spectra = [];
    for line in open(spectraPath):
        #end of a spectra is indicated with END IONS so when it appears 
        #all data stored in the the list is added to the spectraList
        #and the list is emptied for the next spectra
        if line.startswith("END IONS"):
            if spectra != []:
                spectra.append(line);
                #sends the spectra (list of all the lines in the spectra) and the spectraZip to the method remakeSpectra.
                spectraList.append(spectra);
                spectra = [];
        elif line == "\n":
            pass;
        else: 
            spectra.append(line.strip());
    return spectraList;

"""
checks the number of identifiers present in the mgf entry and creates a dictionary of these.
spectra =  the spectra entry in the mfg
numOfIdentifiers = the number of lines in the spectra that belong to the identifiers.
returns: a dict containing the identifiers as Keys and theirs values as value.
"""
def makeMgfIdentifierIndex(spectra,numOfIdentifiers):
    identifierDict = {};
    for identifierIndex in range(1,numOfIdentifiers):
        splitIdentifier = spectra[identifierIndex].split("=");
        identifierDict[splitIdentifier[0]] = splitIdentifier[1];
        
    return identifierDict;

"""
takes a experiment name and description and adds these to the NP database along with a created ID.
fileName = name of the file which will become the Name of the experiment.
description = small explanation of the experiment.
databasePath = path to the NP database.
returns: experimentID
"""
def experimentTableFiller(fileName, description, databasePath):
    db = sqlite3.connect(databasePath);
    cursor = db.cursor()
    cursor.execute('''SELECT max(cfm_experiment_id) FROM cfm_experiment''');
    experimentID = 0;
    for row in cursor:
        experimentID = row[0] + 1;
    try:
        #insert in to database
        with db:
            db.execute('''INSERT INTO cfm_experiment(cfm_experiment_id, title, details)VALUES(?,?,?)'''
                , (experimentID, fileName, description);
    except sqlite3.IntegrityError:
        print('Record already exists')
    db.close();
    return experimentID;
"""
This function fills the database table np_spectra with data contained in the spectra list.
"""
def npTableFiller(db,spectra,numOfIdentifiers,maxID):
    #contains the values for the np_spectra db entry.
    idDict = makeMgfIdentifierIndex(spectra,numOfIdentifiers);
    spectraID = maxID +1;
    cfmModel = "param_output0.log - cfm supplied model trained on metabolites.";
    ce = True;
    try:
        with db:
            db.execute('''INSERT INTO np_spectra(spectra_id, structure_id, molmass,cfm_model,ce_mode)VALUES(?,?,?,?,?)'''
                , (spectraID, idDict["ID"], idDict["PEPMASS"], cfmModel,ce));
    except sqlite3.IntegrityError:
        print('Record already exists')
            
def spectraPeakTableFiller(db,spectra,numOfIdentifiers,spectraID):
    peakNum = 0;
    for peak in spectra[numOfIdentifiers:-1]:
        peakID = spectraID + "_" + str(peakNum);
        print(peakID)
        peakNum += 1; 
        splittedPeak = peak.split(" ");
        weight = float(splittedPeak[0]);
        intensity = float(splittedPeak[1]);
        try:
            with db:
                db.execute('''INSERT INTO spectra_peaks(peak_id, spectra_id, weight, intensity)VALUES(?,?,?,?)'''
                    , (peakID,spectraID,weight,intensity));
        except sqlite3.IntegrityError:
            print('Record already exists')

def spectraTableFiller(spectraList,databasePath,experimentID):
    db = sqlite3.connect(databasePath);
   
    #gets the number of identifiers in the spectra. if the line of a spectra starts with a capitol letter the count goes up
    for spectra in spectraList:
        numOfIdentifiers = len([line for line in spectra if line[0].isalpha()]) - 1;
        #add spectra to np_spectra table
        npTableFiller(db,spectra,numOfIdentifiers,experimentID);
        #add peaks of spectra to spectra_peaks table
        spectraPeakTableFiller(db,spectra,numOfIdentifiers,spectraID);
        maxID += 1;    
        
    db.close();


def main(spectraPath,dataDescription,databasePath):
    fileName = spectraPath.split("/")[-1].split(".")[0]
    spectraList = makeSpectraList(spectraPath);
    spectraTableFiller(spectraList,databasePath);
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2]);
