from fuzzywuzzy import fuzz
import pandas as pd

# Load your dataset
data = pd.read_csv('static/models/kidney.csv')

# List of other organs to check against user queries
other_organs = ['liver', 'eye', 'ear', 'heart', 'lung', 'pancreas']

# Function to check if the user query contains key phrases related to kidney transplantation
def contains_kidney_key_phrases(user_query):
    kidney_key_phrases = ['kidney', 'transplant', 'donor', 'waiting time', 'rejection', 'immunosuppressant']
    return any(phrase in user_query.lower() for phrase in kidney_key_phrases)

# Function to check if the user query contains words related to other organs
def contains_other_organs(user_query):
    return any(organ in user_query.lower() for organ in other_organs)

# Function to get the chatbot's response based on the user query
def chatbot_response(user_query):
    # Check if the user query contains key phrases related to kidney transplantation
    if contains_kidney_key_phrases(user_query):
        # Initialize variables to store the best match and score
        best_match = None
        best_score = 0

        for index, row in data.iterrows():
            transplantation_query = row['User_Query']
            score = fuzz.ratio(user_query.lower(), transplantation_query.lower())  # Using fuzzy matching

            if score > best_score:
                best_score = score
                best_match = transplantation_query

        # Check if the user query contains words related to other organs
        if contains_other_organs(user_query):
            response = " Please ask questions related to kidney transplantation and not about other queries."
        elif best_match is not None:
            transplantation_data = data[data['User_Query'] == best_match]
            response = f" {transplantation_data['Response'].iloc[0]}"
        elif('kidney' not in user_query):
            response = "I don't have specific information about that. Please ask another question related to kidney transplantation."
    else:
        response = " I beg to divert your attention to only kidney transplantation queries"

    return response
