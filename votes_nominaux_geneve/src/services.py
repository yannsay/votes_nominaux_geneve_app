import pandas as pd

def filter_rsge_voting(voting_table: pd.DataFrame,
                       selected_rubriques: list[str],
                       selected_chapitre: list[str],
                       last_debate: bool = True) -> pd.DataFrame:
    """
    Function to filter the voting table
    """
    filtered_df = voting_table.copy()

    if selected_rubriques != []:
        filtered_df = filtered_df[filtered_df["intitule_rubrique"].isin(
            selected_rubriques)]
    if selected_chapitre != []:
        filtered_df = filtered_df[filtered_df["intitule_chapitre"].isin(
            selected_chapitre)]
        
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

def filter_votes(votes_table: pd.DataFrame,
                 persons_table: pd.DataFrame,
                 selected_persons: list[str],
                 selected_parties: list[str],
                 selected_genre: list[str]) -> pd.DataFrame:
    """
    Filter the individual votes table based on the deputees.
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

    return votes_table[votes_table["vote_person_external_id"].isin(filtered_df["person_external_id"])]


def create_table_to_plot(voting_table: pd.DataFrame,
                         votes_table: pd.DataFrame,
                         column_for_title: str = "voting_title_fr"  # "voting_external_id"
                         ) -> pd.DataFrame:
    """
    Function to merge and pivot voting and vote tables.
    """
    full_table = voting_table.merge(votes_table,
                                    left_on="voting_external_id",
                                    right_on="vote_voting_external_id")
    short_test = full_table.sort_values(by="voting_date").loc[:, [
        column_for_title, "vote_person_fullname", "vote_label"]]
    table_to_plot = short_test.pivot(columns=column_for_title,
                                     index="vote_person_fullname",
                                     values="vote_label")
    table_to_plot = table_to_plot.reset_index()
    table_to_plot = table_to_plot.rename(
        columns={'vote_person_fullname': 'Député.e'})

    return table_to_plot

