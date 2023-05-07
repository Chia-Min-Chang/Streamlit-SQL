import pandas as pd
import streamlit as st
import altair as alt
import duckdb

con = duckdb.connect(database='job.db', read_only=True) 

# Countries
query="""
   SELECT * 
   FROM job
"""
Countries=list(con.execute(query).df().columns)[2:]

st.subheader('Investigation')

col1, col2 = st.columns(2)

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
    country1 = st.selectbox('Country 1',Countries)
    country2 = st.selectbox('Country 2',Countries)

result_df = con.execute("""
    SELECT 
        *
    FROM Job 
    WHERE variable=?
    """, [kind]).df()

chart1 = alt.Chart(result_df).mark_circle().encode(
    x='date',
    y=alt.Y(country1, title=country1),
    color=alt.value('blue')
).properties(width=500, height=300)

chart2 = alt.Chart(result_df).mark_circle().encode(
    x='date',
    y=alt.Y(country2, title=country2),
    color=alt.value('orange')
).properties(width=500, height=300)

brush = alt.selection_interval(encodings=['x'])

combined_chart = alt.layer(
    chart1, 
    chart2, 
    resolve_scale=alt.ResolveScale(y='independent')
).add_selection(brush).transform_filter(brush)

st.altair_chart(combined_chart, use_container_width=True)
