
CREATE TABLE query1 AS SELECT g.name,COUNT(c.genreid) as moviecount FROM genres g,hasagenre c WHERE g.genreid=c.genreid GROUP BY g.genreid;

CREATE TABLE query2 AS SELECT g.name,AVG(r.rating) as rating FROM genres g,ratings r WHERE EXISTS (SELECT c.genreid,c.movieid FROM hasagenre c WHERE c.movieid = r.movieid AND c.genreid = g.genreid) GROUP BY g.name;

CREATE TABLE temp1 AS SELECT m.title,COUNT(c.rating) AS CountOfRatings FROM movies m,(SELECT movieid,rating FROM ratings) AS c WHERE c.movieid = m.movieid GROUP BY m.title;
CREATE TABLE query3 AS SELECT title,CountOfRatings FROM temp1 WHERE CountOfRatings>=10;

CREATE TABLE query4 AS SELECT m.movieid,m.title FROM movies m WHERE m.movieid IN (SELECT h.movieid FROM hasagenre h WHERE h.genreid IN (SELECT g.genreid FROM genres g WHERE g.name='Comedy')) GROUP BY m.movieid;

CREATE TABLE query5 AS SELECT m.title,AVG(c.rating) as average FROM movies m,(SELECT movieid,rating FROM ratings) AS c WHERE c.movieid = m.movieid GROUP BY m.title; 

CREATE TABLE query6 AS SELECT AVG(r.rating) AS average FROM ratings r WHERE r.movieid IN (SELECT h.movieid FROM hasagenre h WHERE h.genreid IN (SELECT g.genreid FROM genres g WHERE g.name='Comedy')); 

CREATE TABLE query7 AS SELECT AVG(r.rating) AS average FROM ratings r WHERE r.movieid IN ((SELECT h.movieid FROM hasagenre h WHERE h.genreid IN (SELECT g.genreid FROM genres g WHERE g.name='Comedy')) INTERSECT (SELECT h.movieid FROM hasagenre h WHERE h.genreid IN (SELECT g.genreid FROM genres g WHERE g.name='Romance')));

CREATE TABLE query8 AS SELECT AVG(r.rating) AS average FROM ratings r WHERE r.movieid IN (SELECT h.movieid FROM hasagenre h WHERE h.genreid IN (SELECT g.genreid FROM genres g WHERE g.name='Romance') EXCEPT SELECT h.movieid FROM hasagenre h WHERE h.genreid IN (SELECT g.genreid FROM genres g WHERE g.name='Comedy'));

CREATE TABLE query9 AS SELECT movieid, rating from ratings WHERE userid=:v1;

CREATE TABLE similarity as (
with avgcalc as (select movieid, avg(rating) as average
	from ratings
	group by movieid)
	select a.movieid as m1, b.movieid as m2, ( 1 - ( ABS ( a.average - b.average))/5) as s, c.rating, d.title
		from avgcalc as a, avgcalc as b ,query9 as c,movies as d
		where a.movieid not in(select movieid from query9) --select all movies not rated
		and b.movieid in (select movieid from query9) --select all movies rated
		and b.movieid = c.movieid 
		and a.movieid = d.movieid);

CREATE TABLE recommendation as (
select title
	from similarity 
	group by title, m1
	having (SUM(s * rating) /SUM(s)) > 3.9);