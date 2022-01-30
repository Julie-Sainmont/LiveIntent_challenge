# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 22:15:33 2022

@author: julie
"""

from venn import venn
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib_venn import venn3, venn3_circles
from matplotlib_venn import venn2  # , venn2_circles
import seaborn as sns
from parameters import export_folder, save_graphs

sns.set(font_scale=1.6)  # for label size


def barplot_per_license(df, ylabel="", sub_filename="count"):
    axes = df.plot.bar(
        rot=45,
        subplots=True,
        title=[""] * len(df.columns),
        sharex=True,
        figsize=(10, 16),
    )
    if ylabel != "":
        axes[1].text(-1.2, 0.5, ylabel, va="center", rotation="vertical")
    plt.xlabel("")
    plt.tight_layout()
    if save_graphs:
        plt.savefig(export_folder + sub_filename + "_per_license.png")
    else:
        plt.show()
    plt.clf()
    return


# Distribution of the number of licences covering each identifier
def plot_n_licences_per_identifier(df):
    plt.figure(figsize=(10, 6))
    ax = df["percent"].plot.bar(rot=0)
    ax.set_xlabel("Number of license")
    ax.set_ylabel("Percent of identifier")
    # Format you want the ticks, e.g. '40%'
    xticks = mtick.FormatStrFormatter("%.0f%%")
    ax.yaxis.set_major_formatter(xticks)
    plt.tight_layout()
    if save_graphs:
        plt.savefig(export_folder + "distribution_identifier_license.png")
    else:
        plt.show()
    plt.clf()
    return


def plot_overlapping_sets(sets, sub_filename=""):
    # -- look at them all together
    # ----------------------------
    fig, ax = plt.subplots(1, figsize=(16, 12))
    venn(sets, ax=ax)
    # make the legend in one line
    plt.legend(list(sets.keys()), ncol=len(sets.keys()))
    plt.tight_layout()
    if save_graphs:
        plt.savefig(export_folder + "large_venn_diagram" + sub_filename + ".png")
    else:
        plt.show()
    plt.clf()
    return


def adjust_number_position_venn2(vd, x_buffer=1.0):
    lbl = vd.get_label_by_id("01")
    x, y = lbl.get_position()
    lbl.set_position((x + x_buffer, y))
    lbl = vd.get_label_by_id("10")
    x, y = lbl.get_position()
    lbl.set_position((x - x_buffer, y))
    return vd


def plot_venn_matrix(sets, list_licenses, n_license):
    """
    Buits matrix of venn2 diagram.
    Save or display the graph as per parameters

    Args:
        sets(sets of series):  Sets of identifiers per license
        list_licenses (list of str): The list of license name
    n_license (INT): The number of license considered.

    Returns
        None.
    """
    # subplot indexes
    txt_indexes = [i for i in range(1, 6 * (n_license - 1), 6)]
    title_indexes = [i for i in range(2, 7 * (n_license - 1), 7)]
    plot_indexes = [8, 14, 20, 26, 15, 21, 27, 22, 28, 29]
    c = ("#3E64AF", "#3EAF5D")
    title_fontsize = 20
    x_buffer = 0.13
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
    fig_size = 18
    fig, ax = plt.subplots(1, figsize=(fig_size, fig_size - 2))  # figsize= (16, 16)
    # plot vertical license name
    for idx, txt_idx in enumerate(txt_indexes):
        plt.subplot(n_license, n_license, txt_idx)
        plt.text(
            0.5,
            0.5,
            list_licenses[idx + 1],
            ha="center",
            va="center",
            color="#1F764B",
            fontsize=title_fontsize,
        )
        plt.axis("off")
    # plot top plots (the ones with a title) - i.e on vertical line
    for idx, title_idx in enumerate(title_indexes):
        plt.subplot(6, 6, title_idx)
        vd = venn2(title_sets[idx], set_colors=c, set_labels=(" ", " "))
        vd = adjust_number_position_venn2(vd, x_buffer=x_buffer)
        plt.title(list_licenses[idx], fontsize=title_fontsize, color="#1F4576")
    # plot the rest of the diagrams
    for idx, plot_idx in enumerate(plot_indexes):
        plt.subplot(6, 6, plot_idx)
        vd = venn2(plot_sets[idx], set_colors=c, set_labels=(" ", " "))
        vd = adjust_number_position_venn2(vd, x_buffer=x_buffer)
    plt.tight_layout()
    if save_graphs:
        plt.savefig(export_folder + "venn_matrix.png")
    else:
        plt.show()
    plt.clf()
    return


# ---- overlapping matrix
def plot_cross_matrix(df, sub_filename="", show_percent=False):
    """
    Plot a heatmap from cross matrix of info crossing licenses
    Args:
        df (DataFrame): df containing the cross matrix
        sub_filename (str, optional): Substring to be added to the filename. Defaults to "".

    Returns:
        None.

    """
    plt.figure(figsize=(11, 8))  # , dpi=200
    if show_percent:
        sns.heatmap(
            df,
            annot=True,
            annot_kws={"size": 16},
            fmt=".1%",
            cbar_kws={"format": mtick.FuncFormatter(lambda x, pos: "{:.0%}".format(x))},
        )
    else:
        sns.heatmap(
            df, annot=True, annot_kws={"size": 16}, fmt=".1f",
        )
    plt.yticks(fontsize=16)
    locs, labels = plt.xticks(fontsize=16)
    plt.setp(labels, rotation=45)
    plt.xlabel("")
    plt.ylabel("")
    plt.tight_layout()
    if sub_filename != "":
        sub_filename = "_" + sub_filename
    if save_graphs:
        plt.savefig(export_folder + "heatmap" + sub_filename + ".png")
    else:
        plt.show()
    plt.clf()
    return


def plot_venn3(sets, list_suggestion=[], add_circle=False, sub_filename=""):
    """
    Plot of venn 3 diagram from the 3 suggested licences

    Args:
        sets(sets of series):  Sets of identifiers per license
        list_suggestion (list of str): The list of license that should be plotted

    Returns:
        None.

    """
    if len(list_suggestion) == 0:
        print("list of suggested license is null - the first 3 are reported on")
        list_suggestion = list(sets.keys())[:3]
    elif len(list_suggestion) != 3:
        print("Need list of 3 licences to make the Venn3 graph")
        return
    suggested_set = {key: sets[key] for key in list_suggestion}

    plt.figure(figsize=(10, 10))
    venn3(
        list(suggested_set.values()),
        set_colors=("#3E64AF", "#3EAF5D", "#D74E3B"),
        set_labels=list(suggested_set.keys()),
        alpha=0.75,
    )
    if add_circle:
        venn3_circles(list(suggested_set.values()), lw=0.7)
    plt.tight_layout()
    if save_graphs:
        if sub_filename != "":
            sub_filename = "_" + sub_filename
        plt.savefig(export_folder + "venn3" + sub_filename + ".png")
    else:
        plt.show()
    plt.clf()
    return


def hist_activity_per_licence(df, activity_list, list_licenses, n_license):
    txt_size = 20
    # n_act = len(activity_list)
    # fig, axs = plt.subplots(
    #     n_license, n_act, tight_layout=True,  sharey=True, figsize=(16, 20)
    # )
    # lic_i = -1
    # for lic in list_licenses:
    #     act_i = -1
    #     lic_i += 1
    #     df_lic = df[df["license"] == lic]
    #     for act in activity_list:
    #         act_i += 1
    #         if act == "conversions":
    #             set_log_ax = False
    #         else:
    #             set_log_ax = True
    #         ax = df_lic[act].plot.hist(
    #             logx=set_log_ax, logy=True, bins=50, ax=axs[lic_i, act_i]
    #         )
    #         if act_i == 0:
    #             ax.set_ylabel(lic, fontsize=20)
    #         else:
    #             ax.set_ylabel("")
    #         if lic_i == 0:
    #             ax.set_title(act, fontsize=20)

    # Make 3 fig - 1 per activity:
    for act in activity_list:
        fig, axs = plt.subplots(
            n_license, 1, tight_layout=True, sharey=True, sharex=True, figsize=(7, 20)
        )
        lic_i = -1
        for lic in list_licenses:
            lic_i += 1
            df_lic = df[df["license"] == lic]

            if act == "conversions":
                set_log_ax = False
            else:
                set_log_ax = True
            ax = df_lic[act].plot.hist(
                logx=set_log_ax, logy=True, bins=50, ax=axs[lic_i]
            )
            ax.set_ylabel(lic + "\n frequency", fontsize=txt_size)
            if lic_i == 0:
                ax.set_title(act, fontsize=txt_size)
            elif lic_i == n_license - 1:
                ax.set_xlabel("Number of " + act, fontsize=txt_size)
        if save_graphs:
            plt.savefig(export_folder + "distribution_" + act + "_quantity.png")
        else:
            plt.show()
    return
