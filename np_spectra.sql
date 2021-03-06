drop table if exists np_spectra; 

create table np_spectra
(	spectra_id		varchar			not null,
	cfm_experiment_id	integer		not null,
	structure_id	varchar			not null,
	smiles			varchar			not null,
	molmass			double			not null,
	primary key(spectra_id)
	foreign key(cfm_experiment_id) references cfm_experiment(cfm_experiment_id)
);
