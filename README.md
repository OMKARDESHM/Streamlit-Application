# Streamlit Application
A Streamlit application for visualizing data insights from uploaded CSV, Excel, or text files, powered by a FastAPI backend for data processing and analysis

This project is a data analysis web application that allows users to upload CSV or Excel files and instantly get a summary of insights and visualizations using **FastAPI** on the backend and **Streamlit** on the frontend.

## 🚀 Features

- Upload CSV or Excel datasets via a web interface
- Automatically extracts:
  - Number of rows and columns
  - Column names and data types
  - Missing values and unique counts
  - Summary statistics for numeric columns
  - Top frequent values in categorical columns
- Visualizes:
  - Missing values heatmap
  - Histograms and boxplots
  - Correlation matrix and heatmap
  - Bar plots for categorical variables
  - Pairplot for small numeric datasets
- Clean, responsive UI with Streamlit

---

## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (for data processing and visualization)
- **Frontend**: [Streamlit](https://streamlit.io/) (for interactive UI)
- **Data Processing**: `pandas`, `matplotlib`, `seaborn`
- **Communication**: `requests` (Streamlit ↔ FastAPI)

---

## 📦 Installation

1.Clone the Repository
```bash
git clone https://github.com/OMKARDESHM/Streamlit-Application.git
cd data-insights-app

2. Create a Virtual Environment (optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies

fastapi
uvicorn
pandas
matplotlib
seaborn
openpyxl
streamlit
requests

4.Running the App

Step 1: Start the FastAPI Backend
uvicorn backend:app --reload

Step 2: Launch the Streamlit Frontend
streamlit run main.py

Then go to http://localhost:8501 in your browser.


5.Project Structure

.
├── backend.py          # FastAPI backend for data processing
├── main.py             # Streamlit frontend
├── requirements.txt    # Python dependencies
└── README.md           # This file
