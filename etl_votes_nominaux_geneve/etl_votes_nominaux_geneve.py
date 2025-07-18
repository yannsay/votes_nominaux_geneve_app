from src.etl_rsge import create_clean_rsge_data
from src.etl_votings import create_clean_votings_data
from sqlalchemy import create_engine
engine = create_engine('sqlite:///db.sqlite3')

clean_rsge = create_clean_rsge_data("etl_votes_nominaux_geneve/inputs/rsGE.csv")
clean_rsge.to_sql("RSGEChapter", if_exists='replace', con=engine)
print("""
    #### writing RSGE to database done
    """)
clean_votings = create_clean_votings_data( votings_file = "etl_votes_nominaux_geneve/inputs/voting_body.csv",
                                          rsge_data =  clean_rsge)
clean_votings["clean_rsge_voting"].to_sql("cleanVotings", if_exists="replace", con=engine)
print("""
    #### writing cleanVotings to database done
    """)
clean_votings["clean_oth_voting"].to_sql("otherVotings", if_exists="replace", con=engine)
print("""
    #### writing otherVotings to database done
    """)

