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

from matplotlib_venn import venn3, venn3_circles
from matplotlib_venn import venn2, venn2_circles
from read_db import fetch_data

# venn
from venn import venn

df_input, identifier_info = fetch_data()

# list of licenses
list_licenses = list(df_input.license.dropna().unique())
n_license = len(list_licenses)
# checked:
# identifier is unique in the identifier_info table


# ----- Visuals:

# ---- general quantities of identifiers per license:
df_provider = df_input.groupby("license").sum()

axes = df_provider.plot.bar(rot=45, subplots=True, figsize=(10, 18))
# axes[1].legend(loc=2)


# ---- How many license each identifier can be optained from
df_id_count_license = (
    df_input.groupby("identifier")
    .agg(**{"license_count": ("license", "count")})
    .reset_index()
)


# df_id_count_license.hist(
#     bins=df_id_count_license["license_count"].max(),
#     weights=np.ones_like(df_id_count_license[df_id_count_license.columns[1]])
#     * 100.0
#     / len(df_id_count_license),
# )
# # OR
df_distribution_coverage = (
    df_id_count_license.groupby("license_count").count().reset_index()
)
df_distribution_coverage["percent"] = (
    100
    * df_distribution_coverage["identifier"]
    / df_distribution_coverage["identifier"].sum()
)
df_distribution_coverage["percent"].plot.bar(rot=0)
plt.title("distribution of the number of licences covering each identifier")


# # --- idea:

#! look at the otherlap of licences!
# "a license for a given identifier can potentially be obtained from multiple partners #
# use venn diagram # https://towardsdatascience.com/visualizing-intersections-and-overlaps-with-python-a6af49c597d9

# we could say that Netwise is too small compare to the other so we dont look into it

# look at the ratio of conversions/opens or clicks?
# Look at the distribution of identifier's opens, clicks, conversion for each license

# ---------------------------------- #
# --- Overlap of the licenses  ----- #
# ---------------------------------- #
# make a df with identifier only linked to license, and which lead to opens, clicks or conversions
df = df_input[
    np.logical_and(
        ~pd.isnull(df_input["license"]),
        df_input[["opens", "clicks", "conversions"]].sum(axis=1) > 0,
    )
].copy()


sets = {}
for lic in list_licenses:
    set_df = df[
        df["license"] == lic
    ].identifier.to_list()  # replace index with identifier ?
    sets[lic] = set(set_df)
# -- look at them all together
# ----------------------------
fig, ax = plt.subplots(1, figsize=(16, 12))
venn(sets, ax=ax)
# make the legend in one line
plt.legend(list(sets.keys()), ncol=len(sets.keys()))


# -- subplots:
# ---------------------------------- #
# subplot indexes
txt_indexes = [i for i in range(1, 6 * (n_license - 1), 6)]
title_indexes = [i for i in range(2, 7 * (n_license - 1), 7)]
plot_indexes = [8, 14, 20, 26, 15, 21, 27, 22, 28, 29]
c = ("#3E64AF", "#3EAF5D")
# combinations of sets
title_sets = [
    [set(sets[list_licenses[i_lic]]), set(sets[list_licenses[i_lic + 1]])]
    for i_lic in range(0, n_license - 1)
]
plot_sets = [
    [set(sets[list_licenses[i_lic]]), set(sets[list_licenses[i2_lic]])]
    for i_lic in range(0, n_license - 2)
    for i2_lic in range(i_lic + 2, n_license)
]

fig_size = 16
fig, ax = plt.subplots(1, figsize=(fig_size, fig_size))  # figsize= (16, 16)
# plot vertical license name
for idx, txt_idx in enumerate(txt_indexes):
    print(idx, txt_idx)
    plt.subplot(n_license, n_license, txt_idx)
    plt.text(
        0.5, 0.5, list_licenses[idx + 1], ha="center", va="center", color="#1F764B"
    )
    plt.axis("off")
# plot top plots (the ones with a title) - i.e on vertical line
for idx, title_idx in enumerate(title_indexes):
    print(idx, title_idx)
    plt.subplot(6, 6, title_idx)
    vd = venn2(title_sets[idx], set_colors=c, set_labels=(" ", " "))
    plt.title(list_licenses[idx], fontsize=10, color="#1F4576")
    # Move the numbers in the circles
    # vd.get_label_by_id("100").set_x(-0.2)
# plot the rest of the diagrams
for idx, plot_idx in enumerate(plot_indexes):
    plt.subplot(6, 6, plot_idx)
    venn2(plot_sets[idx], set_colors=c, set_labels=(" ", " "))
# plt.show()


plt.savefig("venn_matrix.png")


# -- create a venn grpah with some combination to investigate further..
# Netwise is small but doesnt seem to have a lot of overlap with the other licenses
# -- could we get the number behind the overlap ? otherwise should compute to get them with group by
# could make a table groupby by identifiers and list of licenses attached to them
