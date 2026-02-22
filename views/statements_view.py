import streamlit as st
import pandas as pd

def render_statements_page():
    st.title("📊 Financial Statements")
    
    if 'months_data' not in st.session_state or not st.session_state.months_data:
        st.warning("Please link your bank account first.")
        return

    data = st.session_state.months_data
    available_months = list(data.keys())

    # --- 导航控制 ---
    col1, col2 = st.columns([1, 1])
    with col1:
        view_type = st.radio("View Type", ["Single Month", "Summary View"], horizontal=True)
    with col2:
        if view_type == "Single Month":
            selected_period = st.selectbox("Select Month", available_months, index=len(available_months)-1)
            target_months = [selected_period]
        else:
            n = st.selectbox("Duration", [3, 6], format_func=lambda x: f"Last {x} Months")
            target_months = available_months[-n:]

    # --- 数据对齐逻辑 ---
    try:
        def get_statement(key):
            if len(target_months) == 1:
                return data[target_months[0]]['statements'][key]
            # 聚合：将多个月的 Amount 累加
            dfs = [data[m]['statements'][key].set_index("Item" if key == 'p_and_l' else "Activity") for m in target_months]
            combined = pd.concat(dfs, axis=1).sum(axis=1).reset_index()
    
            # 这一行最关键：手动重新命名，不依赖 pandas 自动生成
            current_col = "Item" if key == 'p_and_l' else "Activity"
            combined.columns = [current_col, "Amount"]
            return combined
        

        display_pl = get_statement('p_and_l')
        display_cf = get_statement('cash_flow')
        # Balance Sheet 永远只看最近一个月的快照
        display_bs = data[target_months[-1]]['statements']['balance_sheet']

    except Exception as e:
        st.error(f"Display Error: {e}")
        return

    # --- 渲染标签页 ---
    t1, t2, t3, t4 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow", "Ledger"])
    fmt = {"Amount": "${:,.2f}"}

    with t1:
        st.table(display_pl.set_index("Item").style.format(fmt))
    with t2:
        st.table(display_bs.set_index("Category").style.format(fmt))
    with t3:
        st.table(display_cf.set_index("Activity").style.format(fmt))
    with t4:
        # 显示原始流水
        combined_ledger = pd.concat([data[m]['ledger'] for m in target_months])
        st.dataframe(combined_ledger.sort_values('date', ascending=False), use_container_width=True)