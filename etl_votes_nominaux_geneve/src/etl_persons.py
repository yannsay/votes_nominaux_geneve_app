import pandas as pd

def create_clean_persons_data(persons_file: str, votes_data) -> pd.DataFrame:
    """
    Cleaner for persons data
    """
    persons_raw = pd.read_csv(persons_file)

    columns_to_keep = ["person_external_id", "person_fullname", "person_firstname", "person_lastname",
                        "person_party_fr", "person_website_parliament_url_fr", "person_image_url",
                        "person_birthday", "person_occupation_fr", "person_gender",
                        "person_function_latest_fr"]
    clean_persons = persons_raw[columns_to_keep]

    # Filter the persons that votes are in the period
    clean_persons = clean_persons[clean_persons["person_external_id"].isin(
        votes_data["vote_person_external_id"])]

    return clean_persons