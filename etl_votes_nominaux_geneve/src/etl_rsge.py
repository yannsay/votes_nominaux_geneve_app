import pandas as pd
import re

def extract_last_parentheses(text):
    """
    Return the content in the last parenthesis of a text
    """
    matches = re.findall(r'\(([^)]+)\)', text)
    return matches[-1] if matches else text

def concate_2cols(row, col1, col2):
    "return concatenated columns"
    return str(row[col1]) + " - "+ str(row[col2])

def create_clean_rsge_data(rsge_file: str) -> pd.DataFrame:
    """
    Import the Rubriques Systématique Genève rubriques and chapters and clean them.
    """
    rsge = pd.read_csv(rsge_file, sep=";")
    rubriques_mask = rsge["Référence"].str.len() == 1
    rubriques_rsge = rsge.loc[rubriques_mask]
    rubriques_rsge = rubriques_rsge.reset_index().drop(
        columns=["index", "Date d’adoption"])
    rubriques_rsge.columns = ["Rubrique", "Intitulé rubrique"]

    chapitres_mask = (rsge["Référence"].str.len() > 1) & (
        rsge["Référence"].str.len() <= 4)
    chapitres_rsge = rsge.loc[chapitres_mask]
    chapitres_rsge = chapitres_rsge.reset_index().drop(
        columns=["index", "Date d’adoption"])
    chapitres_rsge.columns = ["Chapitre", "Intitulé chapitre"]

    reformatted_rsge = rsge.loc[~(chapitres_mask | rubriques_mask)]
    reformatted_rsge = reformatted_rsge.loc[~pd.isna(
        reformatted_rsge["Référence"])]
    reformatted_rsge = reformatted_rsge.reset_index().drop(
        columns=["index"])
    reformatted_rsge["Rubrique"] = reformatted_rsge['Référence'].str[0]
    reformatted_rsge["Chapitre"] = reformatted_rsge['Référence'].str[:3]
    reformatted_rsge = reformatted_rsge.merge(
        rubriques_rsge, on="Rubrique", how="left").merge(chapitres_rsge, on="Chapitre", how="left")
    
    # create title with code and intitulé
    reformatted_rsge["rubrique_complet"] = reformatted_rsge.apply(concate_2cols, axis = 1, col1 = "Rubrique", col2 = "Intitulé rubrique")
    reformatted_rsge["chapitre_complet"] = reformatted_rsge.apply(concate_2cols, axis = 1, col1 = "Chapitre", col2 = "Intitulé chapitre")
    # look for law acronym
    reformatted_rsge["acronym"] = reformatted_rsge["Intitulé"].apply(extract_last_parentheses)

    column_names_dict = {'Référence':'reference',
                         'Intitulé' :'intitule',
                         'Rubrique':'rubrique', 
                         'Chapitre':'chapitre', 
                         'Intitulé chapitre':'intitule_chapitre',
                         'Intitulé rubrique':'intitule_rubrique',
                         "Date d’adoption":"date_d_adoption"
                         }
    
    reformatted_rsge.rename(columns=column_names_dict, inplace=True)

    if reformatted_rsge["acronym"].duplicated().sum() > 0:
        print("Look for duplications in acronyms")

    return reformatted_rsge

def add_counts(rsge_date:pd.DataFrame, voting_data:pd.DataFrame) -> pd.DataFrame:
    "Adds the count of votings per rubrique and chapter"
    resume_votings_par_rubrique= voting_data.groupby("rubrique_complet").rubrique_complet.value_counts().reset_index()
    resume_votings_par_rubrique = resume_votings_par_rubrique.rename(columns={"count":"rubrique_count"})
    clean_rsge = rsge_date.merge(resume_votings_par_rubrique, "left")

    resume_votings_par_chapitre = voting_data.groupby("chapitre_complet").chapitre_complet.value_counts().reset_index()
    resume_votings_par_chapitre = resume_votings_par_chapitre.rename(columns={"count":"chapitre_count"})
    clean_rsge = clean_rsge.merge(resume_votings_par_chapitre, "left")

    return clean_rsge