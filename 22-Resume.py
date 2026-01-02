import streamlit as st
import pandas as pd
import sqlite3
import re

# Have page configuration above everything, even session state
st.set_page_config(page_title='Resume', layout='wide')

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@st.cache_resource
def get_connection():
    return sqlite3.connect('contacts.db', check_same_thread=False)

# conn = sqlite3.connect('contacts.db')
conn = get_connection()
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    phone TEXT,
    linkedin TEXT,
    discord TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

st.title('Kirolous (Kiro) Shenouda')
st.subheader('Data Consultant')

st.sidebar.title('Page Navigation')
section = st.sidebar.radio('Go to', ['About', 'Experience', 'Skills', 'Education', 'Contact', 'Admin'])

skills = {
    'Streamlit': 0.9,
    'SQL': 0.9,
    'Data Visualization (Tableau, Power BI)': 0.8,
    'Snowflake': 0.8,
    'Matillion': 0.7
}

if section == 'About':
    st.markdown(f'''
    Experienced data consultant with strong skills in analytics
    and visualization. Passionate about turning raw data into
    meaningful facts and actionable insights.

    Use the sidebar on the left to navigate across the different pages.
    ''')

elif section == 'Skills':
    st.header('Skills Overview')
    for skill, level in skills.items():
        st.write(f'{skill}')
        st.progress(level)
    df_skills = pd.DataFrame({
        'Skill': list(skills.keys()),
        'Proficiency': list(skills.values())
    })
    st.bar_chart(df_skills.set_index('Skill'))

elif section == 'Experience':
    st.header('Work Experience')
    with st.expander('Data Consultant | SDG Group | July 2023'):
        st.markdown('''
- Gather, ingest, and analyze data from over 500 tables from over 30 sources from a client to a data warehouse in
Snowflake through Matillion, and implement data governance policies and role assignments in Microsoft Purview
- Used Power BI to recreate 10 public and internal dashboards from Tableau, and ran consistent working sessions
with stakeholders to better understand their requirements and preferences, and solve any issues
- Collaborate with clients to understand business requirements and provide recommendations for data ingestion,
validation, and reporting
        ''')
    with st.expander('Data Analytics Intern | Horizon Blue Cross Blue Shield | Summer 2022'):
        st.markdown('''
- Used RStudio Workbench and SQL to clean and organize healthcare data from a data lake into multiple tables for
a medical company client
- Collaborated with 20 fellow interns to present our analysis and research on Horizon’s workforce by generation
        ''')
    with st.expander('Research and Data Analyst Intern | Davigate | December 2020 - January 2021'): 
        st.markdown('''
- Researched, populated, and analyzed data on sponsoring schools and companies as well as immigration in order to
create a website that provides information on companies that sponsor international students
- Developed skills to work with the designated workflow tools, particularly Airtable for business, strategy, and
efficient and effective communication
        ''')
    with st.expander('HEOP Math Tutor | Hamilton College | Summer 2020 & 2021'):
        st.markdown('''
- Assisted the math professor in the tutorial and developmental instruction to instill students’ confidence in the class
- Provided about 40 students assistance with assignments to ensure their success in the class
- Served as a mentor for the students, offering them advice on time management, socializing, and college in general
        ''')

elif section == 'Education':
    st.header('Education')
    st.write('B.A in Economics | [Hamilton College](https://www.hamilton.edu) | May 2023')

elif section == 'Contact':
    st.header('Get in touch')
    with st.form('contact_form'):
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input('Email *')
            phone = st.text_input('Phone Number')
        with col2:
            linkedin = st.text_input('LinkedIn URL')
            discord = st.text_input('Discord Name')
        message = st.text_area('Message')
        submitted = st.form_submit_button('Send')
        # if submitted and not st.session_state.submitted:
        if submitted:
            # st.session_state.submitted = True
            if not valid_email(email):
                st.warning('Please enter a valid email address')
                st.session_state.submitted = False
            else:
                cursor.execute('''
                    INSERT INTO contacts (email, phone, linkedin, discord, message)
                    VALUES (?, ?, ?, ?, ?)
                ''', (email, phone, linkedin, discord, message))
                conn.commit()
                st.success("Thanks for reaching out, I'll be in touch!")
                st.session_state.submitted = True

elif section == 'Admin':
    st.header('Contact Submissions')
    password = st.text_input('Admin Password *', type='password')
    if password == st.secrets['ADMIN_PASSWORD']:
        cursor.execute('SELECT * FROM contacts ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        if rows:
            df_contacts = pd.DataFrame(
                rows,
                columns=['ID', 'Email', 'Phone', 'LinkedIn', 'Discord', 'Message', 'Timestamp']
            )
            st.metric('Total Submissions', len(df_contacts))
            st.dataframe(df_contacts, use_container_width=True)
        else:
            st.info('No contact submissions yet')
    elif password: # != st.secrets['ADMIN_PASSWORD'] and password != '':
        st.error('Unauthorized Access')

st.divider()
st.caption("Kiro Shenouda's Resume | Updated Jan 1, 2025 | Created with Streamlit")
# conn.close()