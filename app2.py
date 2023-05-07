
import logging
logging.basicConfig(level=logging.DEBUG)

import pandas as pd
import streamlit as st

import altair as alt
import duckdb

import logging
logging.basicConfig(level=logging.DEBUG)

con = duckdb.connect(database='job.db', read_only=True) 

# Countries
query="""
   SELECT * 
   FROM job
"""
Countries=list(con.execute(query).df().columns)[2:]

st.subheader('Investigation')

col1, col2, col3 = st.columns(3)

with col1:
    query="""
            SELECT 
                 DISTINCT variable
            From job        
            ORDER BY variable       
          """

    kinds=con.execute(query).df()
    kind = st.selectbox('Kind of Statistics',kinds)

with col2: 
    countries = st.multiselect('Countries',Countries)

with col3:
    result_df = con.execute(f"""
        SELECT 
            date, {','.join(countries)}
        FROM Job 
        WHERE variable=?
    """, [kind]).df()

    chart = alt.Chart(result_df).mark_line().encode(
        x='date',
        y=alt.Y(','.join(countries), axis=alt.Axis(title='Value'))
    ).interactive()

    st.write(chart)
