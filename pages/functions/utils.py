import pandas as pd
import sqlite3 as sql
import os

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
    #db_file = os.path.dirname(os.path.abspath(__file__)) + '\\kmo13.db'
    db_file = 'https://github.com/jakereckin/Katelyn_School_DP/blob/97eb316175689a0ac60a9d2edc776e9b620915a8/kmo13.db'
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
           HW.HW_DONE
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
           COUNT(HW.HW_DONE) AS HW_NOT_DONE_COUNT
       FROM STUDENT 
       INNER JOIN HW 
       ON HW.NAME = STUDENT.NAME 
       WHERE HW.HW_DONE = 'NO'
       GROUP BY STUDENT.NAME,
                HW.HW_DATE
    """
    df = pd.read_sql_query(SELECT_RESULTS, conn)
    df['HW_DATE'] = pd.to_datetime(df['HW_DATE'])
    df['WEEK_START'] = df['HW_DATE'].dt.to_period('W').apply(lambda r: r.start_time)
    df_group = df.groupby(by=['NAME', 'WEEK_START'], as_index=False)['HW_NOT_DONE_COUNT'].sum()
    return df_group
