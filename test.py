import streamlit as st
import folium
import requests
from streamlit_folium import folium_static

def fetch_hospitals(city):
    url = "http://test-1-app-lb-1716509588.us-west-1.elb.amazonaws.com:8080/medicalservices/getAll"
    payload = f"\"hospitals that accept AETNA insurance {city}\""
    headers = {
      'Content-Type': 'text/plain'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch hospital data.")
        return None

def main():
    st.markdown(
        """
        <style>
        .reportview-container {
            background: #8a2be2
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if 'title_clicked' not in st.session_state:
        st.header('We can Help you')
        if st.button('Click here to continue'):
            st.session_state['title_clicked'] = True
    else:
        st.title('Hospital Search Portal')

        california_map = folium.Map(location=[37.3382, -121.8863], zoom_start=10)

        city_query = st.text_input('Search for a city:', '')
        if st.button('Search'):
            hospitals_data = fetch_hospitals(city_query)

            if hospitals_data:
                for hospital in hospitals_data:
                    latitude = float(hospital['locationLat'])
                    longitude = float(hospital['locationLong'])
                    name = hospital['name']
                    address = hospital['address']
                    ratings = hospital['ratings']
                    business_status = hospital['businessStatus']

                    icon_color = 'green' if business_status == 'OPERATIONAL' else 'red'

                    popup_content = f"""
                        <b>Name:</b> {name}<br>
                        <b>Address:</b> {address}<br>
                        <b>Ratings:</b> {ratings}<br>
                        <b>Business Status:</b> {business_status}<br>
                    """

                    folium.Marker(
                        [latitude, longitude],
                        popup=folium.Popup(popup_content, max_width=300),
                        icon=folium.Icon(color=icon_color)
                    ).add_to(california_map)

        folium_static(california_map)

if __name__ == "__main__":
    main()
