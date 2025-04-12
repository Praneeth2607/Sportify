from bardapi import Bard
import os

os.environ['_BARD_API_KEY'] = "your_bard_api_key_here"

def get_user_details_from_storage(username):
    user_database = {
        "Adi_05": {
            "full_name": "Adithya Narayan",
            "email": "adithya.narayan@example.com",
            "interests": ["Football", "Chess"],
            "city": "New York",
            "occupation": "Software Engineer"
        },
        "Praneeth_45": {
            "full_name": "Praneeth Kumar",
            "email": "praneeth.kumar@example.com",
            "interests": ["Basketball", "Throwball"],
            "city": "London",
            "occupation": "Marketing Manager"
        },
        "Kish_69": {
            "full_name": "Kishore Ramaswamy",
            "email": "kishore.ramaswamy@example.com",
            "interests": ["Carrom", "Badminton"],
            "city": "Los Angeles",
            "occupation": "Data Scientist"
        },
         "arav_06": {
            "full_name": "Aarav Kumar",
            "email": "aarav.kumar@example.com",
            "interests": ["Shooting", "Chess"],
            "city": "Delhi",
            "occupation": "Student"
        },
        
    }

    if username in user_database:
        user_data = user_database[username]
        return f"Full Name: {user_data['full_name']}, Email: {user_data['email']}, Interests: {', '.join(user_data['interests'])}, City: {user_data['city']}, Occupation: {user_data['occupation']}"
    else:
        return f"User '{username}' not found."

def ask_bard_about_user(username, question):
    details = get_user_details_from_storage(username)
    if "not found" in details:
        return details

    bard = Bard()
    prompt = f"Based on the following information about {username}: {details}\n\nAnswer the question: {question}"
    try:
        return bard.get_answer(prompt)['content']
    except Exception as e:
        return f"Error communicating with Bard: {e}"