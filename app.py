import streamlit as st
from pymongo import MongoClient
import base64

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://sudhakartechw:root@crazy1.0em7j98.mongodb.net/")
db = client["mydb"]
collection = db["image"]

def insert_data(profile_photo, name, employee_id, email, phone_number):
    # Convert uploaded image to base64 format
    encoded_image = base64.b64encode(profile_photo.read()).decode('utf-8')

    # Store base64 encoded image in the database
    data = {
        "profile_photo": encoded_image,
        "name": name,
        "employee_id": employee_id,
        "email": email,
        "phone_number": phone_number
    }
    collection.insert_one(data)

def view_data(employee_id):
    query = {"employee_id": employee_id}
    result = collection.find_one(query)
    return result

def main():
    st.title("Employee Management System")

    page = st.sidebar.selectbox("Select a page", ["Add Employee", "View Employee"])

    if page == "Add Employee":
        st.header("Add Employee")

        profile_photo = st.file_uploader("Upload Profile Photo", type=["jpg", "jpeg", "png"])
        name = st.text_input("Name")
        employee_id = st.text_input("Employee ID")
        email = st.text_input("Email")
        phone_number = st.text_input("Phone Number")

        if st.button("Submit"):
            if profile_photo is not None and name != "" and employee_id != "" and email != "" and phone_number != "":
                insert_data(profile_photo, name, employee_id, email, phone_number)
                st.success("Employee added successfully!")
            else:
                st.error("Please fill in all fields.")

    elif page == "View Employee":
        st.header("View Employee")

        employee_id = st.text_input("Enter Employee ID")

        if st.button("View"):
            if employee_id != "":
                result = view_data(employee_id)
                if result:
                    st.write("Name:", result["name"])
                    st.write("Employee ID:", result["employee_id"])
                    st.write("Email:", result["email"])
                    st.write("Phone Number:", result["phone_number"])
                    if result["profile_photo"]:
                        st.image(base64.b64decode(result["profile_photo"]), caption="Profile Photo", use_column_width=True)
                else:
                    st.error("Employee ID not found.")
            else:
                st.error("Please enter an Employee ID.")

if __name__ == "__main__":
    main()
