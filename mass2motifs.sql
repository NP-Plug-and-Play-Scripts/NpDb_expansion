drop table if exists mass2motifs; 

create table mass2motifs
(	motif_id		varchar			not null,
	motifName		varchar			not null,
	ms2lda_experiment_id		integer			not null,
	degree			int			not null,
	annotation		text			not null,
	primary key(motif_id),
	foreign key (ms2lda_experiment_id) references ms2lda_experiment(ms2lda_experiment_id)
);
