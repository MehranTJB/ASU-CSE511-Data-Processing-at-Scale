## Assignment-1 Create-Movie-Recommendation-Database

In this database, a movie has two attributes: id, title. A possible movie record is as follows: 54796, 2
Days in Paris (2007).
A movie can be categorized into multiple genres. A genre is selected from Action, Adventure,
Animation, Children’s, Comedy, Crime, and so on. A movie may not necessarily have a genre.
A user can give a 5-star scale rating (0-5) to a movie. For instance, User (ID 4) gave 4 stars to the
movie “The GodFather”. A user can only rate a movie once. The database needs to log each rating
operation. The database should not allow any out-of-range movie ratings.
A user can also assign a tag to a movie. A user can tag a movie multiple times. For instance, User (ID
20) assigned a “very cool” tag to the movie “Mission: Impossible – Ghost Protocol”. Two days later, he
added a new tag, “unbelievable”, to the same movie. Each tag is typically a single word or short
phrase. The meaning, value, and purpose of a particular tag are determined by each user. The
database needs to log each tagging operation.