import pandas as pd

def create_clean_votes_data(votes_file: str) -> pd.DataFrame:
    """
    Cleaner for the votes table
    """
    votes_raw = pd.read_csv(votes_file)

    # Translates votes
    vote_dict = pd.DataFrame({"vote_vote": ["yes", "no", "abstention"],
                            "vote_label": ["Oui", "Non", "Abstention"]})
    clean_votes = votes_raw.merge(vote_dict, how="left", on="vote_vote")

    clean_votes = clean_votes.drop(columns=[
                                "vote_body_key", "vote_created_local", "vote_vote_display_de", "vote_vote_display_it", "vote_vote"])

    return clean_votes
            