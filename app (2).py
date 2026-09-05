
import streamlit as st
from groq import Groq


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Email Generator",
    page_icon="✉️",
    layout="centered"
)


# =========================================================
# TITLE
# =========================================================

st.title("✉️ AI Email Generator")

st.write(
    "Generate professional emails using Groq AI."
)


# =========================================================
# LOAD GROQ API KEY
# =========================================================

try:

    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

except Exception as e:

    st.error("❌ API key could not be loaded.")

    st.code(
        f"Error: {type(e).__name__}: {str(e)}"
    )

    st.stop()


# =========================================================
# CREATE GROQ CLIENT
# =========================================================

try:

    client = Groq(
        api_key=GROQ_API_KEY
    )

except Exception as e:

    st.error("❌ Could not create Groq client.")

    st.code(
        f"Error: {type(e).__name__}: {str(e)}"
    )

    st.stop()


# =========================================================
# INPUTS
# =========================================================

email_type = st.selectbox(
    "Email Type",
    [
        "Job Application",
        "Business Email",
        "Follow-up Email",
        "Meeting Request",
        "Thank You Email",
        "Complaint Email",
        "Leave Request",
        "Cold Email",
        "Apology Email"
    ]
)


recipient = st.text_input(
    "Recipient",
    placeholder="Example: colleague"
)


tone = st.selectbox(
    "Tone",
    [
        "Professional",
        "Formal",
        "Friendly",
        "Casual",
        "Persuasive"
    ]
)


purpose = st.text_area(
    "What should the email be about?",
    placeholder=(
        "Example: We have to discuss our new product."
    ),
    height=120
)


details = st.text_area(
    "Additional Details",
    placeholder=(
        "Example: We will meet tomorrow."
    ),
    height=120
)


# =========================================================
# GENERATE EMAIL
# =========================================================

if st.button(
    "✨ Generate Email",
    use_container_width=True
):

    if not purpose.strip():

        st.warning(
            "Please describe what the email should be about."
        )

        st.stop()


    prompt = f"""
You are an expert professional email writer.

Write an email based ONLY on the information provided.

Email Type:
{email_type}

Recipient:
{recipient}

Tone:
{tone}

Purpose:
{purpose}

Additional Details:
{details}

Requirements:

1. Write a natural and professional email.
2. Create a suitable subject line.
3. Do not invent information.
4. Use [Name] if the recipient's name is unknown.
5. Keep the email concise.
6. Correct grammar and spelling automatically.
7. Return only the email.

Format:

Subject: <subject>

<email body>
"""


    # =====================================================
    # CALL GROQ
    # =====================================================

    with st.spinner(
        "🤖 Generating your email..."
    ):

        try:

            response = client.chat.completions.create(

                model="openai/gpt-oss-120b",

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional "
                            "email writing assistant."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.7,

                max_completion_tokens=500
            )


            generated_email = (
                response
                .choices[0]
                .message
                .content
            )


            st.success(
                "✅ Email generated successfully!"
            )

            st.subheader(
                "📧 Generated Email"
            )

            st.text_area(
                "Your Email",
                value=generated_email,
                height=350
            )


        except Exception as e:

            st.error(
                "❌ Groq request failed."
            )

            # THIS IS IMPORTANT
            # It shows the actual reason
            st.code(
                f"""
Error Type:
{type(e).__name__}

Error Message:
{str(e)}
"""
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Powered by Groq + Llama + Streamlit"
)
