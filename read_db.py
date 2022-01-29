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

import pandas as pd
import sqlite3
from parameters import db_filename, dict_provider_name


def fetch_data():
    # Create a SQL connection to our SQLite database
    try:
        conn_sql = sqlite3.connect(db_filename)
    except Exception as e:
        print(e)
    # # creating cursor
    # cursor = conn_sql.cursor()

    # # reading all table names
    # table_list = [
    #     cur for cur in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    # ]
    # # here is you table list
    # print(table_list)
    identifier_info = pd.read_sql_query("SELECT * FROM identifier_info", conn_sql)

    sql = """
    SELECT pd.license, ii.identifier, ii.opens, ii.clicks, ii.conversions
    FROM identifier_info ii
    LEFT JOIN license_info pd
    on ii.identifier = pd.identifier
    """
    df = pd.read_sql_query(sql, conn_sql)  # Check if we need another type of Join!

    df = df.replace({"license": dict_provider_name})
    print("df", len(df))
    df_out = df.groupby(["license", "identifier"], as_index=False).sum()
    print("df_out", len(df_out))
    # Close the connection to the DB
    conn_sql.close()
    return df_out, identifier_info
