import streamlit as st

# --- Brand Color Palette ---
# Using soft, professional tones to appeal to female entrepreneurs (the target audience)
CHERRY_BLOSSOM = "#F9F1F3"  # Primary theme color (soft pink)
POWDER_PETAL = "#F9F1F3"    # Page background
DUST_GREY = "#E8F0FE"       # Sidebar background
ICE_BLUE = "#E8F0FE"        # Hover states and accents
DEEP_BLUE = "#0747A6"       # Call-to-action (CTA) and emphasis
TEXT_COLOR = "#2D3436"      # Primary text color for readability

def apply_custom_css():
    """
    Injects global CSS into the Streamlit app to override default styling.
    This creates a modern, custom 'BackHer' brand identity.
    """
    st.markdown(f"""
        <style>
        /* --- Layout Optimization --- */
        /* Forces the app to use the full width and adds breathable padding */
        .stAppViewMain .main .block-container {{
            max-width: 100% !important;
            width: 100% !important;
            padding: 2rem 4% !important;
        }}

        /* --- Global Background --- */
        .stApp {{ 
            background-color: {POWDER_PETAL}; 
        }}
        
        /* --- Sidebar Styling --- */
        /* Customizes the sidebar background and adds a subtle right border */
        [data-testid="stSidebar"] {{
            background-color: {DUST_GREY} !important;
            border-right: 1px solid #D1E3F8;
        }}

        /* Sidebar Typography: Using clean, modern sans-serif fonts */
        [data-testid="stSidebar"] .stText, 
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label {{
            font-family: 'Inter', 'Segoe UI', sans-serif !important;
        }}
        
        /* --- Unified Button Component --- */
        /* Transforms default Streamlit buttons into branded rounded cards */
        .stButton>button {{
            background-color: {CHERRY_BLOSSOM};
            color: {TEXT_COLOR};
            border-radius: 12px;
            border: 1px solid #FADADD;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease; /* Smooth transition for hover effects */
            width: 100%;
        }}

        /* Button Hover State: Adds elevation and color shift for better UX feedback */
        .stButton>button:hover {{
            background-color: {ICE_BLUE};
            color: {DEEP_BLUE} !important;
            border: 1px solid {DEEP_BLUE};
            transform: translateY(-2px); /* Subtle lift effect */
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        
        /* --- Typography --- */
        h1, h2, h3 {{ 
            color: {TEXT_COLOR}; 
            font-family: 'Inter', -apple-system, sans-serif;
            font-weight: 700;
        }}

        p {{
            color: {TEXT_COLOR};
            line-height: 1.6;
        }}

        /* --- Custom Metric Card Class --- */
        /* Used for displaying financial ratios and key performance indicators (KPIs) */
        .metric-card {{
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            border-left: 5px solid {DEEP_BLUE};
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            margin-bottom: 15px;
        }}
        </style>
    """, unsafe_allow_html=True)