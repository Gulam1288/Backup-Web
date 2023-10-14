from flask import Flask, render_template, request, jsonify
import random
import json
import re
from difflib import SequenceMatcher

app = Flask(__name__)

# Load the dataset content
with open("dataset.txt", "r") as file:
    dataset_content = file.read()

GREET_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREET_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

previous_question = ""
previous_response = ""

feedback_file_path = "supervised_learning.txt"

def greet(sentence):
    for word in sentence.split():
        if word.lower() in GREET_INPUTS:
            return random.choice(GREET_RESPONSES)

def generate_response(user_input, dataset_content):
    global previous_question, previous_response

    print(f"Received user input: {user_input}")  # Add this line for debugging

    if user_input.lower() in GREET_INPUTS:
        return greet(user_input)+"."

    response = ""
    rules = dataset_content.split(".")
    for rule in rules:
        if user_input in rule.lower():
            response += f"\n {rule}.\n"
    if response:
        return response
    else:
        # Check if the user is asking the same question again
        if user_input == previous_question:
            return previous_response
        else:
            # Check for similarity with supervised learning data

            # Now, let's check the feedback file
            with open(feedback_file_path, "r") as feedback_file:
                feedback_lines = feedback_file.readlines()
                for i in range(0, len(feedback_lines), 4):
                    stored_user_message = feedback_lines[i].strip().replace("User Message: ", "")
                    stored_bot_response = feedback_lines[i + 1].strip().replace("Bot Response: ", "")
                    stored_feedback = feedback_lines[i + 2].strip().replace("Feedback: ", "")
                    similarity_ratio = SequenceMatcher(None, user_input.lower(), stored_user_message.lower()).ratio()
                    if user_input.lower() == stored_bot_response.lower():
                        return stored_user_message
                    if similarity_ratio >= 1.0:
                        if stored_bot_response[-1] in ["!","."]:
                            return stored_bot_response
                        else:
                            return stored_bot_response+"."

                for i in range(0, len(feedback_lines), 4):
                    stored_user_message = feedback_lines[i].strip().replace("User Message: ", "")
                    stored_bot_response = feedback_lines[i + 1].strip().replace("Bot Response: ", "")
                    stored_feedback = feedback_lines[i + 2].strip().replace("Feedback: ", "")
                    similarity_ratio = SequenceMatcher(None, user_input.lower(), stored_user_message.lower()).ratio()

                    if similarity_ratio >= 0.9:
                        if stored_bot_response[-1] in ["!", "."]:
                            return stored_bot_response
                        else:
                            return stored_bot_response + "."
                for i in range(0, len(feedback_lines), 4):
                    stored_user_message = feedback_lines[i].strip().replace("User Message: ", "")
                    stored_bot_response = feedback_lines[i + 1].strip().replace("Bot Response: ", "")
                    stored_feedback = feedback_lines[i + 2].strip().replace("Feedback: ", "")
                    similarity_ratio = SequenceMatcher(None, user_input.lower(), stored_user_message.lower()).ratio()

                    if similarity_ratio >= 0.8:
                        if stored_bot_response[-1] in ["!", "."]:
                            return stored_bot_response
                        else:
                            return stored_bot_response + "."

                for i in range(0, len(feedback_lines), 4):
                    stored_user_message = feedback_lines[i].strip().replace("User Message: ", "")
                    stored_bot_response = feedback_lines[i + 1].strip().replace("Bot Response: ", "")
                    stored_feedback = feedback_lines[i + 2].strip().replace("Feedback: ", "")
                    similarity_ratio = SequenceMatcher(None, user_input.lower(), stored_user_message.lower()).ratio()

                    if similarity_ratio >= 0.7:
                        if stored_bot_response[-1] in ["!", "."]:
                            return stored_bot_response
                        else:
                            return stored_bot_response + "."
            # If no matching stored response is found, return a default message
            return "I couldn't find information related to your question."


@app.route('index.html')
def home():
    return render_template('index.html')

@app.route('chatbot.html')
def bot():
    return render_template('chatbot.html')

@app.route('about.html')
def details():
    return render_template('about.html')

@app.route('login.html')
def login():
    return render_template('login.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form.get('user_message')

    if user_message in ['thanks', 'thank you']:
        bot_response = "You are welcome."
    else:
        bot_response = generate_response(user_message, dataset_content)

    has_feedback = False

    if bot_response.startswith("I couldn't find information"):
        # Now, let's check the feedback file
        with open(feedback_file_path, "r") as feedback_file:
            feedback_lines = feedback_file.readlines()
            for i in range(0, len(feedback_lines), 4):
                stored_user_message = feedback_lines[i].strip().replace("User Message: ", "")
                stored_bot_response = feedback_lines[i + 1].strip().replace("Bot Response: ", "")
                stored_feedback = feedback_lines[i + 2].strip().replace("Feedback: ", "")
                similarity_ratio = SequenceMatcher(None, user_message.lower(), stored_user_message.lower()).ratio()
                if similarity_ratio >= 0.7:
                    bot_response = stored_bot_response + "."
                    has_feedback = True

    global um
    um=user_message
    return jsonify({"bot_response": bot_response, "has_feedback": has_feedback})

# Updated provide_feedback route
@app.route('/provide_feedback', methods=['POST'])
def provide_feedback():
    user_message = request.form.get('user_message')
    bot_response = request.form.get('bot_response')
    feedback = request.form.get('feedback')
    if not feedback:
        return "Please provide feedback for the bot's response."

    # Save feedback to a text file
    with open(feedback_file_path, "a") as feedback_file:
        feedback_file.write(f"User Message: {um}\n")
        feedback_file.write(f"Bot Response: {bot_response}\n")
        feedback_file.write(f"Feedback: {feedback}\n\n")

    return "Feedback received successfully."

@app.route('/export_chat', methods=['POST'])
def export_chat():
    chat_data = request.form.get('chat_data')

    if chat_data:
        # Create a response with the chat data as a text file
        response = Response(chat_data, content_type='text/plain')
        response.headers["Content-Disposition"] = "attachment; filename=chat.txt"
        return response
    else:
        return "Chat data not provided.", 400
    
if __name__ == '__main__':
    app.run(debug=True)
