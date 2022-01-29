# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 22:15:33 2022

@author: julie
"""
import pandas as pd
import numpy as np
from venn import venn
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles
from matplotlib_venn import venn2, venn2_circles

import seaborn as sns

sns.set(font_scale=1.4)  # for label size
from parameters import export_folder, save_graphs


def plot_identifiers_per_license(df_input):
    # ---- general quantities of identifiers per license:
    license_size = df_input.groupby("license").sum()
    axes = license_size.plot.bar(rot=45, subplots=True, figsize=(10, 18))
    # axes[1].legend(loc=2)
    axes[1].set_ylabel("Number of identifiers per license", fontsize=15)
    if save_graphs:
        plt.savefig(export_folder + "volume_per_license.png")
    else:
        plt.show()
    return


# Distribution of the number of licences covering each identifier
def plot_n_licences_per_identifier(df_id_count_license):
    df_distribution_coverage = df_id_count_license.groupby(
        "license_count", as_index=False
    ).count()
    df_distribution_coverage["percent"] = (
        100
        * df_distribution_coverage["identifier"]
        / df_distribution_coverage["identifier"].sum()
    )
    df_distribution_coverage["percent"].plot.bar(rot=0)
    plt.title("Distribution of the number of licences covering each identifier")
    if save_graphs:
        plt.savefig(export_folder + "Distribution_identifier_license.png")
    else:
        plt.show()
    return


def built_venn_sets(df_input, list_licenses):
    df = (
        df_input[
            np.logical_and(
                ~pd.isnull(df_input["license"]),
                df_input[["opens", "clicks", "conversions"]].sum(axis=1) > 0,
            )
        ]
        .copy()
        .reset_index()
    )

    sets = {}
    for lic in list_licenses:
        set_df = df[
            df["license"] == lic
        ].identifier.to_list()  # replace index with identifier ?
        sets[lic] = set(set_df)
    return sets


def plot_overlapping_sets(sets, sub_filename=""):
    # -- look at them all together
    # ----------------------------
    fig, ax = plt.subplots(1, figsize=(16, 12))
    venn(sets, ax=ax)
    # make the legend in one line
    plt.legend(list(sets.keys()), ncol=len(sets.keys()))
    if save_graphs:
        plt.savefig(export_folder + "Large_venn_diagram" + sub_filename + ".png")
    else:
        plt.show()
    return


def plot_venn_matrix(sets, list_licenses, n_license):
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
        plt.subplot(n_license, n_license, txt_idx)
        plt.text(
            0.5, 0.5, list_licenses[idx + 1], ha="center", va="center", color="#1F764B"
        )
        plt.axis("off")
    # plot top plots (the ones with a title) - i.e on vertical line
    for idx, title_idx in enumerate(title_indexes):
        print(idx, title_idx)
        plt.subplot(6, 6, title_idx)
        venn2(title_sets[idx], set_colors=c, set_labels=(" ", " "))
        plt.title(list_licenses[idx], fontsize=10, color="#1F4576")
    # plot the rest of the diagrams
    for idx, plot_idx in enumerate(plot_indexes):
        plt.subplot(6, 6, plot_idx)
        venn2(plot_sets[idx], set_colors=c, set_labels=(" ", " "))
    if save_graphs:
        plt.savefig(export_folder + "venn_matrix.png")
    else:
        plt.show()
    return


# ---- overlapping matrix
def plot_cross_matrix(df, sub_filename=""):

    plt.figure(figsize=(12, 10), dpi=200)
    ax = sns.heatmap(df, annot=True, annot_kws={"size": 18})  # font size
    # ax = sns.heatmap(
    #     df, xticklabels=df.columns, yticklabels=df.columns, center=0, annot=True,
    # )

    plt.yticks(fontsize=12)
    locs, labels = plt.xticks(fontsize=12)
    plt.setp(labels, rotation=45)
    plt.xlabel("")
    plt.ylabel("")
    if save_graphs:
        plt.savefig(export_folder + "heatmap" + sub_filename + ".png")
    else:
        plt.show()
    return


def plot_venn3(sets, list_suggestion):
    suggested_set = {key: sets[key] for key in list_suggestion}
    venn3(
        list(suggested_set.values()),
        set_colors=("#3E64AF", "#3EAF5D", "#D74E3B"),
        set_labels=list(suggested_set.keys()),
        alpha=0.75,
    )
    # venn3_circles(list(suggested_set.values()), lw=0.7)
    return
