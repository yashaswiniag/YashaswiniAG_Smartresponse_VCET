import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# Replace with your OpenAI API key
openai.api_base = "https://api.openai.com/v1"
openai.api_key = ""

# Replace with your email credentials
SMTP_SERVER = "smtp.gmail.com"  # For Gmail
SMTP_PORT = 587
EMAIL_ADDRESS = "yashaswiniag29@gmail.com"
EMAIL_PASSWORD = ""

# Path to feedback storage file
FEEDBACK_FILE = "feedback.json"

def load_feedback():
    """Load stored feedback from a file."""
    try:
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_feedback(feedback_data):
    """Save feedback to the feedback file."""
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback_data, f, indent=4)

def generate_email_response(client_input, feedback=None):
    """
    Generate a professional and human-like email response using OpenAI's GPT API.
    """
    # Crafting the prompt for OpenAI
    messages = [
        {"role": "system", "content": "You are a helpful assistant that writes professional emails."},
        {"role": "user", "content": f"The client has requested an estimated cost and timeline for their project:\n\n{client_input}\n\nGenerate a professional response. {feedback if feedback else ''}"},
    ]

    try:
        # Call OpenAI's Chat API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-4" if you prefer
            messages=messages,
            max_tokens=250,
            temperature=0.7,
        )

        # Extract the content from the response
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating email response: {e}"

def send_email(to_email, subject, body):
    """
    Send an email using the SMTP protocol.
    """
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Log in to the email account
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())  # Send the email
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def request_feedback():
    """Request feedback from the client."""
    feedback = input("Please provide feedback on the email response: ")
    return feedback

# Main script
if __name__ == "__main__":
    # Client's input (example provided in the scenario)
    client_input = """
    We are planning to develop a cloud-based inventory management system with real-time tracking,
    advanced analytics, and user-friendly dashboards. We aim to have it ready within six months. 
    Can you provide an estimated cost and timeline for this project?
    """
    
    # Generate the email response
    email_body = generate_email_response(client_input)

    # Email details
    recipient_email = "rachithamn2003@gmail.com"
    email_subject = "Estimated Cost and Timeline for Your Project"

    # Send the email
    send_email(recipient_email, email_subject, email_body)

    # Request feedback from the user
    feedback = request_feedback()

    # Save feedback to a file
    feedback_data = load_feedback()
    feedback_data.append({
        "client": recipient_email,
        "feedback": feedback
    })
    save_feedback(feedback_data)

