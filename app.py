import streamlit as st
from google import genai

# Get API key securely
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)
# Set page config
st.set_page_config(
    page_title="Team 11 - Smart Crop Recommendation", layout="wide")

# Custom style


def set_custom_style():
    st.markdown("""
        <style>
            body {
                background: linear-gradient(to right, #e6f9e6, #f0fff0);
                color: #2e2e2e;
            }
            .stButton>button {
                background-color: #5cb85c;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
            }
            .stButton>button:hover {
                background-color: #4cae4c;
            }
            .stTextInput>div>div>input {
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)


set_custom_style()

# Crop recommendation function


def recommend_crop_gemini(soil_type, pH, nitrogen, phosphorus, potassium, rainfall, temperature, location):
    prompt = f"""
    Based on the following soil and weather conditions, suggest the best crop(s) to grow in {location}:
    - Soil Type: {soil_type}
    - Soil pH: {pH}
    - Nitrogen Level: {nitrogen} ppm
    - Phosphorus Level: {phosphorus} ppm
    - Potassium Level: {potassium} ppm
    - Annual Rainfall: {rainfall} mm
    - Average Temperature: {temperature} °C

    Provide a concise table with a seasonal timeline and matching crops.
    Use simple language and limit technical analysis.
    
    Start the response with:
    "Based on the provided conditions, the recommended crop(s) are:"

    End with:
    "Thank you for using the Smart Crop Recommendation System by Team 11 🌾🌾🌾."
    (This ending should be outside the table.)
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip() if response and hasattr(response, 'text') else "⚠️ No response from Gemini."
    except Exception as e:
        return f"⚠️ Error communicating with Gemini: {e}"


# UI Layout
st.markdown("<h1 style='color: #2e7d32;'>🌱 Team 11 - Smart Crop Recommendation</h1>",
            unsafe_allow_html=True)
st.markdown("<p>Fill in your soil and weather data to get AI-generated crop suggestions.</p>",
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    soil_type = st.selectbox(
        "🧱 Soil Type", ["Sandy", "Clay", "Loamy", "Silty", "Peaty", "Saline"])
    pH = st.slider("🔬 Soil pH", 4.0, 9.0, 6.5)
    nitrogen = st.number_input("🧪 Nitrogen (ppm)", 0, 200, 50)
    phosphorus = st.number_input("🧪 Phosphorus (ppm)", 0, 200, 50)

with col2:
    potassium = st.number_input("🧪 Potassium (ppm)", 0, 200, 50)
    rainfall = st.number_input("🌧️ Annual Rainfall (mm)", 200, 3000, 1200)
    temperature = st.number_input("🌡️ Avg. Temperature (°C)", 0, 50, 25)
    location = st.text_input("📍 Location (City/District/State)", "")

st.markdown("<hr>", unsafe_allow_html=True)

# Predict button
if st.button("🚀 Recommend Crop"):
    if location.strip():
        with st.spinner("🤖 Fetching recommendations from Gemini..."):
            result = recommend_crop_gemini(
                soil_type, pH, nitrogen, phosphorus, potassium, rainfall, temperature, location)
        st.markdown("<h4>🔍 Recommendation Result:</h4>",
                    unsafe_allow_html=True)
        st.markdown(
            f"<div style='background: #eaffea; padding: 15px; border-radius: 10px;'>{result}</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning(
            "⚠️ Please provide a location to get region-specific crop recommendations.")
