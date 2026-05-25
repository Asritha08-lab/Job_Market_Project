import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Universal Data Analyzer",
    layout="wide"
)

# ---------------- TITLE ---------------- #

st.title("📊 Universal Data Analyzer")

st.write(
    "Upload any CSV file and automatically analyze the dataset."
)

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.file_uploader(
    "📁 Upload CSV File",
    type=["csv"]
)

# ---------------- IF FILE EXISTS ---------------- #

if uploaded_file is not None:

    # ---------------- READ DATASET ---------------- #

    df = pd.read_csv(uploaded_file)

    # ---------------- DATA CLEANING ---------------- #

    cleaning_steps = []

    # Remove unnamed columns
    unnamed_cols = [
        col for col in df.columns
        if "unnamed" in col.lower()
    ]

    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)

        cleaning_steps.append(
            f"Removed unnamed columns: {', '.join(unnamed_cols)}"
        )

    # Remove duplicate rows
    duplicates = df.duplicated().sum()

    if duplicates > 0:

        df.drop_duplicates(inplace=True)

        cleaning_steps.append(
            f"Removed {duplicates} duplicate rows"
        )

    # Missing values
    missing = df.isnull().sum().sum()

    cleaning_steps.append(
        f"Total missing values found: {missing}"
    )

    # ---------------- METRICS ---------------- #

    st.subheader("📌 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", missing)

    # ---------------- TABS ---------------- #

    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Preview",
        "📊 Statistics",
        "📈 Visualization",
        "🔥 Correlation"
    ])

    # ---------------- TAB 1 ---------------- #

    with tab1:

        st.subheader("🧹 Data Cleaning Summary")

        for step in cleaning_steps:
            st.success(step)

        st.subheader("📄 Dataset Preview")

        st.dataframe(df.head(20))

        st.subheader("📌 Data Types")

        st.write(df.dtypes)

        st.subheader("❌ Missing Values")

        st.write(df.isnull().sum())

    # ---------------- TAB 2 ---------------- #

    with tab2:

        st.subheader("📊 Statistical Summary")

        st.write(df.describe())

    # ---------------- TAB 3 ---------------- #

    with tab3:

        st.subheader("📈 Smart Visualization")

        # Numeric columns excluding unnamed
        numeric_columns = [
            col for col in df.select_dtypes(include=['number']).columns
            if "unnamed" not in col.lower()
        ]

        if len(numeric_columns) > 0:

            selected_column = st.selectbox(
                "Select Numeric Column",
                numeric_columns
            )

            fig, ax = plt.subplots(figsize=(8, 5))

            # Smart chart selection
            if df[selected_column].nunique() < 10:

                df[selected_column].value_counts().plot(
                    kind='bar',
                    ax=ax
                )

                ax.set_ylabel("Count")

            else:

                df[selected_column].hist(ax=ax)

                ax.set_ylabel("Frequency")

            ax.set_title(
                f"Distribution of {selected_column}"
            )

            st.pyplot(fig)

        else:

            st.warning("No numeric columns found.")

    # ---------------- TAB 4 ---------------- #

    with tab4:

        st.subheader("🔥 Correlation Heatmap")

        correlation = df.select_dtypes(
            include=['number']
        ).corr()

        fig2, ax2 = plt.subplots(figsize=(10, 6))

        cax = ax2.matshow(
            correlation,
            cmap='coolwarm'
        )

        plt.xticks(
            range(len(correlation.columns)),
            correlation.columns,
            rotation=90
        )

        plt.yticks(
            range(len(correlation.columns)),
            correlation.columns
        )

        fig2.colorbar(cax)

        st.pyplot(fig2)

    # ---------------- DOWNLOAD BUTTON ---------------- #

    st.subheader("📥 Download Dataset")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='processed_data.csv',
        mime='text/csv'
    )

# ---------------- NO FILE ---------------- #

else:

    st.info(
        "Please upload a CSV file to begin analysis."
    )