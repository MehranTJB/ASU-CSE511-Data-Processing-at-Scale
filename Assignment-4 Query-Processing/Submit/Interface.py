#!/usr/bin/python3
#
# Interface for the assignement
DATABASE_NAME = 'dds_assignment'

# TODO: Change these as per your code
RATINGS_TABLE = 'ratings'
RANGE_TABLE_PREFIX = 'rangeratingspart'
RROBIN_TABLE_PREFIX = 'roundrobinratingspart'
RATING_COLNAME = 'rating'

import psycopg2
import os
import io
 

def getOpenConnection(user='postgres', password='1234', dbname='postgres'):
    return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")


def RangeQuery(ratingsTableName, ratingMinValue, ratingMaxValue, openconnection):
	ratingMinValue,ratingMaxValue = float(ratingMinValue), float(ratingMaxValue)
	if ratingMinValue >=0 and ratingMaxValue <=5:
		pass
	else:
		return 'Rating out of range use only ratings in range [0,5]'

	with openconnection.cursor() as cur:
		subtable_ratings_finder(RANGE_TABLE_PREFIX, 'RangeQueryOut.txt', cur, ratingMinValue,ratingMaxValue, mode='w' )
		subtable_ratings_finder(RROBIN_TABLE_PREFIX, 'RangeQueryOut.txt', cur, ratingMinValue,ratingMaxValue,mode='a' )

	print('finished running the function RangeQuery')

	return
		

def PointQuery(ratingsTableName, ratingValue, openconnection):
	with openconnection.cursor() as cur:
		exact_rating_finder(RANGE_TABLE_PREFIX, 'PointQueryOut.txt', cur, ratingValue, mode='w' )
		exact_rating_finder(RROBIN_TABLE_PREFIX, 'PointQueryOut.txt', cur, ratingValue, mode='a' )
		print('finished running the function PointQuery')
	return


def subtable_ratings_finder(table_prefix, filename, cur, ratingMinValue, ratingMaxValue, mode='w' ):


	with open(filename, mode) as fout:

		num_range_tables=find_num_partitions(table_prefix,cur)
		table_num=0

		for i in range(num_range_tables):

			table_name=table_prefix+str(table_num)
			query='''
						SELECT*
						FROM {0}
						WHERE rating>={1} AND rating<={2}
					'''.format(table_name,ratingMinValue,ratingMaxValue)

			cur.execute(query)
			table_num+=1

			n=cur.fetchall()

			for row in n:
				row=[str(i) for i in row]
				row.insert(0, table_name)
				fout.write(",".join(row) +'\n')
	print('added rating tuples from '+ table_prefix)
	return 

def exact_rating_finder(table_prefix, filename, cur, ratingValue, mode='w' ):
	ratingValue=float(ratingValue)

	with open(filename, mode) as fout:

		num_range_tables=find_num_partitions(table_prefix,cur)
		table_num=0

		for i in range(num_range_tables):

			table_name=table_prefix+str(table_num)
			query='''
						SELECT*
						FROM {0}
						WHERE rating={1}
					'''.format(table_name,ratingValue)

			cur.execute(query)
			table_num+=1

			n=cur.fetchall()

			for row in n:
				row=[str(i) for i in row]
				row.insert(0, table_name)
				fout.write(",".join(row) +'\n')
	print('added rating={0} tuples from {1}'.format(ratingValue, table_prefix))
	return 



def find_num_partitions(table_prefix, cur):
	query ="""
		SELECT COUNT(TABLE_NAME)
		FROM INFORMATION_SCHEMA.tables 
		WHERE TABLE_NAME LIKE '{0}%' """.format(table_prefix)
	cur.execute(query)

	return cur.fetchone()[0]