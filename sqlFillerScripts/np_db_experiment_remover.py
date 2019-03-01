#!/usr/bin/env python
import sqlite3;
import sys; 

def ms2ldaExperimentRemove(databasePath, experimentID):
    db = sqlite3.connect(databasePath);
    cursor = db.cursor()
    cursor.execute("Delete from motif_details where detail_id in (select a.detail_id from motif_details a join mass2motifs b on a.motif_id == b.motif_id where b.ms2lda_experiment_id = ? );", (experimentID,));
    cursor.execute("Delete from mass2motifs where ms2lda_experiment_id = ? ;",(experimentID,));
    cursor.execute("Delete from ms2lda_experiment where ms2lda_experiment_id = ? ;",(experimentID,));
    db.commit();
    db.close();
    
def main(databasePath, cfmOrMs2lda, experimentID):
    if cfmOrMs2lda.lower() == "cfm":
        pass
    elif cfmOrMs2lda.lower() == "ms2lda":
        ms2ldaExperimentRemove(databasePath,experimentID);
    else:
        print("Not a valid input please enter either ms2lda or cfm!")
        
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2], sys.argv[3]);
