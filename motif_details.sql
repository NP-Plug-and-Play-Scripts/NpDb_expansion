drop table if exists motif_details; 

create table motif_details
(	detail_id		integer			not null, 
	motif_id		varchar			not null,
	feature			float			not null,
	feature_type	varchar			not null,
	probability		float			not null,
	magma_structure_annotation		varchar null,
	primary key(detail_id),
	foreign key (motif_id) references mass2motifs(motif_id)
);

