# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 12:36:59 2022

@author: julie
"""
import pandas as pd


def percent_coverage_identifiers(df, list_suggestion):
    percent_coverage = len(
        df[df["license"].isin(list_suggestion)]["identifier"].unique()
    ) / len(df["identifier"].unique())
    return percent_coverage


def print_coverage_identifiers(df, list_suggestion):
    percent_coverage = percent_coverage_identifiers(df, list_suggestion)
    print(
        "Coverage of identifiers with %s: %.1f"
        % (", ".join(list_suggestion), 100 * percent_coverage)
    )
    return


def get_volume_license(df):
    # ---- general quantities of identifiers per license:
    license_size = df.groupby("license").agg(
        {"identifier": "count", "opens": "sum", "clicks": "sum", "conversions": "sum"}
    )
    license_performance = license_size.copy()
    for col in ["opens", "clicks", "conversions"]:
        license_performance[col] = (
            license_performance[col] / license_performance["identifier"]
        )
    return license_size, license_performance


def get_coverage_per_license(df):
    # ---- How many license each identifier can be optained from
    df_id_count_license = (
        df[~pd.isnull(df["license"])]
        .groupby("identifier")
        .agg(
            **{"license_count": ("license", "count"), "license": ("license", ", ".join)}
        )
        .reset_index()
    )
    # add the zero
    df_id_no_licence = df[pd.isnull(df["license"])][["identifier", "license"]]
    df_id_no_licence["license_count"] = 0
    df_id_count_license2 = pd.concat([df_id_count_license, df_id_no_licence])

    df_distribution_coverage = df_id_count_license2.groupby(
        "license_count", as_index=False
    )["identifier"].count()
    df_distribution_coverage["percent"] = (
        100
        * df_distribution_coverage["identifier"]
        / df_distribution_coverage["identifier"].sum()
    )

    return df_id_count_license2, df_distribution_coverage


def build_overlapping_set_matrix(df_input, list_licenses, only_active_identifier=True):
    if only_active_identifier:
        # make a df with identifier only linked to license, and which lead to opens, clicks or conversions
        df = (
            df_input[df_input[["opens", "clicks", "conversions"]].sum(axis=1) > 0]
            .reset_index(drop=True)
            .copy()
        )
    else:
        df = df_input.copy()
    # built venn sets
    sets = {}
    for lic in list_licenses:
        set_df = df[df["license"] == lic].identifier.to_list()
        sets[lic] = set(set_df)
    # ----  correlation matrix
    # Find element overlap, remove same tag matches
    res = df.merge(df, on="identifier").query("license_x != license_y")
    cross_df = pd.crosstab(res.license_x, res.license_y)
    license_n_identifier = df.groupby("license")["identifier"].count()
    # fill the middle with the size of the license
    for lic in license_n_identifier.index:
        cross_df.loc[lic][lic] = license_n_identifier.loc[lic]
    cross_percent_df = cross_df / license_n_identifier
    added_percent_df = (license_n_identifier - cross_df) / license_n_identifier
    return sets, cross_percent_df, added_percent_df


def build_coverage_sumary(dict_ref, suggestion_lists, coverage_columns, activity_list):
    df_coverage = pd.DataFrame(
        columns=coverage_columns + ["Volume " + act for act in activity_list]
    )
    df_all = dict_ref["All Id"]
    for sugg in suggestion_lists:
        df_tmp = df_all[df_all["license"].isin(sugg)].drop_duplicates(
            subset="identifier", keep="first"
        )
        df_coverage.loc[", ".join(sugg)] = [
            percent_coverage_identifiers(df_v, sugg) for df_v in dict_ref.values()
        ] + [df_tmp[act].sum() for act in activity_list]
    return df_coverage
