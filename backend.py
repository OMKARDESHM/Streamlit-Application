from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io

app = FastAPI()

def generate_base64_image(fig):
    """Converts a matplotlib figure to a base64 string."""
    img_io = io.BytesIO()
    fig.savefig(img_io, format='png')
    img_io.seek(0)
    return base64.b64encode(img_io.getvalue()).decode('utf-8')

@app.post("/process_uploaded_file/")
async def process_uploaded_file(file: UploadFile = File(...)):
    try:
        # Read the file
        contents = await file.read()
        file_type = file.content_type
        print(f"File received: {file.filename}, File type: {file_type}")

        # Process CSV or Excel files
        if file_type == "text/csv":
            df = pd.read_csv(io.BytesIO(contents))
        elif file_type in ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        # Enhanced Insights
        insights = {
            "num_rows": df.shape[0],
            "num_columns": df.shape[1],
            "column_names": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "unique_values": df.nunique().to_dict(),
        }

        # Summary statistics
        insights["numeric_summary"] = df.describe().to_dict()

        # Top frequent values for categorical columns
        top_freq = {}
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            top_freq[col] = df[col].value_counts().head(5).to_dict()
        insights["top_frequent_categorical_values"] = top_freq

        # Correlation matrix for numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            insights["correlation_matrix"] = numeric_df.corr().round(2).to_dict()

        # Create visualizations
        visualizations = {}

        # Missing Values Heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
        visualizations["missing_values_heatmap"] = generate_base64_image(plt)
        plt.close()

        # Histogram of numeric columns
        plt.figure(figsize=(10, 6))
        df.hist(bins=15, figsize=(15, 10))
        visualizations["histogram"] = generate_base64_image(plt)
        plt.close()

        # Boxplot for numeric columns
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=numeric_df)
        visualizations["boxplot"] = generate_base64_image(plt)
        plt.close()

        # Correlation Heatmap
        if not numeric_df.empty:
            plt.figure(figsize=(10, 6))
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
            visualizations["correlation_heatmap"] = generate_base64_image(plt)
            plt.close()

        # Bar plots for each categorical column
        for col in cat_cols:
            plt.figure(figsize=(10, 6))
            df[col].value_counts().plot(kind='bar')
            plt.title(f"Bar Plot of {col}")
            visualizations[f"{col}_barplot"] = generate_base64_image(plt)
            plt.close()

        # Pairplot if dataset is small
        if numeric_df.shape[1] <= 5 and df.shape[0] <= 100:
            sns_plot = sns.pairplot(numeric_df)
            img_io = io.BytesIO()
            sns_plot.savefig(img_io, format='png')
            img_io.seek(0)
            visualizations["pairplot"] = base64.b64encode(img_io.getvalue()).decode('utf-8')
            plt.close('all')

        return JSONResponse(content={"insights": insights, "visualizations": visualizations})

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing the file: {e}")