import streamlit as st

# Create the tabs and assign them to variables
tab1, tab2, tab3 = st.tabs(["Tab 1 Title", "Tab 2 Title", "Tab 3 Title"])

# Populate the content of each tab using 'with' notation
with tab1:
    st.header("Content for Tab 1")
    st.write("This is some text specific to Tab 1.")
    st.button("Click me in Tab 1")

with tab2:
    st.header("Content for Tab 2")
    st.write("Here you can find information related to Tab 2.")
    st.slider("Select a value", 0, 100)

with tab3:
    st.header("Content for Tab 3")
    st.write("This is the final tab with its own unique content.")
    st.checkbox("Enable feature")