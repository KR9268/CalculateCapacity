import streamlit as st
import pandas as pd
import sample2

st.set_page_config(layout="wide")

# Input
volume = {
        "A": 6, "B": 7, "C": 2, "D": 1, "E": 5, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0, "L": 0, "M": 0, "N": 0, "O": 0, "P": 0, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0, "W": 0, "X": 0
    }
df = sample2.calculate_cheapest_shipping(volume)

temp_volume = {}
col1, col2 = st.columns([0.3,0.7])
with col1:
    st.title('Input 20FT Qty')
    for key in volume.keys():
        temp_volume[key] = int(st.text_input(key, value=volume[key]))

with col2:
    # Streamlit 애플리케이션 작성
    st.title('Calculated table')
    col2_1, col2_2 = st.columns([0.1,0.9])
    with col2_1:
        if st.button('Calculate'):
            for key in volume.keys():
                temp_volume[key] = temp_volume[key]

            df = sample2.calculate_cheapest_shipping(temp_volume)
    with col2_2:
        st.write(f"#### Total Cost : {df['totalCost'].sum()}")

    st.dataframe(df, width=1500, hide_index=True)
    #st.dataframe(df)  # pandas DataFrame을 Streamlit으로 표시

    # streamlit run C:\Users\user\Downloads\UI.py
    # streamlit run C:\python_source\Calculate_Vessel_Capacity\UI.py