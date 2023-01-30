create table users (
	userid int primary key,
	name text not null
);
create table movies (
	movieid integer primary key,
	title text not null
);
create table genres (
	genreid integer primary key,
	name text not null
);
create table taginfo (
	tagid int primary key, 
	content text not null
);
create table hasagenre (
	movieid integer,
	genreid integer,
	primary key (movieid,genreid),
	foreign key (movieid) references movies on delete cascade,
	foreign key (genreid) references genres on delete cascade
);
create table ratings (
	userid int,
	movieid integer,
	rating numeric constraint check_ratings check (rating>=0 and rating<=5),
	timestamp bigint,
	primary key (userid,movieid),
	foreign key (userid) references users on delete cascade,
	foreign key (movieid) references movies on delete cascade
	
);
create table tags (
	userid integer, 
	movieid integer, 
	tagid int,
	timestamp bigint,
	primary key (userid,movieid,tagid),
	foreign key (userid) references users on delete cascade,
	foreign key (movieid) references movies on delete cascade,
	foreign key (tagid) references taginfo on delete cascade
);
