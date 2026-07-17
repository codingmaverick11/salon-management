import psycopg2
import streamlit as st
from fpdf import FPDF


def connect():

    conn = psycopg2.connect(
        host=st.secrets["host"],
        database="postgres",
        user=st.secrets["user"],
        password=st.secrets["password"],
        port="6543"
    )

    return conn



# ---------------- LOGIN ----------------

def login(username, password):

    conn = connect()
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM users
    WHERE username=%s
    AND password=%s
    """

    cursor.execute(
        query,
        (username, password)
    )

    user = cursor.fetchone()

    if user:

        user = {
            "id": user[0],
            "username": user[1],
            "password": user[2],
            "role": user[3]
        }


    cursor.close()
    conn.close()

    return user



# ---------------- ADD JOB CARD ----------------

def add_job_card(customer_name, phone, service,
                 amount, payment_mode,
                 employee, visit_date, visit_time):

    conn = connect()
    cursor = conn.cursor()


    query = """
    INSERT INTO job_cards
    (
    customer_name,
    phone,
    service,
    amount,
    payment_mode,
    employee,
    visit_date,
    visit_time
    )

    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s)
    """


    cursor.execute(
        query,
        (
            customer_name,
            phone,
            service,
            amount,
            payment_mode,
            employee,
            visit_date,
            visit_time
        )
    )


    conn.commit()

    cursor.close()
    conn.close()



# ---------------- ALL JOB CARDS ----------------

def get_all_job_cards():

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM job_cards
        ORDER BY visit_date DESC
        """
    )


    rows = cursor.fetchall()


    columns = [
        desc[0]
        for desc in cursor.description
    ]


    data = [
        dict(zip(columns,row))
        for row in rows
    ]


    for row in data:

        if row["visit_time"]:
            row["visit_time"] = str(row["visit_time"])


    cursor.close()
    conn.close()

    return data



# ---------------- REVENUE ----------------

def get_total_revenue():

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT SUM(amount)
        FROM job_cards
        """
    )


    result = cursor.fetchone()


    cursor.close()
    conn.close()


    return result[0] if result[0] else 0



# ---------------- EMPLOYEE SALES ----------------

def get_employee_sales():

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
        employee,
        COUNT(*) AS customers,
        SUM(amount) AS revenue

        FROM job_cards

        GROUP BY employee
        """
    )


    rows = cursor.fetchall()


    columns = [
        desc[0]
        for desc in cursor.description
    ]


    data = [
        dict(zip(columns,row))
        for row in rows
    ]


    cursor.close()
    conn.close()

    return data



# ---------------- CUSTOMER COUNT ----------------

def get_total_customers():

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM job_cards
        """
    )


    result = cursor.fetchone()


    cursor.close()
    conn.close()


    return result[0]



# ---------------- AVERAGE BILL ----------------

def get_average_bill():

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT AVG(amount)
        FROM job_cards
        """
    )


    result = cursor.fetchone()


    cursor.close()
    conn.close()


    return round(result[0],2) if result[0] else 0



# ---------------- SERVICES ----------------

def get_service_count():

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
        service,
        COUNT(*) AS count

        FROM job_cards

        GROUP BY service

        ORDER BY count DESC
        """
    )


    rows = cursor.fetchall()


    columns = [
        desc[0]
        for desc in cursor.description
    ]


    data = [
        dict(zip(columns,row))
        for row in rows
    ]


    cursor.close()
    conn.close()


    return data



# ---------------- SEARCH CUSTOMER ----------------

def search_customer(name):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
        customer_name,
        phone,
        service,
        amount,
        visit_date,
        visit_time,
        employee

        FROM job_cards

        WHERE customer_name ILIKE %s

        ORDER BY visit_date DESC
        """,
        ('%' + name + '%',)
    )


    rows = cursor.fetchall()


    columns = [
        desc[0]
        for desc in cursor.description
    ]


    data = [
        dict(zip(columns,row))
        for row in rows
    ]


    cursor.close()
    conn.close()

    return data



# ---------------- APPOINTMENT ----------------

def add_appointment(customer_name, phone, service,
                    appointment_date, appointment_time,
                    employee):


    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO appointments
        (
        customer_name,
        phone,
        service,
        appointment_date,
        appointment_time,
        employee
        )

        VALUES
        (%s,%s,%s,%s,%s,%s)
        """,

        (
            customer_name,
            phone,
            service,
            appointment_date,
            appointment_time,
            employee
        )
    )


    conn.commit()

    cursor.close()
    conn.close()



def get_appointments():

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM appointments
        ORDER BY appointment_date, appointment_time
        """
    )


    rows = cursor.fetchall()


    columns = [
        desc[0]
        for desc in cursor.description
    ]


    data = [
        dict(zip(columns,row))
        for row in rows
    ]


    cursor.close()
    conn.close()


    return data



# ---------------- EXPORT ----------------

def export_job_cards():

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
        customer_name,
        phone,
        service,
        amount,
        payment_mode,
        employee,
        visit_date,
        visit_time

        FROM job_cards

        ORDER BY visit_date DESC
        """
    )


    rows = cursor.fetchall()


    columns = [
        desc[0]
        for desc in cursor.description
    ]


    data = [
        dict(zip(columns,row))
        for row in rows
    ]


    cursor.close()
    conn.close()

    return data



# ---------------- PDF ----------------

def create_pdf_report(revenue, customers):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=16
    )


    pdf.cell(
        200,
        10,
        "Salon Monthly Report",
        ln=True
    )


    pdf.cell(
        200,
        10,
        f"Revenue: Rs {revenue}",
        ln=True
    )


    pdf.cell(
        200,
        10,
        f"Customers: {customers}",
        ln=True
    )


    pdf.output(
        "Salon_Report.pdf"
    )
#
def get_user_by_username(username):

        conn = connect()

        cursor = conn.cursor()

        query = """
        SELECT *
        FROM users
        WHERE username=%s
        """

        cursor.execute(
            query,
            (username,)
        )

        row = cursor.fetchone()

        if row:

            columns = [
                desc[0]
                for desc in cursor.description
            ]

            user = dict(
                zip(columns, row)
            )

        else:
            user = None

        cursor.close()
        conn.close()

        return user