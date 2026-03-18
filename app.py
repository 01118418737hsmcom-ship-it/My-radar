import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# إعداد الواجهة
st.set_page_config(page_title="رادار الحيتان", layout="wide")
st.title("📊 رادار الحيتان - تحليل البورصة المصرية")

# القائمة الجانبية
st.sidebar.header("🕹️ التحكم")
ticker = st.sidebar.text_input("أدخل كود السهم (مثلاً COMI.CA):", "")

# التحقق من وجود مدخلات
if ticker:
    try:
        # جلب البيانات
        data = yf.download(ticker, period="1mo",interval="1d")

        
        if not data.empty:
            # رسم الشموع اليابانية
            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close']
            )])
            fig.update_layout(template="plotly_dark", title=f"تحليل سهم {ticker}")
            st.plotly_chart(fig, use_container_width=True)

            # حساب RSI
            rsi_series = ta.rsi(data['Close'])
            if rsi_series is not None and not rsi_series.empty:
                rsi = rsi_series.iloc[-1]
                st.metric("مؤشر القوة النسبية (RSI)", f"{rsi:.2f}")

                if rsi < 30:
                    st.success("✅ توصية: منطقة شراء (تجميع)")
                elif rsi > 70:
                    st.error("⚠️ توصية: منطقة بيع (تصريف)")
                else:
                    st.warning("⚖️ حالة حيادية")
        else:
            st.error("لم يتم العثور على بيانات. تأكد من إضافة .CA بعد رمز السهم")
    except Exception as e:
        st.error(f"حدث خطأ أثناء جلب البيانات: {e}")
else:
    st.info("👈 أهلاً بك! ابدأ بكتابة رمز السهم في الخانة على اليسار (مثل TMGH.CA)")
