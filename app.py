import streamlit as st
from datetime import datetime
import pytz


from database import (
    add_job_card,
    add_appointment
)


# Page settings
st.set_page_config(
    page_title="Salon Job Card",
    page_icon="💇",
    layout="centered"
)


st.title("💇 Salon Job Card")


# ---------------- EMPLOYEE SELECTION ----------------

st.subheader("Employee Details")

employee = st.selectbox(
    "Employee Name",
    [
        "Rajni",
        "Kiran",
        "Emp3",
        "Emp4"
    ]
)


if employee == "Other":
    employee = st.text_input(
        "Enter Employee Name"
    )


st.divider()


# ---------------- CREATE JOB CARD ----------------

st.subheader("📝 Create Job Card")


customer = st.text_input(
    "Customer Name"
)


phone = st.text_input(
    "Phone Number"
)


service = st.selectbox(
    "Service",
    [
        "Threading",
        "Haircut",
        "Facial",
        "Waxing",
        "Hair Color",
        "Nails",
        "Spa",
        "Other"
    ]
)


if service == "Other":

    custom_service = st.text_input(
        "Specify Service"
    )

    if custom_service:
        service = custom_service



amount = st.number_input(
    "Amount",
    min_value=0.0
)


payment = st.selectbox(
    "Payment Mode",
    [
        "Cash",
        "UPI",
        "Card"
    ]
)



# Automatic timestamp

india_timezone = pytz.timezone(
    "Asia/Kolkata"
)

current_time = datetime.now(
    india_timezone
)


date = current_time.date()

time = current_time.time()



st.info(
    f"Visit Time: {date} | {time.strftime('%H:%M:%S')}"
)



if st.button(
    "Save Job Card",
    use_container_width=True
):

    if not customer or not phone or not employee:

        st.error(
            "Please fill all required details"
        )


    else:

        add_job_card(
            customer,
            phone,
            service,
            amount,
            payment,
            employee,
            date,
            time
        )


        st.success(
            "✅ Job Card Saved Successfully"
        )



st.divider()



# ---------------- APPOINTMENT ----------------


st.subheader(
    "📅 Create Appointment"
)


app_customer = st.text_input(
    "Customer Name",
    key="app_customer"
)


app_phone = st.text_input(
    "Phone Number",
    key="app_phone"
)



app_service = st.selectbox(
    "Service",
    [
        "Haircut",
        "Beard",
        "Facial",
        "Hair Color",
        "Spa",
        "Other"
    ],
    key="app_service"
)



app_date = st.date_input(
    "Appointment Date"
)


app_time = st.time_input(
    "Appointment Time"
)



if st.button(
    "Book Appointment",
    use_container_width=True
):

    if not app_customer or not app_phone:

        st.error(
            "Please fill customer details"
        )


    else:

        add_appointment(
            app_customer,
            app_phone,
            app_service,
            app_date,
            app_time,
            employee
        )


        st.success(
            "📅 Appointment Booked Successfully"
        )