import streamlit as st
import google.generativeai as genai

def get_classification_from_ai(api_key: str, abstract_text: str) -> str:
    """
    Uses the Google Gemini model to classify the abstract based on a specific prompt.

    Args:
        api_key: The user's Google API key.
        abstract_text: The journal abstract to classify.

    Returns:
        The classification category as a string, or an error message.
    """
    try:
        # Configure the generative AI client with the provided API key
        genai.configure(api_key=api_key)
    except Exception as e:
        return f"Error: Could not configure the API. Please check your key. Details: {e}"

    # The prompt provided by the user, formatted for the API call
    prompt = f"""
I want to determine if the following abstract from a journal article talks about ferroptosis, SkyClarys or omaveloxolone, neither, or both. Please provide only the category.

---
{abstract_text}
---
"""

    try:
        # Initialize the model and generate the content
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        # Clean up the response to ensure it's just the category word
        # (e.g., "Ferroptosis", "Both", etc.)
        category = response.text.strip()
        return category

    except Exception as e:
        # Handle potential errors during the API call (e.g., invalid key, network issues)
        return f"Error: An issue occurred while contacting the AI model. Details: {e}"


# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="Generative FA Abstract Classifier",
    page_icon="🧠",
    layout="centered"
)

# --- App Header ---
st.title("AI-Powered FA Abstract Classifier")
st.markdown(
    "This app uses a generative AI model to analyze and categorize journal abstracts "
    "about **Friedreich's Ataxia (FA)**. It evaluates the text's intent, not just keywords."
)

# --- Sidebar for API Key Input ---
with st.sidebar:
    st.header("Configuration")
    st.markdown(
        "To use this app, you need a Google API key for the Gemini model."
    )
    google_api_key = st.text_input(
        "Enter your Google API Key",
        type="password",
        help="Get your free key from https://aistudio.google.com/app/apikey"
    )
    st.markdown("---")
    st.header("How it Works")
    st.info(
        "When you click 'Classify', the abstract is sent to the Google Gemini model "
        "along with the specific instructions you provided. The model then returns the "
        "most appropriate category."
    )


# --- Example Abstract from Prompt ---
example_abstract = (
    "Ferroptosis is an iron-dependent form of regulated cell death, arising from the "
    "accumulation of lipid-based reactive oxygen species when glutathione-dependent "
    "repair systems are compromised. Lipid peroxidation, mitochondrial impairment and "
    "iron dyshomeostasis are the hallmark of ferroptosis, which is emerging as a "
    "crucial player in neurodegeneration. This review provides an analysis of the "
    "most recent advances in ferroptosis, with a special focus on Friedreich's Ataxia "
    "(FA), the most common autosomal recessive neurodegenerative disease, caused by "
    "reduced levels of frataxin, a mitochondrial protein involved in iron-sulfur "
    "cluster synthesis and antioxidant defenses. The hypothesis is that the "
    "iron-induced oxidative damage accumulates over time in FA, lowering the "
    "ferroptosis threshold and leading to neuronal cell death and, at last, to "
    "cardiac failure. The use of anti-ferroptosis drugs combined with treatments "
    "able to activate the antioxidant response will be of paramount importance in FA "
    "therapy, such as in many other neurodegenerative diseases triggered by "
    "oxidative stress."
)

# --- User Input Section ---
st.subheader("Paste Abstract Here")
user_input = st.text_area(
    label="Enter the abstract text:",
    value=example_abstract,
    height=300,
    label_visibility="collapsed"
)

# --- Classification Button and Output ---
if st.button("Classify Abstract", type="primary"):
    # Validate that the API key and abstract are provided
    if not google_api_key:
        st.warning("Please enter your Google API Key in the sidebar to proceed.")
    elif not user_input or not user_input.strip():
        st.warning("Please paste an abstract into the text box.")
    else:
        # Show a spinner while the AI is processing
        with st.spinner("🤖 The AI is analyzing the abstract..."):
            category = get_classification_from_ai(google_api_key, user_input)

            st.subheader("Classification Result")
            # Display an error message if the API call failed
            if category.startswith("Error:"):
                st.error(category)
            else:
                st.success(f"**Category:** {category}")
