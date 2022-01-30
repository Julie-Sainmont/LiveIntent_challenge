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

Notes:
Use Venn diagram to look at overlap:
    # https://towardsdatascience.com/visualizing-intersections-and-overlaps-with-python-a6af49c597d9

@author: julie
"""
# import pandas as pd

from read_db import fetch_data
from visuals import (
    barplot_per_license,
    plot_n_licences_per_identifier,
    plot_overlapping_sets,
    plot_venn_matrix,
    plot_cross_matrix,
    plot_venn3,
    hist_activity_per_licence,
)
from supportive_functions import (
    # percent_coverage_identifiers,
    # print_coverage_identifiers,
    get_volume_license,
    get_coverage_per_license,
    build_overlapping_set_matrix,
    build_coverage_sumary,
)


# ---- Get the data from the database
# ----------------------------------
df_input = fetch_data(print_db_header=False)
# list of licenses
list_licenses = list(df_input.license.dropna().unique())
n_license = len(list_licenses)
activity_list = ["opens", "clicks", "conversions"]

# ---- Number of licenses covering each license:
# -----------------------------------------------
(_, df_dist_coverage) = get_coverage_per_license(df_input)
# Distribution (bar plot) of the number of licences covering each identifier
plot_n_licences_per_identifier(df_dist_coverage)


# ---- general quantities of identifiers per license:
# --------------------------------------------------
license_size, license_performance = get_volume_license(df_input)
# visulas:
barplot_per_license(license_size, ylabel="Volume", sub_filename="volume")
barplot_per_license(
    license_performance.drop("identifier", axis=1),
    ylabel="Volume of activity per identifier",
    sub_filename="volume_per_identifier",
)

# Distribution of identifier's opens, clicks, conversion for each license
# -----------------------------------------------------------------------
hist_activity_per_licence(df_input, activity_list, list_licenses, n_license)

# --- Overlap of the licenses
# ---------------------------
(sets, cross_percent_df, added_percent_df) = build_overlapping_set_matrix(
    df_input, list_licenses, only_active_identifier=True
)
plot_overlapping_sets(sets)
plot_venn_matrix(sets, list_licenses, n_license)
plot_cross_matrix(cross_percent_df, sub_filename="percent_overlap", show_percent=True)
plot_cross_matrix(added_percent_df, sub_filename="percent_added", show_percent=True)


# Some suggestions should be supported by venn3 diagram to show the final overlap
# -------------------------------------------------------------------------------
# Compare against both the full dataset, and only the active identifiers
# - get a dataframe with information for different suggestions:
dict_ref = {
    "All Id": df_input,
    "Active Id": df_input[df_input[activity_list].sum(axis=1) > 0],
}
suggestion_lists = [
    ["LiveRamp"],
    ["Audience Accuity"],
    ["Audience Accuity", "TowerData"],
    ["Audience Accuity", "TowerData", "Netwise"],
    ["Audience Accuity", "FullContact"],
    ["Audience Accuity", "FullContact", "Netwise"],
    ["Audience Accuity", "FullContact", "TowerData"],
    ["Audience Accuity", "FullContact", "TowerData", "Netwise"],
    ["Audience Accuity", "LiveRamp", "Netwise"],
]
# prepare the dataframe
coverage_columns = ["Coverage vs " + key for key in dict_ref.keys()]

df_coverage = build_coverage_sumary(
    dict_ref, suggestion_lists, coverage_columns, activity_list
)
plot_cross_matrix(
    df_coverage[coverage_columns], sub_filename="percent_coverage", show_percent=True,
)
plot_cross_matrix(
    df_coverage[["Volume clicks"]], sub_filename="volume_clicks", show_percent=False,
)


for sugg in suggestion_lists:
    if len(sugg) == 3:
        plot_venn3(
            sets, list_suggestion=sugg, add_circle=False, sub_filename="_".join(sugg),
        )
    elif len(sugg) > 3:
        sets2 = {keys: sets[keys] for keys in sugg}
        plot_overlapping_sets(sets2, sub_filename="_".join(sets.keys()))
