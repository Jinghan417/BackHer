import json
import random
from datetime import datetime, timedelta

def create_pro_bakery_json():
    all_transactions = []
    start_date = datetime(2025, 9, 1)
    
    for day_offset in range(180):
        dt = start_date + timedelta(days=day_offset)
        curr = dt.strftime("%Y-%m-%d")
        
        # --- A. 收入分类生成 ---
        # 1. 零售单 (Retail)
        for _ in range(random.randint(2, 6)):
            all_transactions.append({
                "date": curr, "merchant": "Bakery POS", "amount": float(random.randint(35, 80)),
                "category": "Revenue: Retail", "type": "inflow"
            })
        
        # 2. 定制大单 (Special Orders) - 每周 1-2 次
        if dt.weekday() in [4, 5] and random.random() < 0.4:
            all_transactions.append({
                "date": curr, "merchant": "Invoiced Client", "amount": float(random.randint(200, 500)),
                "category": "Revenue: Special Orders", "type": "inflow"
            })

        # --- B. 支出分类生成 ---
        # 1. 变动成本 (COGS) - Costco 进货
        if dt.weekday() in [1, 4]:
            all_transactions.append({
                "date": curr, "merchant": "Costco", "amount": float(random.randint(150, 350)),
                "category": "COGS: Ingredients", "type": "outflow"
            })

        # 2. 固定支出 (Monthly OPEX)
        if dt.day == 1:
            all_transactions.append({"date": curr, "merchant": "Rent/Storage", "amount": 800.0, "category": "Expense: Rent", "type": "outflow"})
            # 3. 负债还款 (Liability Repayment) - 假设欠了 Costco 信用卡或者器材贷款
            all_transactions.append({"date": curr, "merchant": "SBA Loan Service", "amount": 250.0, "category": "Liability: Loan Repayment", "type": "outflow"})

    with open('plaid_simulator.json', 'w') as f:
        json.dump(all_transactions, f, indent=4)
    print("✅ Professional data with Revenue breakdown and Liabilities generated.")

if __name__ == "__main__":
    create_pro_bakery_json()