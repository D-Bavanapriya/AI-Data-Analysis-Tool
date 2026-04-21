import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io

# ✅ OpenAI setup
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ✅ Page config
st.set_page_config(page_title='AI Data Analyst', page_icon='🤖', layout='wide')
st.title('AI Data Analysis Tool')

# ✅ File upload
uploaded_file = st.file_uploader('Upload CSV file', type=['csv'])

# ✅ Run only if file uploaded
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 📊 Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric('Rows', df.shape[0])
    c2.metric('Columns', df.shape[1])
    c3.metric('Missing', df.isnull().sum().sum())

    # 📋 Preview
    st.dataframe(df.head(10), use_container_width=True)

    # 🔍 Numeric columns
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    # 📊 Chart selection
    chart_type = st.selectbox(
        'Chart type:',
        ['Histogram', 'Box Plot', 'Heatmap', 'Scatter']
    )

    # 📈 Charts
    if chart_type == 'Histogram' and numeric_cols:
        col = st.selectbox('Column:', numeric_cols)
        fig = px.histogram(df, x=col)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == 'Box Plot' and numeric_cols:
        col = st.selectbox('Column:', numeric_cols)
        fig = px.box(df, y=col)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == 'Heatmap' and len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == 'Scatter' and len(numeric_cols) >= 2:
        x_col = st.selectbox('X axis:', numeric_cols, index=0)
        y_col = st.selectbox('Y axis:', numeric_cols, index=1)
        fig = px.scatter(df, x=x_col, y=y_col)
        st.plotly_chart(fig, use_container_width=True)

    # 🤖 AI Auto Analysis
    st.subheader('AI Auto-Analysis')

    if st.button('Generate AI Insights'):
        with st.spinner('Analyzing...'):

            buf = io.StringIO()
            df.info(buf=buf)
            info_text = buf.getvalue()

            prompt = (
                "You are an expert data analyst. "
                "Dataset info: " + info_text +
                " Statistical summary: " + df.describe().to_string() +
                " Give: 1) What the dataset is about "
                "2) Key patterns and trends "
                "3) Anomalies or outliers "
                "4) Three business recommendations "
                "5) Most important columns"
            )

            st.write(ask_ai(prompt))

    # 💬 Custom Question
    custom_q = st.text_area(
        'Ask a custom question:',
        placeholder='What is the average salary by department?'
    )

    if st.button('Ask AI') and custom_q:
        with st.spinner('Processing...'):

            prompt = (
                "Dataset sample: " + df.head(20).to_string() +
                " Columns: " + str(list(df.columns)) +
                " Question: " + custom_q
            )

            st.info(ask_ai(prompt))