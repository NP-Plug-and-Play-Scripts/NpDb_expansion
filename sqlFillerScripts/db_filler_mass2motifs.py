#!/usr/bin/env python
import sqlite3;
import sys;

"""
This function fills the database table experiment with info from a given path to a csv file
it splits the input lines on "," and then adds the lines to a dictionary first part becoming the Key and second part becoming the value.
Next it inserts the values belonging to the Key "Name" and "Details" to the ms2lda_experiment table.
databasePath = path to the NP database. 
experimentInfoPath = csv containing the info about the ms2lda experiment.
"""
def experimentFiller(databasePath, experimentInfoPath):
    db = sqlite3.connect(databasePath);
    cursor = db.cursor()
    #select the highest experiment_id from ms2lda_experiment
    cursor.execute('''SELECT max(ms2lda_experiment_id) FROM ms2lda_experiment''');
    experimentID = 0;
    #get the value of experiments present and add 1. This is now the new experiment ID
    row = cursor.fetchone();
    if row[0] == None:
        experimentID = 1;
    else: 
        experimentID = row[0] + 1;
        
    experimentInfoDict = {}
    for line in open(experimentInfoPath):
        splittedLine = line.split(",");
        experimentInfoDict[splittedLine[0]] = splittedLine[1].strip();
    try:
        #insert in to database
        with db:
            db.execute('''INSERT INTO ms2lda_experiment(ms2lda_experiment_id, title, details)VALUES(?,?,?)'''
                , (experimentID, experimentInfoDict["Name"],experimentInfoDict["Details"]));
    except sqlite3.IntegrityError:
        print('Experiment already exists')
    db.close();
    return experimentID;
"""
This function fills the database table mass2motifs with info from a given path to a csv file.
It split the lines on "," and then assigns each part to a different column in the database.
databasePath = path to the NP database. 
motifPath = csv containing the info about the mass2motifs.
experimentID = the id of the experiment. used to link back to the ms2lda_experiment table.
"""
def mass2motifsFiller(databasePath,motifsPath, experimentID):
    db = sqlite3.connect(databasePath);
    cursor = db.cursor()
    with open(motifsPath) as f:
        #skip first line.
        next(f)
        for line in f:
            splittedLine = line.split(",");
            #make the motifID the name of the motif + the experimentID.
            motifID = splittedLine[0].replace("\"", "") + "-" + str(experimentID);
            motifName = splittedLine[0].replace("\"", "")
            #amount of times the motif has been seen in this data.
            degree = int(splittedLine[1].replace("\"", ""));
            #annotation of the motif.
            annotation = splittedLine[2];
            try:
                with db:
                    db.execute('''INSERT INTO mass2motifs(motif_id,motifName,ms2lda_experiment_id, degree,annotation)VALUES(?,?,?,?,?)'''
                        , (motifID, motifName, experimentID, degree, annotation));
            except sqlite3.IntegrityError:
                print(' Motif already exists')
    db.close();

"""
This function fills the database table motif_details with info from a given path to a csv file.
It split the lines on "," and then assigns each part to a different column in the database.
databasePath = path to the NP database. 
motifInfoPath = csv containing the info about the motifDetails.
experimentID = the id of the experiment. used to link back to the ms2lda_experiment table.
"""
def motifDetailsFiller(databasePath,motifInfoPath,experimentID):
    db = sqlite3.connect(databasePath);
    cursor = db.cursor()
    #select max detail id so a unique id can be given.
    cursor.execute('''SELECT max(detail_id) FROM motif_details''');
    detailID = 0;
        #get the value of experiments present and add 1. This is now the new experiment ID
    row = cursor.fetchone();
    if row[0] == None:
        detailID = 1;
    else: 
        detailID = int(row[0]) + 1;
    with open(motifInfoPath) as f:
        #skip first line (contains column names)
        next(f)
        for line in f:
            splittedLine = line.split(",");
            #agains combines the motif name with the experimentID. used to link back to the mass2motifs table
            motifID = splittedLine[0].replace("\"", "") + "-" + str(experimentID);
            featureSplitted = splittedLine[1].split("_");
            #replaces are there to remove the " from the string.
            feature = float(featureSplitted[1].replace("\"", ""));
            featureType = featureSplitted[0].replace("\"", "");
            probability = float(splittedLine[4].replace("\"", ""));
            try:
                with db:
                    db.execute('''INSERT INTO motif_details(detail_id, motif_id, feature, feature_type, probability)VALUES(?,?,?,?,?)'''
                        , (detailID, motifID, feature, featureType, probability));
            except sqlite3.IntegrityError:
                print('motif feature already exists')
            detailID += 1;
    db.close();
"""
main function runs all other functions.
experimentInfoPath =  path to the experiment info file
motifsPath = path to the csv file containing the motif data of an experiment on ms2lda.
motifInfoPath = csv containing the info about the motifDetails.
databasePath = path to the NP database. 
"""
def main(experimentInfoPath,motifsPath,motifInfoPath,databasePath):
    experimentID = experimentFiller(databasePath,experimentInfoPath);
    mass2motifsFiller(databasePath,motifsPath,experimentID);
    motifDetailsFiller(databasePath,motifInfoPath,experimentID)
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]);
