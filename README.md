# AI-Data-Analysis-Tool
An interactive data analysis web app that allows users to upload datasets, explore them visually, and generate AI-driven insights using natural language. Built using Streamlit, Pandas, and OpenAI.

# Features
* Upload CSV datasets
* Dataset overview (rows, columns, missing values)
* Interactive visualizations:
    - Histogram
    - Box Plot
    - Heatmap
* Scatter Plot
* AI-powered automatic insights
* Ask custom questions about your data
  
# Tech Stack
- Frontend: Streamlit
- Data Processing: Pandas, NumPy
- Visualization: Plotly
- AI Integration: OpenAI

# Setup & Installation
1. Clone the repository
    git clone <your-repo-link>
    cd yt_app
2. Create virtual environment
    python -m venv .venv
    .venv\Scripts\activate
3. Install dependencies
    pip install -r requirements.txt
4. Add API key
    Create .streamlit/secrets.toml
    OPENAI_API_KEY = "your_api_key_here"
5. Run the app
    streamlit run app.py
