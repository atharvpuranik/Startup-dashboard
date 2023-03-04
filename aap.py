import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Startup Analysis')
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():

    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.metric('Avg',str(round(avg_funding)) + ' Cr')

    with col4:
        st.metric('Funded Startups',num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig8, ax8 = plt.subplots()
    ax8.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig8)

def load_startup_deatils(startup):
    st.title(startup)
    # last 5 investments
    Last_df = df[df['startup'].str.contains(startup)].head()[
        ['date', 'startup', 'vertical', 'city', 'round','investors', 'amount']]
    st.subheader('Startup details')
    st.dataframe(Last_df)

    col1, col2 = st.columns(2)

    # biggest Investments
    with col1:
        big_series_bar = df[df['startup'].str.contains(startup)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('Biggest Investments')

        figx, axy = plt.subplots()
        axy.bar(big_series_bar.index, big_series_bar.values)
        st.pyplot(figx)

        city_series_pie = df[df['startup'].str.contains(startup)].groupby('city')['amount'].sum()

        st.subheader('Location ')
        fig7, ax7 = plt.subplots()
        ax7.pie(city_series_pie, labels=city_series_pie.index, autopct='%0.01f%%')

        st.pyplot(fig7)

    with col2:
        big_series_pie = df[df['startup'].str.contains(startup)].groupby('vertical')['amount'].sum()

        st.subheader('Industry')
        fig0, ax0 = plt.subplots()
        ax0.pie(big_series_pie, labels=big_series_pie.index, autopct='%0.01f%%')

        st.pyplot(fig0)

        round_series_pie1 = df[df['startup'].str.contains(startup)].groupby('round')['amount'].sum()

        st.subheader('Stages Invested ')
        fig11, ax11 = plt.subplots()
        ax11.pie(round_series_pie1, labels=round_series_pie1.index, autopct='%0.01f%%')

        st.pyplot(fig11)

    # st.subheader('Similar startups')



def load_investor_details(investor):

    st.title(investor)
    #last 5 investments
    Last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical','city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(Last5_df)

    col1, col2 = st.columns(2)

    #biggest Investments
    with col1:
        big_series_bar = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')

        fig, ax = plt.subplots()
        ax.bar(big_series_bar.index, big_series_bar.values)
        st.pyplot(fig)

        city_series_pie = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()

        st.subheader('Cities Invested in ')
        fig2, ax2 = plt.subplots()
        ax2.pie(city_series_pie, labels=city_series_pie.index,autopct='%0.01f%%')

        st.pyplot(fig2)

    with col2 :
        big_series_pie = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors Invested in ')
        fig1, ax1 = plt.subplots()
        ax1.pie(big_series_pie,labels=big_series_pie.index,autopct='%0.01f%%')

        st.pyplot(fig1)

        round_series_pie = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()

        st.subheader('Stages Invested at')
        fig3, ax3 = plt.subplots()
        ax3.pie(round_series_pie, labels=round_series_pie.index,autopct='%0.01f%%')

        st.pyplot(fig3)

    df['year'] =df['date'].dt.year
    yoy_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('Year on Year Investments')
    fig4, ax4 = plt.subplots()
    ax4.plot(yoy_series.index,yoy_series.values)

    st.pyplot(fig4)

# st.dataframe(df)
st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Startup':
    selected_startup=st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    butn = st.sidebar.button('Find startup details')
    st.title("Startup Analysis")
    if butn:
        load_startup_deatils(selected_startup)
else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    botn2 = st.sidebar.button('Find Investor details')
    if botn2:
        load_investor_details(selected_investor)