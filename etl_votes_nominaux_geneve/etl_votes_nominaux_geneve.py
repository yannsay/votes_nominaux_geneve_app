from sqlalchemy import create_engine

from src.etl_rsge import create_clean_rsge_data, add_counts
from src.etl_votings import create_clean_votings_data
from src.etl_votes import create_clean_votes_data
from src.etl_persons import create_clean_persons_data

engine = create_engine('sqlite:///db.sqlite3')

# Clean RSGE
clean_rsge = create_clean_rsge_data("etl_votes_nominaux_geneve/inputs/rsGE.csv")

# Clean votings
clean_votings = create_clean_votings_data( votings_file = "etl_votes_nominaux_geneve/inputs/voting_body.csv",
                                          rsge_data =  clean_rsge)

if clean_votings["clean_rsge_voting"][clean_votings["clean_rsge_voting"].debat_numero == 999].shape[0] != 0:
    print("### missing debate number in data_votings_rsge")

# Write clean RSGE voting
clean_votings["clean_rsge_voting"].to_sql("data_votings_rsge", if_exists="replace", con=engine)

print("""
    #### writing RSGEVotings to database done. table is data_votings_rsge
    """)
print(clean_votings["clean_rsge_voting"].columns)

# Write clean other voting
clean_votings["clean_oth_voting"].to_sql("data_votings_others", if_exists="replace", con=engine)
print("""
    #### writing otherVotings to database done. table is data_votings_others
    """)
print(clean_votings["clean_oth_voting"].columns)

# Adding information on votes to RSGE data
clean_rsge = add_counts(clean_rsge, clean_votings["clean_rsge_voting"])
print(clean_rsge.columns)
clean_rsge.to_sql("data_rsge", if_exists='replace', con=engine)

print("""
    #### writing RSGE to database done. table is data_rsge
    """)
print(clean_rsge.columns)

# Clean votes and write votes
clean_votes = create_clean_votes_data("etl_votes_nominaux_geneve/inputs/votes.csv")
clean_votes.to_sql("data_votes", if_exists="replace", con=engine)
print("""
    #### writing votes to database done. table is data_votes
    """)
print(clean_votes.columns)

# Clean persons and write persons
clean_persons = create_clean_persons_data("etl_votes_nominaux_geneve/inputs/persons.csv", votes_data=clean_votes)
clean_persons.to_sql("data_persons", if_exists="replace", con=engine)
print("""
    #### writing persons to database done. table is data_persons
    """)
print(clean_persons.columns)

