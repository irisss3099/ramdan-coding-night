import re
import random
import string
import streamlit as st

st.markdown(
    """
<style>
    .footer {
        text-align: center;
        padding: 1rem;
        font-size: 1.0rem;
        color: #2C2C54; /* Dark font for better visibility */
        margin-top: 2rem;
        background: linear-gradient(90deg, #E0E7FF, #CBD5E1); /* Light gradient background */
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #4F46E5, #6366F1);
        -webkit-background-clip: text;
        color: transparent;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
        transition: transform 0.3s ease;
    }
    .title:hover {
        transform: scale(1.1);
    }
    .generate-button {
        background: linear-gradient(90deg, #87CEFA, #D8BFD8); /* Sky blue to light purple gradient */
        color: #2C2C54; /* Dark text for better contrast */
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 8px;
        font-size: 1.2rem;
        transition: background 0.4s ease, transform 0.3s ease;
    }
    .generate-button:hover {
        background: linear-gradient(90deg, #B0E0E6, #E6E6FA); /* Lighter gradient on hover */
        transform: scale(1.1);
    }
    body {
        background-color: #FFDAB9; /* Peach background */
    }
</style>
    """,
    unsafe_allow_html=True,
)

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Check password length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("❌ Add at least one uppercase letter (A-Z).")

    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("❌ Add at least one lowercase letter (a-z).")

    # Check for digits
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("❌ Include at least one digit (0-9).")

    # Check for special characters
    if re.search(r'[!@#$%^&*]', password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    # Check for common passwords
    common_passwords = ["password123", "123456", "qwerty", "letmein", "12345678"]
    if password.lower() in common_passwords:
        score = 1
        feedback.append("❌ This password is too common. Choose a more unique one!")

    return score, feedback

# Function to evaluate the score
def evaluate_score(score):
    if score == 5:
        return "Strong 💪"
    elif 3 <= score <= 4:
        return "Moderate 🟡"
    else:
        return "Weak ⚠️"

# Password generator
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# Streamlit Interface
st.markdown("<div class='title'>🔐 Password Strength Meter</div>", unsafe_allow_html=True)

# User Input
password = st.text_input("Enter a password to check its strength:", type="password")

if password:
    score, feedback = check_password_strength(password)
    strength = evaluate_score(score)

    st.subheader(f"Password Strength: {strength}")

    if feedback:
        st.warning("Here are some suggestions to improve your password:")
        for tip in feedback:
            st.write(tip)

    if strength == "Strong 💪":
        st.success("✅ Your password is strong and secure!")

    if strength == "Weak ⚠️":
        st.info("💡 Suggested Strong Password:")
        st.code(generate_password(16))

# Generate Random Strong Password Button
if st.markdown("<button class='generate-button'>🔍 Generate a Strong Password</button>", unsafe_allow_html=True):
    st.code(generate_password(16))

# Footer
st.markdown("<div class='footer'>🚀 SK PASSWORD STRENGTH METER | © 2025 | <a href='#' style='color: #2C2C54;'>Terms & Privacy</a></div>", unsafe_allow_html=True)
