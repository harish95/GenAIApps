from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import sqlite3
import google.generativeai as genai

## Configure GenAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load google gemini model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([prompt[0], question])
    return response.text

## Fucntion to retrieve query from the sql db
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    print("Executing SQL:", sql)
    try:
        cur.execute(sql)
    except Exception as e:
        print("Error executing SQL:", e)
        return None
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

def main():
    st.set_page_config(page_title="Text2SQL Query")
    st.header("Text2SQL Query")

    input = st.text_input("Input: ", key="input")
    submit = st.button("Ask the question")

    # Prompt for gemini
    prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - STUDENT (NAME VARCHAR(25), CLASS VARCHAR(25),
    SECTION VARCHAR(25), MARKS INT) \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """
]
    if submit:
        response = get_gemini_response(input, prompt)
        print("Response: ", response)
        query = response
        answer = read_sql_query(query, "student.db")
        st.subheader("The SQL Query is:")
        st.write(response)
        st.subheader("The Output is:")
        st.write(answer)
        st.write("The above output is in the form of a list, where each element is a tuple representing a row from the database.")


if __name__ == "__main__":
    main()
