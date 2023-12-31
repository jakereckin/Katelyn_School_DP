import pandas as pd
import sqlite3 as sql
import os
import smtplib
import ssl 
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

def get_students(r_1_file, r_2_file):
    r_1 = pd.read_csv(r_1_file, index_col=False)
    r_2 = pd.read_csv(r_2_file, index_col=False)
    r_1['HOMEROOM'] = 'Hetrick'
    r_2['HOMEROOM'] = 'Morgan'
    full_students = pd.concat([r_1, r_2])
    full_students['NAME'] = full_students['First Name'] + ' ' + full_students['Last Name']
    insert = list(list(zip(full_students['NAME'], full_students['HOMEROOM'])))
    return full_students, insert

def create_db():
    if os.path.exists(r'C:\Users\Jake\Documents\GitHub\Katelyn_School_DP'):
        conn = sql.connect(r'C:\Users\Jake\Documents\GitHub\Katelyn_School_DP\kmo13.db', check_same_thread=False)
    else:
        conn = sql.connect('kmo13.db', check_same_thread=False)
    return conn

def close_db(conn):
    conn.close()
    return None

def create_student(conn):
    cursor = conn.cursor()
    CREATE = """ CREATE TABLE IF NOT EXISTS STUDENT (
        NAME VARCHAR(255) NOT NULL,
        HOMEROOM VARCHAR(25) NOT NULL
    )"""
    cursor.execute(CREATE)
    conn.commit()
    cursor.close()
    return None

def create_hw(conn):
    cursor = conn.cursor()
    CREATE = """ CREATE TABLE IF NOT EXISTS HW (
        NAME VARCHAR(255) NOT NULL,
        HW_DATE VARCHAR(25) NOT NULL,
        HW_DONE VARCHAR(25) NOT NULL
    )"""
    cursor.execute(CREATE)
    conn.commit()
    cursor.close()
    return None

def drop_hw(conn):
    cursor = conn.cursor()
    DROP = """ 
    DROP TABLE HW;
    """
    cursor.execute(DROP)
    conn.commit()
    cursor.close()
    return None

def drop_student(conn):
    cursor = conn.cursor()
    DROP = """ 
    DROP TABLE STUDENT;
    """
    cursor.execute(DROP)
    conn.commit()
    cursor.close()
    return None

def insert_student(conn, data):
    cursor = conn.cursor()
    INSERT_STUDENT = """ INSERT INTO STUDENT VALUES (?, ?)"""
    cursor.executemany(INSERT_STUDENT, data)
    conn.commit()
    cursor.close()
    return None

def insert_hw(conn, data):
    cursor = conn.cursor()
    INSERT_HW = """ INSERT INTO HW (NAME, HW_DATE, HW_DONE) VALUES(?, ?, ?) """
    cursor.execute(INSERT_HW, data)
    conn.commit()
    cursor.close()
    return None

def select_students(conn):
    SELECT = "SELECT NAME FROM STUDENT"
    df = pd.read_sql_query(SELECT, conn)
    return df

def select_students_morgan(conn):
    SELECT_MORGAN = """
    SELECT STUDENT.NAME
       FROM STUDENT 
   --    LEFT JOIN HW 
    --   ON HW.NAME = STUDENT.NAME
       WHERE HOMEROOM = 'Morgan'
    --   AND (HW.HW_DATE != DATE('now')
     --  OR HW.HW_DATE IS NULL)
    """
    df = pd.read_sql_query(SELECT_MORGAN, conn)
    return df

def select_students_hetrick(conn):
    SELECT_HETRICK = """
    SELECT STUDENT.NAME
       FROM STUDENT 
      -- LEFT JOIN HW 
      -- ON HW.NAME = STUDENT.NAME 
       WHERE HOMEROOM = 'Hetrick'
     --  AND (HW.HW_DATE != DATE('now')
      -- OR HW.HW_DATE IS NULL)
    """
    df = pd.read_sql_query(SELECT_HETRICK, conn)
    return df

def select_full_results(conn):
    SELECT_RESULTS = """
    SELECT STUDENT.NAME,
           HW.HW_DATE,
           HW.HW_DONE,
           HOMEROOM
       FROM STUDENT 
       INNER JOIN HW 
       ON HW.NAME = STUDENT.NAME 
    """
    df = pd.read_sql_query(SELECT_RESULTS, conn)
    return df

def select_counts(conn):
    SELECT_RESULTS = """
        SELECT STUDENT.NAME,
           HW.HW_DATE,
           SUM(CASE
                 WHEN HW.HW_DONE = 'NO'
                   THEN 1
                 ELSE 0
               END) AS HW_NOT_DONE_COUNT
       FROM STUDENT 
       INNER JOIN HW 
       ON HW.NAME = STUDENT.NAME
       GROUP BY STUDENT.NAME,
                HW.HW_DATE
    """
    df = pd.read_sql_query(SELECT_RESULTS, conn)
    df['HW_DATE'] = pd.to_datetime(df['HW_DATE'], errors='coerce')
    df['WEEK_START'] = df['HW_DATE'].dt.to_period('W').apply(lambda r: r.start_time)
    df_group = df.groupby(by=['NAME', 
                              'WEEK_START'], 
                          as_index=False)['HW_NOT_DONE_COUNT'].sum()
    df_all = df.groupby(by=['WEEK_START'], 
                        as_index=False)['HW_NOT_DONE_COUNT'].sum()
    return df_group, df_all

def my_email(password, data):
    msg = MIMEMultipart()
    msg['From'] = 'jjrekn@gmail.com'
    msg['To'] = 'jjrekn@gmail.com'
    msg['Subject'] = 'Homework Submission'
    attachment = MIMEApplication(data.to_csv(index=False))
    attachment["Content-Disposition"] = 'attachment; filename=" {}"'.format("Homework.csv")
    msg.attach(attachment)

    with smtplib.SMTP('smtp.gmail.com', 587) as e:
        e.ehlo()
        e.starttls(context=ssl.create_default_context())
        print(password.strip())
        e.login('jjrekn@gmail.com', password=password.strip())
        e.sendmail('jjrekn@gmail.com', 'jjrekn@gmail.com', msg.as_string())
    return None