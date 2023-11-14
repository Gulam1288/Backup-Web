from flask import Flask, render_template, request, jsonify, Response
import random
import json
import os
import re
from difflib import SequenceMatcher
from twilio.rest import Client

app = Flask(__name__)

GREET_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREET_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
EXIT_RESPONSES = ["Bye","See you later!","Good bye!","Hope to see you again"]

previous_question = ""
previous_response = ""

feedback_file_path = "supervised_learning.txt"
comments_file = "comments.txt"
with open("dataset.json", "r") as file:
    global dataset
    dataset = json.load(file)

def greet(sentence):
    for word in sentence.split():
        if word.lower() in GREET_INPUTS:
            return random.choice(GREET_RESPONSES)

def generate_response(user_input):
    global previous_question, previous_response, dataset

    print(f"Received user input: {user_input}")  # Add this line for debugging

    if user_input.lower() in GREET_INPUTS:
        return greet(user_input)+"."

    if user_input.lower() in ["bye","see you later"]:
        return random.choice(EXIT_RESPONSES)

    with open(feedback_file_path, "r") as feedback_file:
        feedback_lines = feedback_file.readlines()
        for i in range(0, len(feedback_lines), 4):
            stored_user_message = feedback_lines[i].strip().replace("User Message: ", "")
            stored_bot_response = feedback_lines[i + 1].strip().replace("Bot Response: ", "")
            similarity_ratio = SequenceMatcher(None, user_input.lower(), stored_user_message.lower()).ratio()
            if similarity_ratio >= 1.0:
                if stored_bot_response[-1] in ["!", "."]:
                    if "<" in stored_bot_response:
                        return stored_bot_response
                    elif "/" in stored_bot_response:
                        stored_bot_response = stored_bot_response.replace("/", "<br>\u2022")
                    return stored_bot_response
                else:
                    if "<" in stored_bot_response:
                        return stored_bot_response
                    elif "/" in stored_bot_response:
                        stored_bot_response = stored_bot_response.replace("/", "<br>\u2022")
                    return stored_bot_response + "."

        for i in range(0, len(feedback_lines), 4):
            stored_user_message = feedback_lines[i].strip().replace("User Message: ", "")
            stored_bot_response = feedback_lines[i + 1].strip().replace("Bot Response: ", "")
            similarity_ratio = SequenceMatcher(None, user_input.lower(), stored_user_message.lower()).ratio()

            if similarity_ratio >= 0.9:
                if stored_bot_response[-1] in ["!", "."]:
                    if "<" in stored_bot_response:
                        return stored_bot_response
                    elif "/" in stored_bot_response:
                        stored_bot_response = stored_bot_response.replace("/", "<br>\u2022")
                    return stored_bot_response
                else:
                    if "<" in stored_bot_response:
                        return stored_bot_response
                    elif "/" in stored_bot_response:
                        stored_bot_response = stored_bot_response.replace("/", "<br>\u2022")
                    return stored_bot_response + "."

        for i in range(0, len(feedback_lines), 4):
            stored_user_message = feedback_lines[i].strip().replace("User Message: ", "")
            stored_bot_response = feedback_lines[i + 1].strip().replace("Bot Response: ", "")
            similarity_ratio = SequenceMatcher(None, user_input.lower(), stored_user_message.lower()).ratio()

            if similarity_ratio >= 0.8:
                if stored_bot_response[-1] in ["!", "."]:
                    if "<" in stored_bot_response:
                        return stored_bot_response
                    elif "/" in stored_bot_response:
                        stored_bot_response = stored_bot_response.replace("/", "<br>\u2022")
                    return stored_bot_response
                else:
                    if "<" in stored_bot_response:
                        return stored_bot_response
                    elif "/" in stored_bot_response:
                        stored_bot_response = stored_bot_response.replace("/", "<br>\u2022")
                    return stored_bot_response + "."

        for i in range(0, len(feedback_lines), 4):
            stored_user_message = feedback_lines[i].strip().replace("User Message: ", "")
            stored_bot_response = feedback_lines[i + 1].strip().replace("Bot Response: ", "")
            similarity_ratio = SequenceMatcher(None, user_input.lower(), stored_user_message.lower()).ratio()

            if similarity_ratio >= 1.0:
                if stored_bot_response[-1] in ["!", "."]:
                    if "<" in stored_bot_response:
                        return stored_bot_response
                    elif "/" in stored_bot_response:
                        stored_bot_response = stored_bot_response.replace("/", "<br>\u2022")
                    return stored_bot_response
                else:
                    if "<" in stored_bot_response:
                        return stored_bot_response
                    elif "/" in stored_bot_response:
                        stored_bot_response = stored_bot_response.replace("/", "<br>\u2022")
                    return stored_bot_response + "."

    user_queries_to_bot_responses = {}

    # Iterate through the sub-dictionaries under the "software" key
    for sub_topic, sub_data in dataset["software"].items():
        user_queries = sub_data.get("user_queries", [])
        bot_responses = sub_data.get("bot_responses", [])

        key_value_pairs = dict(zip(user_queries, bot_responses))

        user_queries_to_bot_responses.update(key_value_pairs)

    def get_best_match(query, query_dict, threshold=0.8):
        best_match = None
        best_ratio = 0

        for stored_query in query_dict:
            ratio = SequenceMatcher(None, query.lower(), stored_query.lower()).ratio()
            if ratio > best_ratio and ratio >= threshold:
                best_ratio = ratio
                best_match = stored_query
        return best_match


    for subroot in dataset:
        subroot_data = dataset[subroot]
        current_data = subroot_data

        keywords = user_input.lower().split()
        for keyword in keywords:
            if keyword in current_data:
                current_data = current_data[keyword]

        if "bot_responses" in current_data:
            return random.choice(current_data["bot_responses"])

    best_match = get_best_match(user_input, user_queries_to_bot_responses)
    if best_match and best_match in user_queries_to_bot_responses:
        return user_queries_to_bot_responses[best_match]

    current_data = dataset
    keywords = user_input.lower().split()
    for keyword in keywords:
        if keyword in current_data:
            current_data = current_data[keyword]

    if "bot_responses" in current_data:
        return random.choice(current_data["bot_responses"])

    return "I couldn't find information related to your question."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bot')
def bot():
    return render_template('chatbot.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/details')
def details():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

account_sid = 'ACa3d48f183edb1fcf3f0f9ab3f6b94c83'
auth_token = '8ba39dbd48f619e334d9e8c7ce1b36a3'
twilio_phone_number = '+12253417132'
your_phone_number = '+919908065462'

client = Client(account_sid, auth_token)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            with open("form_data.txt", "a") as file:
                file.write(f"Name: {name}\nEmail: {email}\nMessage: {message}\n\n")

            # Send SMS using Twilio
            message_body = f'New Form Submission from {name}. \nEmail: {email} \nMessage: {message}'
            client.messages.create(
                body=message_body,
                from_=twilio_phone_number,
                to=your_phone_number
            )

            return Response("Data submitted successfully! We will respond soon.", content_type='text/plain')

        return Response("Data submission failed.", content_type='text/plain')

    except Exception as e:
        return Response(f"Internal Server Error. {e}", content_type='text/plain')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form.get('user_message')

    if user_message.lower().startswith("feedback:"):
        feedback = user_message[len("feedback:"):].strip()
        # Process the feedback
        if feedback:
            # Save the feedback to the drawbacks.txt file
            with open("drawbacks.txt", "a") as drawbacks_file:
                drawbacks_file.write(feedback + "\n")
            # Respond with a confirmation message
            return jsonify({"bot_response": "Thank you for your feedback."})

    if user_message.lower() in ['thanks', 'thank you']:
        bot_response = "You are welcome."
    else:
        bot_response = generate_response(user_message)

    has_feedback = False

    if bot_response.startswith("I couldn't find information"):
        # Now, let's check the feedback file
        with open(feedback_file_path, "r") as feedback_file:
            feedback_lines = feedback_file.readlines()
            for i in range(0, len(feedback_lines), 4):
                stored_user_message = feedback_lines[i].strip().replace("User Message: ", "")
                stored_bot_response = feedback_lines[i + 1].strip().replace("Bot Response: ", "")
                similarity_ratio = SequenceMatcher(None, user_message.lower(), stored_user_message.lower()).ratio()
                if similarity_ratio >= 1.0:
                    bot_response = stored_bot_response + "."
                    has_feedback = True

    global um
    um=user_message
    return jsonify({"bot_response": bot_response, "has_feedback": has_feedback})


data_directory = "data"  # Directory to store user data files

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    secret_key = data.get('password')

    if username and password:
        # Generate a secret key

        # Store user data in a text file
        user_data = f"Username: {username}, Password: {password}, Secret Key: {secret_key}"
        file_path = os.path.join(data_directory, f"{username}.txt")
        with open(file_path, "w") as user_file:
            user_file.write(user_data)

        return jsonify(message="Registration successful")
    else:
        return jsonify(message="Invalid input"), 400

@app.route('/check_user', methods=['GET'])
def check_user():
    username = request.args.get('username')
    if username:
        file_path = os.path.join(data_directory, f"{username}.txt")
        user_exists = os.path.exists(file_path)
        return jsonify(exists=user_exists)
    else:
        return jsonify(exists=False)

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    secret_key = data.get('secretKey')

    if username and password and secret_key:
        # Store user data in a text file
        user_data = f"Username: {username}, Password: {password}, Secret Key: {secret_key}"
        file_path = os.path.join(data_directory, f"{username}.txt")
        with open(file_path, "w") as user_file:
            user_file.write(user_data)

        return jsonify(message="User creation successful")
    else:
        return jsonify(message="Invalid input"), 400


@app.route('/loginuser', methods=['POST'])
def loginuser():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        file_path = os.path.join(data_directory, f"{username}.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as user_file:
                user_data = user_file.read()
                if f"Username: {username}, Password: {password}" in user_data:
                    return jsonify(message="Login successful")

        return jsonify(message="Invalid login credentials"), 401
    else:
        return jsonify(message="Invalid input"), 400

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    username = data.get('username')
    secret_key = data.get('secret_key')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if(username == "" or secret_key == "" or new_password == "" or confirm_password == ""):
        return jsonify(message="Please fill all fields!"), 400

    if username and secret_key and new_password and confirm_password:
        file_path = os.path.join(data_directory, f"{username}.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as user_file:
                user_data = user_file.read()
                stored_secret_key = re.search(r'Secret Key: (\w+)', user_data).group(1)

                if secret_key == stored_secret_key:
                    if new_password == confirm_password:
                        user_data = re.sub(r'Password: (\w+)', f'Password: {new_password}', user_data)
                        with open(file_path, "w") as updated_file:
                            updated_file.write(user_data)
                        return jsonify(message="Password reset successful")
                    else:
                        return jsonify(message="Passwords do not match"), 400
                else:
                    return jsonify(message="Invalid secret key"), 400

        return jsonify(message="Invalid credentials for password reset"), 400
    else:
        return jsonify(message="Invalid input"), 400

@app.route('/get_secret_key', methods=['GET'])
def get_secret_key():
    username = request.args.get('username')

    if username:
        file_path = os.path.join(data_directory, f"{username}.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as user_file:
                user_data = user_file.read()
                stored_secret_key = re.search(r'Secret Key: (\w+)', user_data).group(1)
                return jsonify(secretKey=stored_secret_key)

    return jsonify(secretKey=None)

# Updated provide_feedback route
@app.route('/provide_feedback', methods=['POST'])
def provide_feedback():
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

@app.route('/add_comment', methods=['POST'])
def add_comment():
    comment = request.get_json()
    comment_text = comment.get('comment')

    if comment_text:
        try:
            with open(comments_file, 'a') as file:
                file.write(comment_text + '\n')
            return jsonify({'success': True})
        except Exception as e:
            print(str(e))
    return jsonify({'success': False})

@app.route('/get_comments')
def get_comments():
    try:
        with open(comments_file, 'r') as file:
            comments = [line.strip() for line in file.readlines()]
        return jsonify({'comments': comments})
    except Exception as e:
        print(str(e))
        return jsonify({'comments': []})

# Delete a comment
@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    key = request.form.get('key')
    if key != 'g1288':
        return "Invalid key", 403

    comment_to_delete = request.form.get('comment')
    if comment_to_delete:
        try:
            with open(comments_file, 'r') as file:
                lines = file.readlines()
            with open(comments_file, 'w') as file:
                for line in lines:
                    if comment_to_delete not in line:
                        file.write(line)
            return "Comment deleted successfully"
        except Exception as e:
            print(str(e))
            return "Error deleting comment", 500
    else:
        return "Comment not provided", 400

if __name__ == '__main__':
    app.run(debug=False)
