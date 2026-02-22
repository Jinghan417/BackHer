# views/welcome_view.py
import streamlit as st

def render_landing_page():
    # 使用容器居中内容
    empty_col, main_col, empty_col2 = st.columns([1, 2, 1])
    
    with main_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("Welcome to BackHer")
        st.subheader("Financial Intelligence for Female Founders")
        st.write("""
            We simplify complex accounting into strategic insights. 
            Connect your data, analyze your health, and pitch with confidence.
        """)
        
        st.divider()
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Get Started", use_container_width=True, type="primary"):
                st.session_state.page_view = "Login"
                st.rerun()
        with col_btn2:
            # 👈 这里改成了通过变量控制点击
            show_more = st.button("Learn More", use_container_width=True)

        # 👈 插入的 Learn More 详情内容
        if show_more:
            st.info("""
            ### Why BackHer? 🚀
            Not everyone has access to the financial knowledge they need, and we're here to bridge that gap.
            
            * **CFO-Level Insights:** Automated analysis of your bank transactions.
            * **AI Strategic Partner:** A specialized Virtual CFO for small businesses.
            * **Investor Readiness:** Key ratios (Burn Rate, EBITDA) calculated instantly.
            """)

def render_login_page():
    st.markdown("### 🔐 Owner's Access Portal")
    st.info("Please enter your personal credentials to manage your businesses.")
    
    with st.container():
        name = st.text_input("Owner Name", placeholder="e.g., Churro")
        password = st.text_input("Password", type="password")
        
        if st.button("Enter Portfolio", use_container_width=True):
            if name and password: # 简化逻辑：只要填了就过
                st.session_state.user_profile["name"] = name
                st.session_state.is_logged_in = True
                st.session_state.page_view = "User_Dashboard"
                st.success(f"Welcome back, {name}!")
                st.rerun()
            else:
                st.error("Please fill in both fields.")