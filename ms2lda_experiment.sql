drop table if exists ms2lda_experiment; 

create table ms2lda_experiment
(	ms2lda_experiment_id	integer			not null, 
	title			varchar			not null,
	details			text			not null,
	primary key(ms2lda_experiment_id)
);
