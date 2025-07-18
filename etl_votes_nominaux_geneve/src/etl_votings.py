import pandas as pd
import re

def create_clean_votings_data(votings_file: str, rsge_data: pd.DataFrame) -> pd.DataFrame:
        """
        Cleaner for the voting tables. It will create 2 tables:
        - one with votings with RSGE: clean_rsge_voting
        - one with votings without RSGE: voting_oth_clean
        Clean the voting table and add the information from RSGE
        """
        clean_voting = pd.read_csv(votings_file)

        # Extract Référence from title.  \xa0 is a type of white space
        pattern = r'([A-Z] [0-9] [0-9]{2}|[A-Z]\xa0[0-9]\xa0[0-9]{2})'
        clean_voting['reference'] = clean_voting['voting_affair_title_fr'].str.extract(
            pattern)
        clean_voting['reference'] = clean_voting['reference'].str.replace(
            '\xa0', ' ', regex=False)

        # Add the type of vote
        pattern = r'([A-Z]{1,2})'
        clean_voting['type_vote'] = clean_voting['voting_affair_number'].str.extract(
            pattern)
        vote_dict = pd.DataFrame({"type_vote": ["IN",
                                                "M",
                                                "P",
                                                "PL",
                                                "PO",
                                                "R",
                                                "RD"],
                                  "type_vote_label": ["Initiative populaire cantonale",
                                                      "Proposition de motion",
                                                      "Pétition",
                                                      "Projet de loi",
                                                      "Proposition de postulat",
                                                      "Proposition de résolution",
                                                      "Rapport"]})

        clean_voting = clean_voting.merge(
            vote_dict, how="left", on="type_vote")
        clean_voting = clean_voting.drop(columns="type_vote")

        # Add the numero_debate
        clean_voting['debat_numero'] = clean_voting["voting_title_fr"].apply(get_debate_number)

        # Clean dates for filter in streamlit
        clean_voting["voting_date"] = pd.to_datetime(
            clean_voting["voting_date"])

        # Filter text without a Référence from RSGE
        oth_voting = clean_voting.loc[pd.isna(
            clean_voting['reference']),].reset_index()

        # Filter text with a Référence from RSGE
        clean_voting = clean_voting.loc[~pd.isna(
            clean_voting['reference']),].reset_index()

        # Remove columns that are empty or not used
        column_missing: str = []
        for column in clean_voting.columns:
            if all(pd.isna(clean_voting[column])):
                column_missing.append(column)
        clean_voting = clean_voting.drop(
            columns=column_missing + ["index", "voting_body_key", "voting_updated_local", "voting_created_local"])

        # Add RSGE information to voting
        clean_rsge = rsge_data
        clean_voting = clean_voting.merge(
            clean_rsge, on="reference", how="left")

        # Removing missing titles with oth_voting
        clean_oth_voting = oth_voting.loc[~pd.isna(
            oth_voting['voting_affair_title_fr']),].reset_index()
        
        # Remove columns that are empty or not used
        column_missing: str = []
        for column in clean_oth_voting.columns:
            if all(pd.isna(clean_oth_voting[column])):
                column_missing.append(column)
        clean_oth_voting = clean_oth_voting.drop(
            columns=column_missing + ["level_0", "index", "voting_body_key", "voting_updated_local", "voting_created_local"])


        return {"clean_rsge_voting":clean_voting,
                "clean_oth_voting":clean_oth_voting}



def get_debate_number(title):
    """
    Extract debate number from titles.
    """
    if pd.isna(title):
        return 999
    
    # Convert to lowercase and strip whitespace
    title_clean = str(title).lower().strip()
    
    # Pattern to match ": [1er|2e|3e] débat" at the end of string
    pattern = r'(?::\s*)?(1er|2e|3e)\s+débat\s*'
    
    match = re.search(pattern, title_clean)
    if match:
        debate_text = match.group(1)
        # Extract the number from "1er", "2e", "3e"
        if debate_text == "1er":
            return 1
        elif debate_text == "2e":
            return 2
        elif debate_text == "3e":
            return 3
    
    return 999

# def test_get_debate_number():
#     """
#     Comprehensive test suite for the get_debate_number function
#     """
    
#     # Test data covering various cases
#     test_cases = [
#         # Standard cases
#         ("PL 13407-A, vote nominal : 3e débat", 3),
#         ("PL 13250, vote nominal : 1er débat", 1),
#         ("PL 12541-A, vote nominal : 2e débat", 2),
        
#         # Case sensitivity tests
#         ("PL 12575-B, vote nominal : 3E DÉBAT", 3),
#         ("PL 12574-B, vote nominal : 1ER Débat", 1),
#         ("PL 12888-A, vote nominal : 2E débat", 2),
        
#         # Whitespace handling
#         ("PL 12310-A, vote nominal : 1er débat  ", 1),  # trailing spaces
#         ("  PL 13175-A, vote nominal : 3e débat", 3),   # leading spaces
#         ("PL 13253, vote nominal :   2e   débat   ", 2), # multiple spaces
        
#         # Edge cases that should return 999
#         ("PL 13293, vote nominal : 4e débat", 999),      # invalid number
#         ("PL 13293, vote nominal : 1er débat sur", 999), # doesn't end with débat
#         ("PL 13293, vote nominal débat 2e", 999),        # wrong format
#         ("PL 13293, vote nominal : débat", 999),         # missing number
#         ("PL 13293, vote nominal", 999),                 # no débat at all
#         ("", 999),                                       # empty string
#         ("PL 13293, vote nominal : 1er debate", 999),    # wrong language
#         ("PL 13293, vote nominal : premier débat", 999), # wrong format
#     ]
    
#     # Test each case
#     for title, expected in test_cases:
#         result = get_debate_number(title)
#         assert result == expected, f"Failed for '{title}': expected {expected}, got {result}"
    
#     print("✅ All standard tests passed!")

# def test_null_values():
#     """
#     Test handling of null/NaN values
#     """
#     test_cases = [
#         (None, 999),
#         (pd.NA, 999),
#         (pd.NaT, 999),
#         (float('nan'), 999),
#     ]
    
#     for value, expected in test_cases:
#         result = get_debate_number(value)
#         assert result == expected, f"Failed for null value {value}: expected {expected}, got {result}"
    
#     print("✅ Null value tests passed!")

# def test_numeric_inputs():
#     """
#     Test behavior with numeric inputs (should be converted to string)
#     """
#     test_cases = [
#         (123, 999),  # Number without the pattern
#         (0, 999),    # Zero
#         (-1, 999),   # Negative number
#     ]
    
#     for value, expected in test_cases:
#         result = get_debate_number(value)
#         assert result == expected, f"Failed for numeric input {value}: expected {expected}, got {result}"
    
#     print("✅ Numeric input tests passed!")

# def test_special_characters():
#     """
#     Test with special characters and unicode
#     """
#     test_cases = [
#         ("PL 13407-A, vote nominal : 3e débat", 3),      # Normal case
#         ("PL 13407-A, vote nominal : 3e débat!", 999),   # Exclamation at end
#         ("PL 13407-A, vote nominal : 3e débat?", 999),   # Question mark at end
#         ("PL 13407-A, vote nominal : 3e débat.", 999),   # Period at end
#         ("PL 13407-A, vote nominal : 3e débat\n", 999),  # Newline at end
#         ("PL 13407-A, vote nominal : 3e débat\t", 999),  # Tab at end
#     ]
    
#     for title, expected in test_cases:
#         result = get_debate_number(title)
#         assert result == expected, f"Failed for special char test '{title}': expected {expected}, got {result}"
    
#     print("✅ Special character tests passed!")

# def test_regex_pattern_edge_cases():
#     """
#     Test edge cases for the regex pattern
#     """
#     test_cases = [
#         # Valid patterns
#         ("Something : 1er débat", 1),
#         ("Something: 2e débat", 2),
#         ("Something :3e débat", 3),
#         ("Something :   1er   débat   ", 1),
        
#         # Invalid patterns
#         ("Something : 1er  débats", 999),    # plural
#         ("Something : 1erdébat", 999),       # no space
#         ("Something : 1er débat extra", 999), # extra text
#         ("Something 1er débat", 999),        # no colon
#         ("Something : 1 débat", 999),        # just number
#         ("Something : 1ere débat", 999),     # wrong form
#         ("Something : 1st débat", 999),      # English ordinal
#     ]
    
#     for title, expected in test_cases:
#         result = get_debate_number(title)
#         assert result == expected, f"Failed for regex edge case '{title}': expected {expected}, got {result}"
    
#     print("✅ Regex pattern edge case tests passed!")

# def test_performance_with_long_strings():
#     """
#     Test performance with very long strings
#     """
#     # Create a very long string
#     long_prefix = "A" * 1000
#     test_cases = [
#         (f"{long_prefix} : 1er débat", 1),
#         (f"{long_prefix} : 2e débat", 2),
#         (f"{long_prefix} : 3e débat", 3),
#         (f"{long_prefix} : invalid", 999),
#     ]
    
#     for title, expected in test_cases:
#         result = get_debate_number(title)
#         assert result == expected, f"Failed for long string test: expected {expected}, got {result}"
    
#     print("✅ Long string performance tests passed!")

# def test_all_debate_types():
#     """
#     Test all three debate types specifically
#     """
#     test_cases = [
#         ("Test : 1er débat", 1),
#         ("Test : 2e débat", 2),
#         ("Test : 3e débat", 3),
#     ]
    
#     results = []
#     for title, expected in test_cases:
#         result = get_debate_number(title)
#         results.append(result)
#         assert result == expected, f"Failed for debate type test '{title}': expected {expected}, got {result}"
    
#     # Check that we got all three types
#     assert set(results) == {1, 2, 3}, f"Expected all three debate types, got {set(results)}"
    
#     print("✅ All debate type tests passed!")

# def test_batch_processing():
#     """
#     Test with a batch of titles (like original data)
#     """
#     titles = [
#         "PL 13407-A, vote nominal : 3e débat",
#         " PL 13250, vote nominal : 1er débat",
#         "PL 12541-A, vote nominal : 1er débat",
#         "PL 12575-B, vote nominal : 3e débat",
#         "PL 12574-B, vote nominal : 3e débat  ",      
#         "PL 12888-A, vote nominal : 3e débat",
#         "PL 12310-A, vote nominal : 1er débat",
#         "PL 13175-A, vote nominal : 3e débat",
#         "PL 13253, vote nominal : 3e débat",
#         "PL 13293, vote nominal : 3e débat",
#     ]
    
#     expected_results = [3, 1, 1, 3, 3, 3, 1, 3, 3, 3]
    
#     results = [get_debate_number(title) for title in titles]
    
#     assert results == expected_results, f"Batch processing failed: expected {expected_results}, got {results}"
    
#     # Check distribution
#     from collections import Counter
#     counts = Counter(results)
#     expected_counts = Counter(expected_results)
    
#     assert counts == expected_counts, f"Result distribution mismatch: expected {expected_counts}, got {counts}"
    
#     print("✅ Batch processing tests passed!")

# def run_all_tests():
#     """
#     Run all tests
#     """
#     print("Running comprehensive tests for get_debate_number function...")
#     print("=" * 60)
    
#     test_get_debate_number()
#     test_null_values()
#     test_numeric_inputs()
#     test_special_characters()
#     test_regex_pattern_edge_cases()
#     test_performance_with_long_strings()
#     test_all_debate_types()
#     test_batch_processing()
    
#     print("=" * 60)
#     print("🎉 All tests passed! The function is working correctly.")

# if __name__ == "__main__":
#     run_all_tests()