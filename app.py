import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime, timedelta

# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="Radar Pro", layout="wide", initial_sidebar_state="expanded")

# تصميم واجهة المستخدم (CSS) لجمال الألوان
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 رادار الحيتان - الإصدار الاحترافي")

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ إعدادات الرادار")
    ticker = st.text_input("كود السهم (مثال: COMI.CA)", "COMI.CA").upper()
    days = st.slider("فترة التحليل (أيام)", 30, 365, 180)

if ticker:
    try:
        # جلب البيانات بدقة
        df = yf.download(ticker, start=(datetime.now() - timedelta(days=days)), interval="1d")
        
        if not df.empty:
            # حساب المؤشرات
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['SMA_20'] = ta.sma(df['Close'], length=20)
            
            last_price = df['Close'].iloc[-1]
            last_rsi = df['RSI'].iloc[-1]
            change = df['Close'].iloc[-1] - df['Close'].iloc[-2]
            
            # عرض المؤشرات العلوية
            col1, col2, col3 = st.columns(3)
            col1.metric("سعر الإغلاق", f"{last_price:.2f} EGP", f"{change:.2f}")
            col2.metric("مؤشر RSI", f"{last_rsi:.2f}")
            
            if last_rsi < 30:
                col3.success("🎯 إشارة: شراء قوي")
            elif last_rsi > 70:
                col3.error("📢 إشارة: بيع (جني أرباح)")
            else:
                col3.warning("⚖️ إشارة: منطقة حيادية")

            # الرسم البياني الاحترافي
            fig = go.Figure()
            # الشموع اليابانية
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], 
                                        low=df['Low'], close=df['Close'], name='السعر'))
            # خط المتوسط المتحرك
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], line=dict(color='yellow', width=1), name='متوسط 20'))
            
            fig.update_layout(height=500, template="plotly_dark", 
                            xaxis_rangeslider_visible=False,
                            margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig, use_container_width=True)
            
            # جدول البيانات الأخير
            st.subheader("📋 آخر التداولات")
            st.dataframe(df.tail(5).style.highlight_max(axis=0), use_container_width=True)

        else:
            st.error("❌ لم نجد بيانات.. تأكد أنك كتبت الرمز صحيح بالامتداد .CA")
    except Exception as e:
        st.error(f"حدث خطأ فني: {e}")
