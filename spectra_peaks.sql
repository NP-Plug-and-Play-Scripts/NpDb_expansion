drop table if exists spectra_peaks; 

create table spectra_peaks
(	peak_id			varchar			not null, 
	spectra_id		integer			not null,
	weight			float			not null,
	intensity		float			not null,
	primary key(peak_id),
	foreign key (spectra_id) references np_spectra(spectra_id)
);

