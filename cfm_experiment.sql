drop table if exists cfm_experiment; 

create table cfm_experiment
(	cfm_experiment_id	integer			not null, 
	title			varchar			not null,
	details			text			null,
	primary key(cfm_experiment_id)
);
