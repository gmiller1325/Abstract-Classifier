import streamlit as st
import google.generativeai as genai

# --- Page and Model Configuration ---

st.set_page_config(
    page_title="FA Abstract Classifier",
    page_icon="🧬",
    layout="centered"
)

# This is the correct, simple way to configure the API key for Streamlit.
# It automatically reads from your .streamlit/secrets.toml file.
try:
    genai.configure(api_key=st.secrets["google_api_key"])
except Exception:
    st.error("Your Google API key is missing or invalid. Please check your .streamlit/secrets.toml file.")
    st.stop()


# --- Core Classification Function ---

def get_classification_from_ai(abstract_text: str) -> str:
    """Uses the Google Gemini model to classify the abstract."""
    
    prompt = f"""
I want to determine if the following abstract from a journal article talks about ferroptosis, SkyClarys or omaveloxolone, neither, or both. Please provide only the category.

---
{abstract_text}
---
"""
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: Could not contact the AI model. Details: {e}"


# --- Streamlit App UI ---

st.title("AI-Powered FA Abstract Classifier")
st.markdown(
    "This app uses a generative AI model to categorize journal abstracts about Friedreich's Ataxia (FA)."
)

example_abstract = (
    "Ferroptosis is an iron-dependent form of regulated cell death, arising from the "
    "accumulation of lipid-based reactive oxygen species when glutathione-dependent "
    "repair systems are compromised. This review provides an analysis of the "
    "most recent advances in ferroptosis, with a special focus on Friedreich's Ataxia "
    "(FA), the most common autosomal recessive neurodegenerative disease, caused by "
    "reduced levels of frataxin. The use of anti-ferroptosis drugs will be of paramount importance in FA therapy."
)

user_input = st.text_area(
    "Paste the abstract text below:",
    value=example_abstract,
    height=250,
)

if st.button("Classify Abstract", type="primary"):
    if user_input and user_input.strip():
        with st.spinner("🤖 The AI is analyzing the abstract..."):
            category = get_classification_from_ai(user_input)
            st.subheader("Classification Result")
            if category.startswith("Error:"):
                st.error(category)
            else:
                st.success(f"**Category:** {category}")
    else:
        st.warning("Please paste an abstract into the text box.")