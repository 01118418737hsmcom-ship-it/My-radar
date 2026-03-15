import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# إعداد الواجهة العربية
st.set_page_config(page_title="رادار الحيتان", layout="wide")
st.markdown("""<style>html, body, [data-testid="stSidebar"], .main { direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }</style>""", unsafe_allow_html=True)

st.title("📊 رادار الحيتان - تحليل البورصة الذكي")

# القائمة الجانبية
st.sidebar.header("🕹️ التحكم")
ticker = st.sidebar.text_input("أدخل كود السهم (مثلاً COMI.CA):", "COMI.CA")

# جلب البيانات والتحليل
try:
    data = yf.download(ticker, period="6mo")
    if not data.empty:
        # رسم الشموع اليابانية
        fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
        fig.update_layout(template="plotly_dark", title=f"تحليل سهم {ticker}")
        st.plotly_chart(fig, use_container_width=True)
        
        # مؤشر RSI بسيط
        rsi = ta.rsi(data['Close']).iloc[-1]
        st.metric("مؤشر القوة النسبية (RSI)", f"{rsi:.2f}")
        
        if rsi < 30: st.success("✅ توصية AI: منطقة شراء (تجميع)")
        elif rsi > 70: st.error("⚠️ توصية AI: منطقة بيع (تصريف)")
        else: st.warning("⚖️ توصية AI: منطقة حيادية (احتفاظ)")
    else:
        st.error("لم يتم العثور على بيانات لهذا السهم.")
except Exception as e:
    st.error(f"حدث خطأ: {e}")
