import streamlit as st
from datetime import datetime
import pytz
import pandas as pd
import extra_streamlit_components as stx
from database import (
    login,
    get_user_by_username,
    add_job_card,
    get_all_job_cards,
    get_total_revenue,
    get_employee_sales,
    get_total_customers,
    get_average_bill,
    get_service_count,
    search_customer,
    add_appointment,
    get_appointments,
    export_job_cards,
    create_pdf_report
)


# Page settings
st.set_page_config(
    page_title="Salon Management",
    page_icon="💇",
    layout="centered"
)

cookie_manager = stx.CookieManager()


st.title("Salon Management")


# ---------------- SESSION INITIALIZATION ----------------

if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- AUTO LOGIN FROM COOKIE ----------------

if "logged_out" not in st.session_state:
    st.session_state.logged_out = False


saved_user = cookie_manager.get(
    "logged_in_user"
)


if (
    st.session_state.user is None
    and saved_user
    and not st.session_state.logged_out
):

    user = get_user_by_username(
        saved_user
    )

    if user:
        st.session_state.user = user



# ---------------- LOGIN PAGE ----------------

if st.session_state.user is None:

    st.subheader("Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button(
        "Login",
        use_container_width=True
    ):

        user = login(
            username,
            password
        )


        if user:

            st.session_state.logged_out = False
            st.session_state.user = user


            # Save login for 30 days
            cookie_manager.set(
                "logged_in_user",
                user["username"]
            )


            st.success(
                "Login Successful!"
            )

            st.rerun()


        else:

            st.error(
                "Invalid Username or Password"
            )



# ---------------- AFTER LOGIN ----------------

else:

    user = st.session_state.user


    st.sidebar.success(
        f"Logged in as: {user['username']}"
    )

    if st.sidebar.button(
            "Logout",
            use_container_width=True
    ):
        cookie_manager.delete(
            "logged_in_user"
        )

        # Prevent auto login after logout
        st.session_state.logged_out = True

        st.session_state.user = None

        st.success(
            "Logged out successfully!"
        )

        st.rerun()



    # -------- OWNER DASHBOARD --------

    if user["role"] == "owner":

        st.header("👑 Owner Dashboard")

        revenue = get_total_revenue()

        customers = get_total_customers()

        avg_bill = get_average_bill()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Revenue",
                f"₹ {revenue}"
            )

        with col2:
            st.metric(
                "Customers",
                customers
            )

        with col3:
            st.metric(
                "Average Bill",
                f"₹ {avg_bill}"
            )

        st.divider()

        st.subheader("📋 All Job Cards")

        jobs = get_all_job_cards()

        st.dataframe(
            jobs,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("👨‍💼 Employee Performance")

        sales = get_employee_sales()

        st.dataframe(
            sales,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("🔍 Customer History")

        search_name = st.text_input(
            "Enter Customer Name"
        )

        if st.button("Search Customer", use_container_width=True):

            history = search_customer(search_name)

            if history:

                st.dataframe(
                    history,
                    use_container_width=True,
                    hide_index=True
                )


            else:

                st.warning(
                    "No customer found"
                )

        st.divider()

        st.subheader("📅 Upcoming Appointments")

        appointments = get_appointments()

        if appointments:

            st.dataframe(
                appointments,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No appointments available"
            )

        st.subheader("📥 Export Reports")

        if st.button("Generate Excel Report", use_container_width=True):
            data = export_job_cards()

            df = pd.DataFrame(data)

            excel_file = "Salon_Report.xlsx"

            df.to_excel(
                excel_file,
                index=False
            )

            with open(excel_file, "rb") as file:
                st.download_button(
                    label="Download Excel",
                    data=file,
                    file_name="Salon_Report.xlsx"
                )

        if st.button("Generate PDF Report", use_container_width=True):
            create_pdf_report(
                revenue,
                customers
            )

            with open(
                    "Salon_Report.pdf",
                    "rb"
            ) as file:
                st.download_button(
                    "Download PDF",
                    file,
                    "Salon_Report.pdf"
                )


    # -------- EMPLOYEE DASHBOARD --------

    else:

        st.header("💇 Employee Dashboard")


        st.subheader("Create Job Card")


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

        india_timezone = pytz.timezone("Asia/Kolkata")

        current_time = datetime.now(india_timezone)

        date = current_time.date()

        time = current_time.time()

        st.info(
            f"Visit Time: {date} | {time.strftime('%H:%M:%S')}"
        )


        if st.button("Save Job Card", use_container_width=True):


            add_job_card(
                customer,
                phone,
                service,
                amount,
                payment,
                user["username"],
                date,
                time
            )


            st.success(
                "✅ Job Card Saved Successfully!"
            )

        st.divider()

        st.subheader("📅 Create Appointment")

        app_customer = st.text_input(
            "Customer Name",
            key="appointment_customer"
        )

        app_phone = st.text_input(
            "Phone Number",
            key="appointment_phone"
        )

        app_service = st.selectbox(
            "Service",
            [
                "Haircut",
                "Beard",
                "Facial",
                "Hair Color",
                "Spa"
            ],
            key="appointment_service"
        )

        app_date = st.date_input(
            "Appointment Date",
            key="appointment_date"
        )

        app_time = st.time_input(
            "Appointment Time",
            key="appointment_time"
        )

        if st.button("Book Appointment", use_container_width=True):
            add_appointment(

                app_customer,
                app_phone,
                app_service,
                app_date,
                app_time,
                user["username"]

            )

            st.success(
                "Appointment Booked!"
            )