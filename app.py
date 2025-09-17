import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("🧠 Natural Language → Chart Generator (Offline)")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    instruction = st.text_input("Enter your chart request (e.g., 'scatter plot of Sales vs Quantity')")

    if st.button("Generate Chart") and instruction:
        # Convert instruction to lowercase for easier matching
        instr = instruction.lower()

        try:
            # Default x and y
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            columns = df.columns.tolist()
            
            x_col = columns[0]  # default x
            y_col = numeric_cols[0] if numeric_cols else columns[1]  # default y
            
            # Try to find column names mentioned in instruction
            for col in columns:
                if col.lower() in instr:
                    x_col = col
                    break
            for col in numeric_cols:
                if col.lower() in instr:
                    y_col = col
                    break

            # Decide chart type
            if "scatter" in instr:
                chart_type = "scatter"
                code = f"df.plot(kind='scatter', x='{x_col}', y='{y_col}')\nplt.title('Scatter Plot of {y_col} vs {x_col}')\nplt.show()"
                df.plot(kind="scatter", x=x_col, y=y_col)
            elif "line" in instr:
                chart_type = "line"
                code = f"df.plot(kind='line', x='{x_col}', y='{y_col}')\nplt.title('Line Plot of {y_col} vs {x_col}')\nplt.show()"
                df.plot(kind="line", x=x_col, y=y_col)
            elif "pie" in instr:
                chart_type = "pie"
                code = f"df.groupby('{x_col}')[\"{y_col}\"].sum().plot(kind='pie', autopct='%1.1f%%')\nplt.title('Pie Chart of {y_col} by {x_col}')\nplt.ylabel('')\nplt.show()"
                df.groupby(x_col)[y_col].sum().plot(kind="pie", autopct="%1.1f%%")
                plt.ylabel('')
            elif "hist" in instr:
                chart_type = "histogram"
                code = f"df['{y_col}'].plot(kind='hist', bins=10)\nplt.title('Histogram of {y_col}')\nplt.show()"
                df[y_col].plot(kind="hist", bins=10)
            elif "stacked" in instr or ("bar" in instr and "stacked" in instr):
                chart_type = "stacked bar"
                # pick first two categorical/numeric columns
                cat_col = x_col
                numeric_col = y_col
                code = f"df.groupby('{cat_col}')['{numeric_col}'].sum().plot(kind='bar', stacked=True)\nplt.title('Stacked Bar Chart of {numeric_col} by {cat_col}')\nplt.show()"
                df.groupby(cat_col)[numeric_col].sum().plot(kind="bar", stacked=True)
            else:
                # default to bar chart
                chart_type = "bar"
                code = f"df.groupby('{x_col}')['{y_col}'].sum().plot(kind='bar')\nplt.title('Bar Chart of {y_col} by {x_col}')\nplt.show()"
                df.groupby(x_col)[y_col].sum().plot(kind="bar")

            # Show code
            st.subheader(f"Generated {chart_type.capitalize()} Code")
            st.code(code, language="python")

            # Show plot
            st.pyplot(plt.gcf())
            plt.clf()

        except Exception as e:
            st.error(f"Error generating chart: {e}")

else:
    st.info("Please upload a CSV to get started.")
