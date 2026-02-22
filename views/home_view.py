import streamlit as st
import pandas as pd
import ai_consultant as ai

def render_user_dashboard():
    st.title(f"👋 Hi, {st.session_state.user_profile['name']}")
    st.write("Welcome back to your financial portfolio. Select a business to manage or create a new one.")
    st.divider()
    
    col_list, col_add = st.columns([2, 1])
    with col_list:
        st.subheader("Your Business List")
        if not st.session_state.businesses:
            st.info("You haven't added any businesses yet. Start by creating your first profile!")
        else:
            for idx, biz in enumerate(st.session_state.businesses):
                with st.container():
                    st.markdown(f"""
                    <div style="border:1px solid #FADADD; padding:20px; border-radius:15px; background-color:white; margin-bottom:10px">
                        <h4>🏢 {biz['name']}</h4>
                        <p>Industry: {biz['type']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Manage {biz['name']}", key=f"biz_{idx}"):
                        st.session_state.current_biz_idx = idx
                        st.session_state.page_view = "Home"
                        st.rerun()

    with col_add:
        st.markdown("### ➕ Operations")
        if st.button("Create New Business Profile", use_container_width=True, type="primary"):
            st.session_state.page_view = "Welcome_Step_1" 
            st.rerun()

def render_business_overview():
    # 1. 基础数据准备
    biz = st.session_state.businesses[st.session_state.current_biz_idx]
    
    if st.button("⬅️ Back to Portfolio"):
        st.session_state.page_view = "User_Dashboard"
        st.rerun()
        
    st.title(f"📊 {biz['name']} | Overview Hub")
    
    if not st.session_state.get('months_data'):
        st.warning("🚨 No financial data detected. Please use the sidebar to 'Link Bank via Plaid'.")
        return

    data = st.session_state.months_data
    months = list(data.keys())

    # 2. 全局趋势图
    st.subheader("📈 Financial Performance Trend")
    trend_df = pd.DataFrame({
        "Revenue": [data[m]['stats']['revenue'] for m in months],
        "Net Income": [data[m]['stats']['net_profit'] for m in months]
    }, index=months)
    st.line_chart(trend_df)

    st.divider()

    # 3. 月份选择与动态 KPI
    col_select, _ = st.columns([1, 2])
    with col_select:
        selected_m = st.selectbox("📅 Select Month for Detailed Analysis", months, index=len(months)-1)

    stats = data[selected_m]['stats']
    
    st.subheader(f"🎯 KPI Breakdown for {selected_m}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue", f"${stats['revenue']:,.2f}")
    col2.metric("Net Profit", f"${stats['net_profit']:,.2f}")
    col3.metric("Net Margin", f"{stats.get('margin', 0):.1f}%")

    # 4. 投资人比率卡片 (使用你之前的自定义 CSS 样式)
    st.write("#### 🎯 Investor Ratios")
    r_col1, r_col2, r_col3 = st.columns(3)
    r_col1.markdown(f"<div class='metric-card'><small>CASH POSITION</small><h2>${stats['cash']:,.2f}</h2></div>", unsafe_allow_html=True)
    r_col2.markdown(f"<div class='metric-card'><small>EBITDA</small><h2>${stats['ebitda']:,.2f}</h2></div>", unsafe_allow_html=True)
    r_col3.markdown(f"<div class='metric-card'><small>BURN RATE (EST.)</small><h2>${(stats['revenue'] - stats['net_profit']):,.2f}</h2></div>", unsafe_allow_html=True)

    # 5. AI 战略分析
    st.divider()
    st.subheader(f"🩷 BackHer AI Strategy Room ({selected_m})")
    
    # 优先从 session_state 获取 api_key
    api_key = st.session_state.get('api_key', "")
    
    if not api_key:
        st.info("💡 Please enter your Gemini API Key in the sidebar to enable AI insights.")
    else:
        if st.button(f"Generate AI Insights for {selected_m}", type="primary"):
            with st.spinner("Analyzing business DNA..."):
                advice = ai.get_cfo_advice(api_key, stats, biz)
                st.markdown(f"""
                <div style="background-color:#F0F2F6; padding:20px; border-radius:15px; border-left: 5px solid #0747A6">
                    {advice}
                </div>
                """, unsafe_allow_html=True)