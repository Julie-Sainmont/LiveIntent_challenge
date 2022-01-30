# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 21:18:26 2022

@author: julie

Info:
-----
CREATE TABLE "identifier_info" (
    "identifier"	TEXT,
    "opens"	INTEGER,
    "clicks"	INTEGER,
    "conversions"	INTEGER
)

-- contains a set of identifiers and for each identifier the number of opens, clicks and conversions recorded

and

CREATE TABLE "license_info" (
    "identifier"	TEXT,
    "license"	TEXT
)

-- contains which partner(s) can provide licenses for a given identifier
-- each row means that the partner can provide a license for the given identifier
-- can be joined using the "identifier column"
-- the partners can be mapped from the license column in the following way
-- AudienceAcuityMain -> Audience Accuity
-- AudienceAcuityPair -> Audience Accuity
-- LiveRampPelFile -> LiveRamp
-- TowerData -> TowerData
-- a license for a given identifier can potentially be obtained from multiple partners

The two tables can be joined using the "identifier column"


"""
import numpy as np
import pandas as pd
import sqlite3
from parameters import db_filename, dict_provider_name


def explore_db(conn_sql):
    # creating cursor
    cursor = conn_sql.cursor()

    # reading all table names
    table_list = [
        cur
        for cur in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    ]
    tablename_list = [tab[0] for tab in table_list]
    # here is you table list
    print("list of table in the db file: ", tablename_list)
    for tablename in tablename_list:
        print(
            tablename,
            pd.read_sql_query(f"SELECT * FROM {tablename} LIMIT 10", conn_sql),
            "\n",
        )
    return


def fetch_data(print_db_header=False):
    # Create a SQL connection to our SQLite database
    try:
        conn_sql = sqlite3.connect(db_filename)
    except Exception as e:
        print(e)
    if print_db_header:
        explore_db(conn_sql)
    # we make an inner join as we are not interested in the identifier not connected to a license (cannot be used)
    sql = """
    SELECT COALESCE(pd.license, '_') as license, ii.identifier, ii.opens, ii.clicks, ii.conversions
    FROM identifier_info ii
      LEFT JOIN license_info pd
        ON ii.identifier = pd.identifier
    """
    df = pd.read_sql_query(sql, conn_sql)  # Check if we need another type of Join!

    df = df.replace({"license": dict_provider_name})
    print("df", len(df))
    df_out = df.groupby(["license", "identifier"], as_index=False).sum()
    df_out = df_out.replace("_", np.nan)
    print("df_out", len(df_out))
    # Close the connection to the DB
    conn_sql.close()
    return df_out
