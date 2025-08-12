import pandas as pd
import numpy as np
def filter_rsge_voting(voting_table: pd.DataFrame,
                       selected_rubriques: list[str],
                       selected_chapitre: list[str],
                       last_debate: bool = True) -> pd.DataFrame:
    """
    Function to filter the voting table
    """
    filtered_df = voting_table.copy()
    if selected_rubriques != []:
        filtered_df = filtered_df[filtered_df["rubrique_complet"].isin(
            selected_rubriques)]
        print("ok")
    if selected_chapitre != []:
        filtered_df = filtered_df[filtered_df["chapitre_complet"].isin(
            selected_chapitre)]
        print("ok")

        
    if last_debate:
        max_debates = filtered_df.groupby('voting_affair_number')['debat_numero'].max().reset_index()
        max_debates.columns = ['voting_affair_number', 'max_debat_numero']
        filtered_df = filtered_df.merge(
            max_debates, 
            left_on=['voting_affair_number', 'debat_numero'], 
            right_on=['voting_affair_number', 'max_debat_numero'],
            how='inner'
        )

        # Drop the helper column
        filtered_df = filtered_df.drop('max_debat_numero', axis=1)

    return filtered_df

def filter_persons(persons_table: pd.DataFrame,
                    selected_persons: list[str],
                    selected_parties: list[str],
                    selected_genre: list[str]) -> pd.DataFrame:
        """
        Filter the persons table based on the selectio .
        """
        filtered_df = persons_table.copy()
        if selected_persons != []:
            filtered_df = filtered_df[filtered_df["person_fullname"].isin(
                selected_persons)]
        if selected_parties != []:
            filtered_df = filtered_df[filtered_df["person_party_fr"].isin(
                selected_parties)]
        if selected_genre != []:
            filtered_df = filtered_df[filtered_df["person_gender"].isin(
                selected_genre)]

        return filtered_df


def create_persons_votes(votes_table: pd.DataFrame,
                 persons_table: pd.DataFrame) -> pd.DataFrame:
    """
    Join the votes and persons table
    """
    full_table = persons_table.merge(votes_table,
                                    left_on="person_external_id",
                                    right_on="vote_person_external_id")
    return full_table

def create_person_votes_table(voting_table: pd.DataFrame,
                                persons_votes_table: pd.DataFrame
                        #  column_for_title: str = "voting_title_fr"  # "voting_external_id"
                         ) -> pd.DataFrame:
    """
    Function to merge and pivot voting and vote tables.
    """
    voting_table["title_column"] = voting_table.apply(add_title, axis = 1)

    full_table = voting_table.merge(persons_votes_table,
                                    left_on="voting_external_id",
                                    right_on="vote_voting_external_id")
    short_table = full_table.sort_values(by="voting_date").loc[:, [
        "title_column", "vote_person_fullname", "vote_label", "person_party_fr"]]
    table_to_plot = short_table.pivot(columns=["title_column"],
                                     index=["person_party_fr","vote_person_fullname"],
                                     values="vote_label")
    table_to_plot = table_to_plot.sort_values(by=["person_party_fr","vote_person_fullname"])
    table_to_plot = table_to_plot.reset_index()
    table_to_plot = table_to_plot.rename(
        columns={'vote_person_fullname': 'Député.e',
                 'person_party_fr': "Parti"})

    return table_to_plot

def create_votes_table(registre: str, 
                       chapitre: str,
                       rsge_votings_data: pd.DataFrame,
                       persons_data: pd.DataFrame,
                       votes_data: pd.DataFrame) -> pd.DataFrame: 


    # filter voting
    votings_table = filter_rsge_voting(voting_table=rsge_votings_data, 
                            selected_rubriques=registre, 
                            selected_chapitre=chapitre)
    # filter persons
    persons_table = filter_persons(persons_data, [],[],[])

    # create persons_votes table
    persons_votes_table = create_persons_votes(votes_data, persons_table)

    # Creat table to plot   
    table_to_plot = create_person_votes_table(voting_table=votings_table, 
                                              persons_votes_table=persons_votes_table)
    table_to_plot = table_to_plot.replace(np.nan, "")

    return table_to_plot

def add_title(row):
    """
    Add a title with the acronym of the law, initial affair if exitis, unique voting affair and debate number.
    Voting affair helps to keep the name unique.
    """
    new_name = row["acronym"] + " -- " + (row["initial_affair"] if row["initial_affair"] else "") + " -- " + row["voting_affair_number"] + " -- débat: " + str(row["debat_numero"])
    return new_name

def create_rsge_dict(rsge_data:pd.DataFrame) -> dict[str , str, str, str]:
    "format the rsge data for view"
    rsge_shorter =rsge_data[["rubrique_complet", "chapitre_complet", "rubrique_count", "chapitre_count"]].drop_duplicates()
    rsge_shorter= rsge_shorter.astype({'rubrique_count': 'str', 'chapitre_count':'str'})
    rsge_shorter= rsge_shorter.replace("nan", "Pas de votes dans les données")
    rsge_shorter["rubrique_count"] = rsge_shorter["rubrique_count"].str.replace(".0", "")
    rsge_shorter["chapitre_count"] = rsge_shorter["chapitre_count"].str.replace(".0", "")
    rsge_dict = {}
    for rubrique in rsge_shorter["rubrique_complet"].unique():
        rsge_dict[rubrique]={
            "count":rsge_shorter[rsge_shorter["rubrique_complet"] == rubrique]["rubrique_count"].values[0],
            "chapitre":{}
        }
        for chapitre in rsge_shorter[rsge_shorter["rubrique_complet"] == rubrique]["chapitre_complet"].to_list():
            rsge_dict[rubrique]["chapitre"][chapitre] =rsge_shorter[rsge_shorter["chapitre_complet"] == chapitre]["chapitre_count"].values[0]
    return rsge_dict

