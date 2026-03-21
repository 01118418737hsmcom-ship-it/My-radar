import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go

# إعدادات الواجهة السيادية
st.set_page_config(page_title="ثروة رادار V1.0", layout="wide")

# محرك البيانات (EGX)
@st.cache_data(ttl=60)
def get_stock_data(ticker):
    data = yf.download(ticker, period="1mo", interval="15m")
    return data

# قائمة الأسهم المفضلة لديك
fav_stocks = ["CIB.CA", "ABUK.CA", "TMGH.CA", "FWRY.CA", "SWDY.CA"]

# التبويبات (تنسيق بسيط للموبايل)
tab_radar, tab_sniper, tab_vault = st.tabs(["🛰️ الرادار", "🎯 القناص", "💰 الخزنة"])

# 1. تبويب الرادار
with tab_radar:
    st.title("📡 رادار النبض اللحظي")
    cols = st.columns(len(fav_stocks))
    for i, stock in enumerate(fav_stocks):
        with cols[i]:
            try:
                df = get_stock_data(stock)
                last_p = df['Close'].iloc[-1]
                st.metric(stock.replace('.CA',''), f"{last_p:.2f} ج.م")
            except:
                st.error(f"خطأ في {stock}")

# 2. تبويب القناص (التحليل الاحترافي)
with tab_sniper:
    st.title("🎯 تحليل القناص (الشموع)")
    s_stock = st.selectbox("اختر السهم للتحليل:", fav_stocks)
    df_s = get_stock_data(s_stock)
    
    # رسم الشموع بذيولها
    fig = go.Figure(data=[go.Candlestick(
        x=df_s.index, 
        open=df_s['Open'], 
        high=df_s['High'], 
        low=df_s['Low'], 
        close=df_s['Close'],
        increasing_line_color='#00ff00', 
        decreasing_line_color='#ff4b4b'
    )])
    
    fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.info("🤖 الـ AI يراقب الذيول والبارات الآن..")

# 3. تبويب الخزنة (إدارة الـ 500 جنيه)
with tab_vault:
    st.title("💰 إدارة الـ 500 جنيه")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🧮 حاسبة المتوسط")
        old_price = st.number_input("سعر الشراء القديم:", value=0.0)
        old_qty = st.number_input("الكمية القديمة:", value=0)
        new_inv = st.number_input("مبلغ الاستثمار (ج.م):", value=500)
    
    with col2:
        st.subheader("📈 التقرير")
        st.write("أدخل البيانات لحساب التعديل السعري فوراً.")
