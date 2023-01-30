#!/usr/bin/python2.7
#
# Interface for the assignement
DATABASE_NAME = 'dds_assignment'

# TODO: Change these as per your code
RATINGS_TABLE = 'ratings'
RANGE_TABLE_PREFIX = 'range_part'
RROBIN_TABLE_PREFIX = 'rrobin_part'
USER_ID_COLNAME = 'userid'
MOVIE_ID_COLNAME = 'movieid'
RATING_COLNAME = 'rating'

import psycopg2
import os
import io

def getOpenConnection(user='postgres', password='1234', dbname='postgres'):
    return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")


def loadRatings(ratingstablename, ratingsfilepath, openconnection):

    cursor = openconnection.cursor()

    cursor.execute(
        "CREATE TABLE " + ratingstablename +
        " (rowid serial primary key, UserID INT, temp1 VARCHAR(10)," +
        " MovieID INT , temp2 VARCHAR(10), Rating REAL, temp3 VARCHAR(10), Timestamp BIGINT)")
    inputFile = open(ratingsfilepath, 'r')
    cursor.copy_from(inputFile, ratingstablename, sep=':',
                  columns=('UserID', 'temp1', 'MovieID', 'temp2', 'Rating', 'temp3', 'Timestamp'))
    cursor.execute(
        "ALTER TABLE " + ratingstablename + " DROP COLUMN Timestamp, " +
        " DROP COLUMN temp1, DROP COLUMN temp2, DROP COLUMN temp3")
    
    cursor.close()


def rangePartition(ratingstablename, numberofpartitions, openconnection):
    lower_lim, upper_lim=(0.0,5.0)
    step=upper_lim/numberofpartitions

    with openconnection.cursor() as cur:
        for i in range(numberofpartitions):
            lower_lim=i*step
            upper_lim=lower_lim+step 
            table_name=RANGE_TABLE_PREFIX+str(i)
            
            create_table_query=  ("""
                        CREATE TABLE {0} ({1} int , {2} int , 
                        {3} float(1) CHECK (rating>=0) CHECK (rating<=5) );
                    """).format(table_name,USER_ID_COLNAME,MOVIE_ID_COLNAME,RATING_COLNAME)
            print(table_name+'was created')





            cur.execute(create_table_query)
            if i==0:
                query=("""
                    INSERT INTO {0} ({1},{2},{3}) 
                    SELECT {1},{2},{3}
                    FROM {6}
                    WHERE {3}>= {4} AND {3}<= {5} 
                    """).format(table_name,USER_ID_COLNAME,MOVIE_ID_COLNAME,RATING_COLNAME, str(lower_lim), str(upper_lim),ratingstablename)
                cur.execute(query)
                print(table_name+'split successful')


            else:
                query=("""
                    INSERT INTO {0} ({1},{2},{3}) 
                    SELECT {1},{2},{3}
                    FROM {6}
                    WHERE {3}> {4} AND {3}<= {5} 
                    """).format(table_name,USER_ID_COLNAME,MOVIE_ID_COLNAME,RATING_COLNAME, str(lower_lim), str(upper_lim),ratingstablename)
                
                cur.execute(query)
                print(table_name+'split successful')
        openconnection.commit()

    return




def roundRobinPartition(ratingstablename, numberofpartitions, openconnection):
    with openconnection.cursor() as cur:
        
        # determine how many samples need to bedivided into equal partitions

        cur.execute('SELECT * FROM {0} ;'.format(ratingstablename) )
        data= cur.fetchall()

        def partition(lst,n):
            return [lst[i::n] for i in range(n)]

        partitions=partition(data, numberofpartitions)
        table_num=0
        for partition in partitions:
 

            table_name=RROBIN_TABLE_PREFIX+str(table_num)

            create_table_query="""
                                CREATE TABLE {0} ({1} int , {2} int , {3} float(1) );
                                """.format(table_name,USER_ID_COLNAME,MOVIE_ID_COLNAME,RATING_COLNAME)
            cur.execute(create_table_query)
            print(table_name+' was created')

            table_num+=1

            for row in partition:
                insert_query=''' INSERT INTO {0}
                VALUES({1},{2},{3})
                '''.format(table_name,row[0], row[1], row[2])

                cur.execute(insert_query)

        openconnection.commit()

    return 



def roundrobininsert(ratingstablename, userid, itemid, rating, openconnection):
    with openconnection.cursor() as cur:
        cur.execute('SELECT COUNT(*) FROM {0} ;'.format(ratingstablename) )
        num_rows=cur.fetchone()[0]


        find_num_partitions ="""
                                SELECT COUNT(TABLE_NAME)
                                FROM INFORMATION_SCHEMA.tables 
                                WHERE TABLE_NAME LIKE '{0}%'
                                """.format(RROBIN_TABLE_PREFIX)

        cur.execute(find_num_partitions)
        num_partitions=cur.fetchone()[0]
        idx=num_rows%num_partitions

        query="""
                INSERT INTO {0} 
                VALUES({1},{2},{3})
                """.format(RROBIN_TABLE_PREFIX+str(idx), userid, itemid, rating )

        cur.execute(query)
        print('inserted value into '+RROBIN_TABLE_PREFIX+str(idx))

        insert_main_query='''INSERT INTO {0}
                        VALUES({1},{2},{3})
                    '''.format(ratingstablename,userid, itemid, rating)
        cur.execute(insert_main_query)

        print('inserted into '+ ratingstablename)

        openconnection.commit()


    return






def rangeinsert(ratingstablename, userid, itemid, rating, openconnection):
        
    with openconnection.cursor() as cur:

        find_num_partitions ="""
                                SELECT COUNT(TABLE_NAME)
                                FROM INFORMATION_SCHEMA.tables 
                                WHERE TABLE_NAME LIKE '{0}%'
                                """.format(RANGE_TABLE_PREFIX)

        cur.execute(find_num_partitions)
        num_partitions=cur.fetchone()[0]
        print(num_partitions)

        step=5.0/num_partitions

        idx=int(rating/step)
        if rating % step == 0 and idx != 0:
            idx = idx - 1
        table_name=RANGE_TABLE_PREFIX+ str(idx)

        insert_query="""
                INSERT INTO {0} 
                VALUES({1},{2},{3})
                """.format(table_name, userid, itemid, rating )


        cur.execute(insert_query)
        print('inserted into '+table_name)
        

        insert_main_query='''INSERT INTO {0}
                        VALUES({1},{2},{3})
                    '''.format(ratingstablename,userid, itemid, rating)
        cur.execute(insert_main_query)

        print('inserted into '+ratingstablename)

        openconnection.commit()


    return






    

























