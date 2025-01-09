import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/Figure-Friday/main/2024/week-32/irish-pay-gap.csv')
df['Report Link'] = df['Report Link'].apply(lambda x: f'[Report]({x})')
df['Company'] = df.apply(lambda row: f'[{row["Company Name"]}]({row["Company Site"]})', axis=1)
df.rename(columns={'Q1 Men': 'Q1 Male'}, inplace=True)

numeric_columns = [
    'Mean Hourly Gap', 'Median Hourly Gap', 'Mean Bonus Gap', 'Median Bonus Gap', 'Mean Hourly Gap Part Time',
    'Median Hourly Gap Part Time', 'Mean Hourly Gap Part Temp', 'Median Hourly Gap Part Temp', 'Percentage Bonus Paid Female',
    'Percentage Bonus Paid Male', 'Percentage BIK Paid Female', 'Percentage BIK Paid Male', 'Q1 Female', 'Q1 Male', 'Q2 Female',
    'Q2 Male', 'Q3 Female', 'Q3 Male', 'Q4 Female', 'Q4 Male', 'Percentage Employees Female', 'Percentage Employees Male'
]

# Streamlit app layout
st.set_page_config(page_title="Ireland Gender Pay Gap Analysis", layout="wide")
st.title("Ireland Gender Pay Gap Analysis")

# About section
with st.expander("About Gender Pay Gap"):
    st.markdown(
        """
        The gender pay gap does not measure equal pay; instead, it measures the difference between men and
        women's average and median hourly pay. Equal pay, on the other hand, is the legal obligation under the Employment
        Equality Acts that requires employers to give men and women equal pay if they are employed to do equal work.
        
        Note that there is no equivalent reporting requirement in the US. Refer to this [US Department of Labour brief](https://www.dol.gov/sites/dolgov/files/WB/equalpay/WB_issuebrief-undstg-wage-gap-v1.pdf)
        which notes that "regardless of the gender composition of jobs, women tend to be paid less on average than men in the
        same occupation even when working full time."
        """
    )

with st.expander("Data Source"):
    st.markdown(
        """
        Starting from 2022, Gender Pay Gap Reporting is a regulatory requirement that mandates employers in Ireland with
        more than 250 employees to publish information on their gender pay gap.
        
        [Data source](https://paygap.ie/)
        
        [Data source GitHub](https://github.com/zenbuffy/irishGenderPayGap/tree/main)
        """
    )

# Sidebar controls
year = st.sidebar.radio("Select Year", [2023, 2022], index=0)
company = st.sidebar.selectbox("Select a Company", sorted(df["Company Name"].unique()))

# Filter data
df_filtered = df[(df["Company Name"] == company) & (df['Report Year'] == year)].fillna('')
data = df_filtered.iloc[0] if not df_filtered.empty else None

# Display title
if data is not None:
    st.markdown(f"## {data['Report Year']} Gender Pay Gap Report for [{data['Company Name']}]({data['Company Site']})")
    st.markdown("**For more company-specific details, see the report link in the table below.**")

# Display pay gap table
if data is not None:
    st.subheader("Pay Gap Details")
    pay_gap_data = {
        "Category": ["Hourly Pay Gap", "Part Time", "Temporary"],
        "Mean": [data['Mean Hourly Gap'], data['Mean Hourly Gap Part Time'], data['Mean Hourly Gap Part Temp']],
        "Median": [data['Median Hourly Gap'], data['Median Hourly Gap Part Time'], data['Median Hourly Gap Part Temp']]
    }
    st.table(pd.DataFrame(pay_gap_data))

# Proportion bar chart
if data is not None:
    st.subheader("Proportion of Men and Women in Each Pay Quartile")
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    male_percentages = [data[f'{q} Male'] for q in quarters]
    female_percentages = [data[f'{q} Female'] for q in quarters]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=quarters,
        x=male_percentages,
        name='Male',
        orientation='h',
        marker=dict(color='#19A0AA'),
        text=male_percentages,
        textposition='inside',
    ))
    fig.add_trace(go.Bar(
        y=quarters,
        x=female_percentages,
        name='Female',
        orientation='h',
        marker=dict(color='#F15F36'),
        text=female_percentages,
        textposition='inside',
    ))
    fig.update_layout(
        barmode='stack',
        xaxis=dict(title='Percentage', ticksuffix='%'),
        yaxis=dict(title='Quartile'),
        template='plotly_white',
    )
    st.plotly_chart(fig, use_container_width=True)

# Display full dataset
st.subheader("Dataset")
st.dataframe(df)
