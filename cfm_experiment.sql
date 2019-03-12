drop table if exists cfm_experiment; 

create table cfm_experiment
(	cfm_experiment_id	integer			not null, 
	title			varchar			not null,
	cfm_model	varchar			not null,
	ce_mode			boolean			not null,
	description			text			null,
	primary key(cfm_experiment_id)
);
