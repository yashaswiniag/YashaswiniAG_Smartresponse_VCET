import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Replace with your OpenAI API key
openai.api_base="https://openrouter.ai/api/v1"
openai.api_key = "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"

# Replace with your email credentials
SMTP_SERVER = "smtp.gmail.com"  # For Gmail
SMTP_PORT = 587
EMAIL_ADDRESS = "yashaswiniag29@gmail.com"
EMAIL_PASSWORD = "updk eioi dbrq xpaj"

def generate_email_response(client_input):
    """
    Generate a professional and human-like email response using OpenAI's GPT API.
    """
    # Crafting the prompt for OpenAI
    prompt = f"""
    You are a project manager responding to a client's query. The client has requested an estimated cost and timeline 
    for their large project based on initial requirements provided. Your email should be professional, polite, and 
    concise, avoiding overused phrases like 'I hope this email finds you well.' Focus on providing a clear and 
    informative response.

    Client's Input:
    {client_input}

    Please generate a professional email response.
    """
    
    try:
        # Call OpenAI's GPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes professional emails."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=250,
            temperature=0.7
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
