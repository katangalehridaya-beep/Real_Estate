import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Real Estate Price Prediction")

st.title("🏠 AI Real Estate Intelligence Platform")

st.sidebar.header("Property Details")

bedrooms = st.sidebar.number_input("Bedrooms", 1, 10, 3)
bathrooms = st.sidebar.number_input("Bathrooms", 1, 10, 2)
living_area = st.sidebar.number_input("Living Area", value=2000)
lot_area = st.sidebar.number_input("Lot Area", value=5000)
floors = st.sidebar.number_input("Floors", value=1)
waterfront = st.sidebar.number_input("Waterfront Present (0/1)", value=0)
views = st.sidebar.number_input("Views", value=0)
condition = st.sidebar.number_input("Condition", value=3)
grade = st.sidebar.number_input("Grade", value=7)
house_area = st.sidebar.number_input("House Area Excluding Basement", value=2000)
basement_area = st.sidebar.number_input("Basement Area", value=0)
built_year = st.sidebar.number_input("Built Year", value=2005)
renovation_year = st.sidebar.number_input("Renovation Year", value=0)
postal_code = st.sidebar.number_input("Postal Code", value=98001)
latitude = st.sidebar.number_input("Latitude", value=47.5)
longitude = st.sidebar.number_input("Longitude", value=-122.2)
living_area_renov = st.sidebar.number_input("Living Area Renov", value=2000)
lot_area_renov = st.sidebar.number_input("Lot Area Renov", value=5000)
schools = st.sidebar.number_input("Schools Nearby", value=2)
airport_distance = st.sidebar.number_input("Distance From Airport", value=20)

if st.button("Predict Price"):

    input_data = pd.DataFrame([[
        bedrooms,
        bathrooms,
        living_area,
        lot_area,
        floors,
        waterfront,
        views,
        condition,
        grade,
        house_area,
        basement_area,
        built_year,
        renovation_year,
        postal_code,
        latitude,
        longitude,
        living_area_renov,
        lot_area_renov,
        schools,
        airport_distance
    ]])

    prediction = model.predict(input_data)

    st.success(f"Predicted Price: ₹ {prediction[0]:,.2f}")

    # Risk Score
    house_age = 2026 - built_year

    risk_score = (
        (10-condition)*4 +
        (house_age/100)*40
    )

    st.subheader("Risk Analysis")
    st.write("Risk Score:", round(risk_score,2))

    if risk_score < 30:
        risk = "Low Risk"
    elif risk_score < 60:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    st.write("Risk Category:", risk)

    # Recommendation
    if risk == "Low Risk":
        recommendation = "BUY"
    elif risk == "Medium Risk":
        recommendation = "HOLD"
    else:
        recommendation = "SELL"

    st.subheader("Investment Recommendation")
    st.write(recommendation)

    # Forecast
    st.subheader("Future Price Forecast")

    price_1 = prediction[0] * 1.08
    price_3 = prediction[0] * (1.08**3)
    price_5 = prediction[0] * (1.08**5)

    st.write("1 Year Forecast:", round(price_1,2))
    st.write("3 Year Forecast:", round(price_3,2))
    st.write("5 Year Forecast:", round(price_5,2))
