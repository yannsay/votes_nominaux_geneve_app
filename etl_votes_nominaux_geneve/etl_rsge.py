import pandas as pd
import re

def extract_last_parentheses(text):
    """
    Return the content in the last parenthesis of a text
    """
    matches = re.findall(r'\(([^)]+)\)', text)
    return matches[-1] if matches else text

def clean_rsge(rsge_file: str) -> pd.DataFrame:
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

if __name__ == '__main__':
    from sqlalchemy import create_engine

    clean_rsge = clean_rsge("etl_votes_nominaux_geneve/inputs/rsGE.csv")

    engine = create_engine('sqlite:///db.sqlite3')

    clean_rsge.to_sql("RSGEChapter", if_exists='replace', con=engine)