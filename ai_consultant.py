from google import genai
import streamlit as st

def get_cfo_advice(api_key, stats, biz_profile):
    """
    连接 Gemini 为特定的企业 profile 提供战略建议
    """
    if not api_key:
        return "⚠️ Please enter your Gemini API Key in the sidebar to enable AI insights."
    
    try:
        client = genai.Client(api_key=api_key)
        
        # 更加专业和定制化的 Prompt
        prompt = f"""
        Role: Strategic Virtual CFO for a female-founded business.
        Business Context: {biz_profile['name']} (Industry: {biz_profile['type']})
        
        Current Financial Performance (Last Month):
        - Revenue: ${stats['revenue']:,.2f}
        - Net Profit: ${stats['net_profit']:,.2f}
        - EBITDA: ${stats['ebitda']:,.2f}
        - Cash on Hand: ${stats['cash']:,.2f}
        
        Task: Provide 3 high-impact strategic insights for the founder.
        Focus on:
        1. Burn rate and runway (based on current cash).
        2. Industry-specific margin optimization for {biz_profile['type']}.
        3. One 'Investability' tip to make this business more attractive to VCs or lenders.
        
        [STRICT INSTRUCTION]: 
        1. Start your response with "Dear Business Owner," 
        2. DO NOT use placeholders like [Founder's Name] or [Business Name].
        3. End with "Best regards, \nFrom BackHer, your online CFO"

        Tone: Empathetic, professional, and data-driven. Keep it concise.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ CFO Connection Error: {str(e)}"