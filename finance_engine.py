import pandas as pd
import json

def process_simulated_plaid_data(json_file):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # 统一月份格式
        df['month_year'] = df['date'].dt.strftime('%B %Y')
        months = df['month_year'].unique()
        
        monthly_reports = {}
        # 初始财务状态
        running_cash = 15000.0
        fixed_assets = 5000.0
        total_debt = 3000.0 
        cum_dep = 0

        for m in months:
            m_df = df[df['month_year'] == m]
            
            # --- 1. 收入拆解 (修正逻辑：从 description 字段匹配) ---
            # 根据截图，category 只是 "Revenue"，所以要在 description 里找关键词
            rev_mask = m_df['category'].str.contains("Revenue", na=False)
            
            # 匹配 Retail 和 Custom (对应你生成器里的内容)
            retail_rev = float(m_df[rev_mask & m_df['description'].str.contains("Retail", na=False)]['amount'].sum())
            special_rev = float(m_df[rev_mask & m_df['description'].str.contains("Custom|Special", na=False)]['amount'].sum())
            total_rev = retail_rev + special_rev
            
            # --- 2. 支出拆解 (确保使用 abs() 转为正数方便计算) ---
            cogs = abs(float(m_df[m_df['category'].str.contains("COGS", na=False)]['amount'].sum()))
            opex = abs(float(m_df[m_df['category'].str.contains("Expense|Rent", na=False)]['amount'].sum()))
            repayment = abs(float(m_df[m_df['category'].str.contains("Liability", na=False)]['amount'].sum()))
            
            # --- 3. 财务计算 ---
            gross_profit = total_rev - cogs
            dep = 100.0  # 每月固定折旧
            cum_dep += dep
            ebitda = total_rev - cogs - opex # 计算 EBITDA 防止 home_view 报错
            net_income = ebitda - dep
            
            # --- 4. 现金与负债变动 ---
            total_debt -= repayment
            monthly_cash_change = total_rev - cogs - opex - repayment
            running_cash += monthly_cash_change

            # --- 5. 构建三张报表 (DataFrame) ---
            pl_df = pd.DataFrame({
                "Item": ["Retail Revenue", "Special Orders", "Total Revenue", "COGS (Materials)", "Gross Profit", "Operating Expenses", "Depreciation", "Net Income"],
                "Amount": [retail_rev, special_rev, total_rev, -cogs, gross_profit, -opex, -dep, net_income]
            })

            bs_df = pd.DataFrame({
                "Category": ["Cash (Assets)", "Equipment (Assets)", "Accum. Depreciation", "Debt (Liabilities)", "Equity"],
                "Amount": [running_cash, fixed_assets, -cum_dep, -total_debt, -(running_cash + fixed_assets - cum_dep - total_debt)]
            })

            cf_df = pd.DataFrame({
                "Activity": ["Cash In (Customers)", "Cash Out (Materials)", "Cash Out (Rent/Tools)", "Loan Repayment", "Net Cash Change"],
                "Amount": [total_rev, -cogs, -opex, -repayment, monthly_cash_change]
            })
            cf_df.columns = cf_df.columns.str.strip()

            # --- 6. 封装数据 (确保包含所有 home_view 需要的 key) ---
            monthly_reports[m] = {
                "ledger": m_df,
                "stats": {
                    "revenue": total_rev, 
                    "net_profit": net_income, 
                    "ebitda": ebitda,  # 👈 修复了这里，不会再报 KeyError 了
                    "cash": running_cash, 
                    "margin": (net_income/total_rev*100) if total_rev>0 else 0
                },
                "statements": {
                    "p_and_l": pl_df,
                    "balance_sheet": bs_df,
                    "cash_flow": cf_df
                }
            }
        return monthly_reports
    except Exception as e:
        print(f"Engine Error: {e}")
        return {}