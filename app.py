import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

# MySQL Database Configuration
db_config = {
    'user': 'root',
    'password': 'TM_edu',
    'host': 'localhost',
    'database': 'list_of_schools',
    'port': '3306'
}

# Create a MySQL connection
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

# Query to fetch data from MySQL
query = 'SELECT * FROM your_table_name;'
df = pd.read_sql(query, con=engine)

# Streamlit App
st.title("School Information App")

# Autocomplete Widget
school_code_autocomplete_key = 'school_code_autocomplete'
school_code_autocomplete = st.text_input("School Code:", key=school_code_autocomplete_key, help='Enter school code')

# Autocomplete Suggestions
initial_suggestion = 'Select'
school_code_autocomplete_suggestions_key = 'school_code_autocomplete_suggestions'
school_code_autocomplete_suggestions = st.selectbox("Suggestions:", key=school_code_autocomplete_suggestions_key, options=[initial_suggestion] + df['KOD SEKOLAH'].tolist())

# Search Button
search_button = st.button("Search")

# Clear Button
clear_button = st.button("Clear Results")

# Display Result
result_expander_key = 'result_expander'
with st.expander("Result", expanded=False):  # Set expanded to False initially
    if search_button:
        school_code = school_code_autocomplete if school_code_autocomplete != 'Select' else school_code_autocomplete_suggestions
        result = df[df['KOD SEKOLAH'] == school_code][['KOD SEKOLAH', 'SENARAI SEKOLAH MALAYSIA', 'SEKOLAH INTERIM', 'SEKOLAH VSAT', 'SEKOLAH HIBRID']]

        if result.empty:
            st.warning(f"No information found for School Code: {school_code}")
        else:
            # Display the output as a list
            st.success("Information for School Code {}: ".format(school_code))
            for _, row in result.iterrows():
                st.write("- School Code: {}".format(row['KOD SEKOLAH']))
                st.write("  School Name: {}".format(row['SENARAI SEKOLAH MALAYSIA']))
                st.write("  TM Interim: {}".format(row['SEKOLAH INTERIM']))
                st.write("  VSAT: {}".format(row['SEKOLAH VSAT']))
                st.write("  TM Hybrid: {}".format(row['SEKOLAH HIBRID']))
                st.write("\n")

# Clear Results
if clear_button:
    school_code_autocomplete = ''
    school_code_autocomplete_suggestions = initial_suggestion

    st.warning("Results cleared.")

# Update Suggestions based on Input
entered_text = school_code_autocomplete.upper()
filtered_options = [option for option in df['KOD SEKOLAH'].tolist() if option.startswith(entered_text)]
unique_suggestions_key = 'unique_suggestions_key'  # Add a unique key
school_code_autocomplete_suggestions = st.selectbox("Suggestions:", key=unique_suggestions_key, options=[initial_suggestion] + filtered_options)

# Update Search Bar based on Dropdown Selection
if school_code_autocomplete_suggestions != 'Select':
    school_code_autocomplete = school_code_autocomplete_suggestions

# Display widgets
st.write("### Search Parameters:")
st.write(f"- School Code: {school_code_autocomplete}")
st.write(f"- Suggestions: {school_code_autocomplete_suggestions}")

# Add any other Streamlit components or visualizations as needed
