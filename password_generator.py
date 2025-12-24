import streamlit as st
import random
import string
import pandas as pd

st.set_page_config(page_title="Password Generator")
st.title("Simple Password Generator")

if "history" not in st.session_state:
    st.session_state.history = []
if "strengths" not in st.session_state:
    st.session_state.strengths = []
if "total" not in st.session_state:
    st.session_state.total = 0


def password_strength(pwd):
    score = 0

    if any(ch.isupper() for ch in pwd):
        score += 1
    if any(ch.islower() for ch in pwd):
        score += 1
    if any(ch.isdigit() for ch in pwd):
        score += 1
    if any(ch in string.punctuation for ch in pwd):
        score += 1
    if len(pwd) >= 12:
        score += 1

    if score <= 2:
        return "Weak", "red"
    elif score <= 4:
        return "Medium", "orange"
    else:
        return "Strong", "green"


def save_password(pwd):
    with open("passwords.txt", "a") as file:
        file.write(pwd + "\n")


st.header("Options")

length = st.number_input("Password length", min_value=0, value=12)

preset = st.radio(
    "Choose a theme preset",
    ["Letters Only", "Letters + Numbers", "Full Strength", "Custom"]
)

use_upper = use_lower = use_numbers = use_symbols = False

if preset == "Letters Only":
    use_upper = True
    use_lower = True
elif preset == "Letters + Numbers":
    use_upper = True
    use_lower = True
    use_numbers = True
elif preset == "Full Strength":
    use_upper = True
    use_lower = True
    use_numbers = True
    use_symbols = True
else:
    use_upper = st.checkbox("Uppercase Letters")
    use_lower = st.checkbox("Lowercase Letters")
    use_numbers = st.checkbox("Numbers")
    use_symbols = st.checkbox("Symbols")


if st.button("Generate Password"):
    if length < 8:
        st.error("Hmm… that’s pretty short. Try 8 or more characters!")
    else:
        pool = ""
        password = ""

        if use_upper:
            pool += string.ascii_uppercase
            password += random.choice(string.ascii_uppercase)

        if use_lower:
            pool += string.ascii_lowercase
            password += random.choice(string.ascii_lowercase)

        if use_numbers:
            pool += string.digits
            password += random.choice(string.digits)

        if use_symbols:
            pool += string.punctuation
            password += random.choice(string.punctuation)

        if pool == "":
            st.warning("Hey, pick at least one type of character, please!")
        else:
            while len(password) < length:
                password += random.choice(pool)

            pwd_list = list(password)
            random.shuffle(pwd_list)
            password = "".join(pwd_list)

            st.session_state.total += 1
            st.session_state.history.append(password)

            strength, color = password_strength(password)
            st.session_state.strengths.append(strength)

            save_password(password)

            st.subheader("Here’s your password:")
            st.code(password)
            st.markdown(f"Strength: :{color}[{strength}]")


st.divider()
st.write(f"You’ve generated {st.session_state.total} passwords so far!")

if st.checkbox("Show Password History"):
    if st.session_state.history:
        df = pd.DataFrame({
            "Password": st.session_state.history,
            "Strength": st.session_state.strengths
        })
        st.table(df)
    else:
        st.write("No passwords yet… generate one first!")

if st.button("Clear History"):
    st.session_state.history = []
    st.session_state.strengths = []
    st.session_state.total = 0
    st.rerun()
