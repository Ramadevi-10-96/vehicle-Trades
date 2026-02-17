import streamlit as st
import pyodbc
import pandas as pd

# DB Connection
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"
    "Database=VehicleSystem;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

st.title("🚗 Vehicle Rental, Resale & Training System")

menu = st.sidebar.selectbox(
    "Select Option",
    ["Register User", "Add Vehicle", "View Vehicles", "Rent Vehicle", "Resale", "Training"]
)

# Register User
if menu == "Register User":
    st.header("Register User")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    if st.button("Register"):
        cursor.execute("INSERT INTO Users (name,email,phone) VALUES (?,?,?)", (name,email,phone))
        conn.commit()
        st.success("User Registered Successfully")

# Add Vehicle (NEW)
elif menu == "Add Vehicle":
    st.header("Add Vehicle (Admin)")
    vname = st.text_input("Vehicle Name")
    vtype = st.selectbox("Vehicle Type", ["Bike", "Car", "Auto"])
    price = st.number_input("Price per day / resale", step=100)

    if st.button("Add Vehicle"):
        cursor.execute(
            "INSERT INTO Vehicles (vehicle_name, type, price, status) VALUES (?,?,?,?)",
            (vname, vtype, price, "Available")
        )
        conn.commit()
        st.success("Vehicle Added Successfully")

# View Vehicles
elif menu == "View Vehicles":
    st.header("Vehicles List")
    df = pd.read_sql("SELECT * FROM Vehicles", conn)
    st.dataframe(df)

# Rent Vehicle
elif menu == "Rent Vehicle":
    st.header("Rent Vehicle")
    user_id = st.number_input("User ID", step=1)
    vehicle_id = st.number_input("Vehicle ID", step=1)
    days = st.number_input("Days", step=1)

    if st.button("Rent"):
        cursor.execute("INSERT INTO Rentals (user_id, vehicle_id, days) VALUES (?,?,?)",
                       (user_id, vehicle_id, days))
        cursor.execute("UPDATE Vehicles SET status='Rented' WHERE vehicle_id=?", (vehicle_id,))
        conn.commit()
        st.success("Vehicle Rented Successfully")

# Resale
elif menu == "Resale":
    st.header("Resale Vehicle")
    user_id = st.number_input("User ID", step=1)
    vehicle_id = st.number_input("Vehicle ID", step=1)
    price = st.number_input("Resale Price", step=100)

    if st.button("Sell"):
        cursor.execute("INSERT INTO Resale (user_id, vehicle_id, price) VALUES (?,?,?)",
                       (user_id, vehicle_id, price))
        cursor.execute("UPDATE Vehicles SET status='Sold' WHERE vehicle_id=?", (vehicle_id,))
        conn.commit()
        st.success("Vehicle Sold Successfully")

# Training
elif menu == "Training":
    st.header("Vehicle Training")
    user_id = st.number_input("User ID", step=1)
    vehicle_type = st.selectbox("Vehicle Type", ["Bike", "Car", "Auto"])
    duration = st.number_input("Duration (days)", step=1)

    if st.button("Apply"):
        cursor.execute("INSERT INTO Training (user_id, vehicle_type, duration_days) VALUES (?,?,?)",
                       (user_id, vehicle_type, duration))
        conn.commit()
        st.success("Training Applied Successfully")
