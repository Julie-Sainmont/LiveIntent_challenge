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


df_input, identifier_info = fetch_data()

# ---- general quantities of licence:
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

# checks:
# identifier is unique in the identifier_info table

## --- idea:

#! look at the otherlap of licences!
# "a license for a given identifier can potentially be obtained from multiple partners #
# use venn diagram # https://towardsdatascience.com/visualizing-intersections-and-overlaps-with-python-a6af49c597d9

# we could say that Netwise is too small compare to the other so we dont look into it

# look at the ratio of conversions/opens or clicks?
# Look at the distribution of identifier's opens, clicks, conversion for each license

# venn
from venn import venn

df_input["leads"] = df_input[["opens", "clicks", "conversions"]].sum(axis=1)
df = df_input[
    np.logical_and(~pd.isnull(df_input["license"]), df_input["leads"] > 0)
].copy()


sets = {labels[0]: set(d1), labels[1]: set(d2), labels[2]: set(d3), labels[3]: set(d4)}
fig, ax = plt.subplots(1, figsize=(16, 12))
venn(sets, ax=ax)
plt.legend(labels[:-2], ncol=6)
