# app.py

import streamlit as st
from styles import apply_custom_css
import views.welcome_view as welcome
import views.home_view as home
import views.statements_view as statements 
import finance_engine as fe 
import ai_consultant as ai

# --- 持久化 API Key 初始化 ---
if 'api_key' not in st.session_state: st.session_state.api_key = ""

# 1. 页面配置
from PIL import Image
logo_img = Image.open("logo.png")
st.set_page_config(page_title="BackHer | Financial Intelligence", layout="wide", page_icon=logo_img)
apply_custom_css()

# 2. 状态初始化
if 'is_logged_in' not in st.session_state: st.session_state.is_logged_in = False
if 'page_view' not in st.session_state: st.session_state.page_view = "Landing" 
if 'user_profile' not in st.session_state: st.session_state.user_profile = {"name": "", "email": ""}
if 'businesses' not in st.session_state: st.session_state.businesses = [] 
if 'current_biz_idx' not in st.session_state: st.session_state.current_biz_idx = None 
if 'months_data' not in st.session_state: st.session_state.months_data = {}

# --- A. Sidebar 导航控制 ---
with st.sidebar:
    try: st.image("logo.png", width=120)
    except: st.title("💰 BackHer")
    

    # --- 🔑 新增：API KEY 输入框 (最小化调整) ---
    #st.subheader("🤖 AI Settings")
    #current_key = st.text_input("Gemini API Key", type="password", value=st.session_state.api_key)
    #if current_key != st.session_state.api_key:
    #    st.session_state.api_key = current_key
    if 'api_key' not in st.session_state or st.session_state.api_key == "":
        st.session_state.api_key = ""
    
    
    if not st.session_state.is_logged_in:
        # 未登录导航
        if st.button("🏠 Landing Page", use_container_width=True):
            st.session_state.page_view = "Landing"
            st.rerun()
        if st.button("🔐 Owner Login", use_container_width=True):
            st.session_state.page_view = "Login"
            st.rerun()
    else:
        st.write(f"👤 **Owner:** {st.session_state.user_profile['name']}")
        
        if st.button("🏠 My Business Portfolio", use_container_width=True):
            st.session_state.page_view = "User_Dashboard"
            st.rerun()

        if st.session_state.current_biz_idx is not None:
            biz_name = st.session_state.businesses[st.session_state.current_biz_idx]['name']
            st.divider()
            st.subheader(f"🏢 {biz_name}")
            
            if st.button("📈 Business Overview Hub", use_container_width=True):
                st.session_state.page_view = "Home"
                st.rerun()
            
            if st.button("📊 Financial Statements", use_container_width=True):
                st.session_state.page_view = "Statements"
                st.rerun()

            st.divider()
            st.subheader("🏦 Bank Integration")
            if st.button("🔗 Link Bank via Plaid", use_container_width=True):
                with st.spinner(f"Connecting {biz_name} to Plaid..."):
                    import time; time.sleep(1.5) 
                    results = fe.process_simulated_plaid_data('plaid_simulator.json')
                    st.session_state.months_data = results
                    st.success("Fetched 6 months of historical data!")
                    st.balloons()
                    st.rerun()
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.is_logged_in = False
            st.session_state.current_biz_idx = None
            st.session_state.page_view = "Landing"
            st.rerun()

# --- B. 路由逻辑 (修正函数名确保运行) ---
if st.session_state.page_view == "Landing":
    welcome.render_landing_page()

elif st.session_state.page_view == "Login":
    welcome.render_login_page()

elif st.session_state.page_view == "User_Dashboard":
    home.render_user_dashboard()

elif st.session_state.page_view == "Home":
    home.render_business_overview()

elif st.session_state.page_view == "Welcome_Step_1":
    st.title("✨ Create Business Profile")
    b_name = st.text_input("Business Name")
    b_type = st.selectbox("Industry Type", ["E-commerce", "SaaS", "Retail", "Service", "Other"])
    
    if st.button("Initialize Business DNA"):
        if b_name:
            st.session_state.businesses.append({"name": b_name, "type": b_type})
            st.session_state.current_biz_idx = len(st.session_state.businesses) - 1
            st.session_state.page_view = "Home" 
            st.rerun()
            
elif st.session_state.page_view == "Statements":
    statements.render_statements_page()