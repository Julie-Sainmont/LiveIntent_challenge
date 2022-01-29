# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 21:42:46 2022

Purpose:
--------
LiveIntent can acquire a license from a partner to use a set of identifiers to
provide services for other partners. An identifier can only be used in those
services if a license is obtained. Currently LiveIntent has an agreement with
one such provider (LiveRamp) and is considering whether it should replace that
partner with one of two other partners, Audience Accuity and TowerData, or maybe
rely on two or three of them. 

Request:
-------
Please create one or more visualisations that would highlight how the choice of
a new partner would affect available opens, clicks and conversions that could be
used for provding services to other partners. A reasonable assumption is that
the more opens, clicks and conversions that are available for the services the
better the service will perform. Feel free to use all the tools you are comfortable with.
Solution would include both visualisations and the code used to produce them


@author: julie
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from venn import venn
from matplotlib_venn import venn3, venn3_circles
from matplotlib_venn import venn2, venn2_circles
from read_db import fetch_data
from visuals import (
    built_venn_sets,
    plot_identifiers_per_license,
    plot_n_licences_per_identifier,
    plot_overlapping_sets,
    plot_venn_matrix,
    plot_cross_matrix,
    plot_venn3,
)

# Get the data from the database
df_input, identifier_info = fetch_data()

# list of licenses
list_licenses = list(df_input.license.dropna().unique())
n_license = len(list_licenses)


# - bar plot of the number of identifiers per license
plot_identifiers_per_license(df_input)


# ---- How many license each identifier can be optained from
df_id_count_license = (
    df_input[~pd.isnull(df_input["license"])]
    .groupby("identifier")
    .agg(**{"license_count": ("license", "count"), "license": ("license", ", ".join)})
    .reset_index()
)

# Distribution (bar plot) of the number of licences covering each identifier
plot_n_licences_per_identifier(df_id_count_license)


# # --- idea:

#! look at the otherlap of licences!
# "a license for a given identifier can potentially be obtained from multiple partners #
# use venn diagram # https://towardsdatascience.com/visualizing-intersections-and-overlaps-with-python-a6af49c597d9

# look at the ratio of conversions/opens or clicks?
# Look at the distribution of identifier's opens, clicks, conversion for each license

# ---------------------------------- #
# --- Overlap of the licenses  ----- #
# ---------------------------------- #
df = (
    df_input[
        np.logical_and(
            ~pd.isnull(df_input["license"]),
            df_input[["opens", "clicks", "conversions"]].sum(axis=1) > 0,
        )
    ]
    .copy()
    .reset_index(drop=True)
)

# make a df with identifier only linked to license, and which lead to opens, clicks or conversions
sets = built_venn_sets(df, list_licenses)
plot_overlapping_sets(sets)

plot_venn_matrix(sets, list_licenses, n_license)
# correlation matrix
# Find element overlap, remove same tag matches
res = df.merge(df, on="identifier").query("license_x != license_y")
cross_df = pd.crosstab(res.license_x, res.license_y)
license_n_identifier = df.groupby("license")["identifier"].count()
cross_percent_df = 100 * cross_df / license_n_identifier

plot_cross_matrix(cross_percent_df, sub_filename="percent_overlap")

added_percent_df = 100 * (license_n_identifier - cross_df) / license_n_identifier
plot_cross_matrix(added_percent_df, sub_filename="percent_added")

# list_licenses.remove("Netwise").remove("Netwise")
# dic_added_partner = {}
# for i_lic in range(len(list_licenses)):
#     lic = list_licenses[i_lic]
#     for i_lic2 in range(i_lic + 1, len(list_licenses)):
#         lic2 = list_licenses[i_lic2]
#         dic_added_partner[lic + " - " + lic2] = (
#             added_percent_df[lic].loc[lic2] + added_percent_df[lic2].loc[lic]
#         )


list_suggestion = ["Audience Accuity", "TowerData", "Netwise"]
plot_venn3(sets, list_suggestion)


# -- suggestion:
# Netwise is small but little overlap with the other -- take this one
# Kochava is not worth as most are overlap with othe license
# AudienceAccuity has a 84% and 81% overlap with FullContact and LiveRamp
# - but only 22% TowerData


# -- create a venn grpah with some combination to investigate further..
# Netwise is small but doesnt seem to have a lot of overlap with the other licenses
# -- could we get the number behind the overlap ? otherwise should compute to get them with group by
# could make a table groupby by identifiers and list of licenses attached to them

# final suggestion should be supported by a 2 - 3 venn diagram to show the final overlap
