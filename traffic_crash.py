import streamlit as st
import pandas as pd
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ilikedubai12",
    database="traffic_crash",
    auth_plugin="mysql_native_password"
)

cursor = connection.cursor()

st.title("Welcome to My Miniproject 1.")
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Main Menu", ["Home", "Queries"], 
        icons=['house', 'gear'], menu_icon="cast", default_index=1)
    selected
if selected == "Home":
    st.header('Traffic Crash Analysis Project for Business Insights and Decision Making.')
    st.write("In this analysis project, I have analysed the traffic crash dataset provided and extracted all the 15 query data outputs from the entire traffic crash dataset using VScode and MySQL queries, and I will discuss my findings and analysis of all the 15 query data outputs.")
    st.image("dataanalysis.jpg", caption="Jessica Sriramula")

if selected == "Queries":
    st.subheader("Analysis of all the 15 Query Data Outputs.")
    one = st.selectbox("Please choose the query you want to display:", ["Query 1: top 5 most dangerous combinations of weather and crash type", 
                                                                        "Query 2: top 10 streets with the highest number of injury crashes", 
                                                                        "Query 3: the percentage of crashes that resulted in injuries for each crash type", 
                                                                        "Query 4: the peak crash hour for each month", 
                                                                        "Query 5: the top 5 primary causes of crashes during night time for crash hour >=18", 
                                                                        "Query 6: comparing the average number of injuries in daylight conditions",
                                                                        "Query 7: comparing the average number of injuries in darkness conditions",
                                                                        "Query 8: traffic control device condition type that has the highest average injuries per crash",
                                                                        "Query 9: the top 5 locations (latitude) with the highest crash frequency", 
                                                                        "Query 10: the top 5 locations (longitude) with the highest crash frequency",
                                                                        "Query 11: the top 5 streets with the highest injury rate", 
                                                                        "Query 12: the most common crash type for each year", 
                                                                        "Query 13: the day of the week with the highest average crashes per hour", 
                                                                        "Query 14: high risk time slots and the bucket that has the highest injury crashes", 
                                                                        "Query 15: the top 3 contributing causes for each crash type", 
                                                                        "Query 16: the year-over-year growth rate of crashes", 
                                                                        "Query 17: hotspot zones grouped together",
                                                                        "Query 18: top 10 zones with highest crashes"])

    if one == "Query 1: top 5 most dangerous combinations of weather and crash type":
        st.write("Here we can see that when the weather was clear there was a significantly large number of crashes that happened with no injury/drive away compared to the remaining crash types that happened in rain and unknown weather conditions.")
        query = """SELECT WEATHER_CONDITION, 
    CRASH_TYPE, 
    COUNT(*) AS TOTAL_CRASHES
FROM 
    traffic_crashesdata
GROUP BY 

    WEATHER_CONDITION, 
    CRASH_TYPE

ORDER BY 
    TOTAL_CRASHES DESC

LIMIT 5;"""

        cursor.execute(query)
        
        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)
        

    if one == "Query 2: top 10 streets with the highest number of injury crashes":
        st.write("Here we can see all the top 10 streets with the highest number of total crashes where Western Avenue street has the highest number of total crashes.")
        query = """SELECT 
    STREET_NAME,
    COUNT(*) AS highest_injury_crashes
FROM 
    traffic_crashesdata
WHERE 
    STREET_NAME IS NOT NULL 
    AND STREET_NAME != ''
GROUP BY 
    STREET_NAME
ORDER BY 
    highest_injury_crashes DESC
LIMIT 10;"""

        cursor.execute(query)
        
        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)

    
    if one == "Query 3: the percentage of crashes that resulted in injuries for each crash type":
        st.write("Here we can see that 71% of crashes resulted in no injury/drive away and 29% of crashes resulted in injury and or tow due to crash.")
        query = """SELECT 
    CRASH_TYPE,
    COUNT(*) AS crashes_injuries,
    ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM traffic_crashesdata), 2) AS percentage_of_crashes_injuries
FROM 
    traffic_crashesdata
GROUP BY 
    CRASH_TYPE
ORDER BY 
    percentage_of_crashes_injuries DESC;"""
        
        cursor.execute(query)
        
        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)

        
    if one == "Query 4: the peak crash hour for each month":
        st.write("Here we can see all the peak crash hour for each month as well as the total injuries that happened for each peak crash hour.")
        query = """SELECT 
    CRASH_MONTH,
    CRASH_HOUR AS peak_crash_hour,
    INJURIES_TOTAL
FROM 
    traffic_crashesdata
ORDER BY 
    CRASH_MONTH ASC;"""
        
        cursor.execute(query)
        
        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)

    
    if one == "Query 5: the top 5 primary causes of crashes during night time for crash hour >=18":
        st.write("Here we can see all the top 5 primary causes of crashes during night time for crash hour >=18 where we are unable to determine the primary contributory cause for 24500 crashes that happened.")
        query = """SELECT 
    PRIM_CONTRIBUTORY_CAUSE,
    COUNT(*) AS total_crashes_greaterthan_or_equal_to_crashhour18
FROM 
    traffic_crashesdata
WHERE 
    CRASH_HOUR >= 18
GROUP BY 
    PRIM_CONTRIBUTORY_CAUSE
ORDER BY 
    total_crashes_greaterthan_or_equal_to_crashhour18 DESC

LIMIT 5;"""
        
        cursor.execute(query)
        
        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)

    
    if one == "Query 6: comparing the average number of injuries in daylight conditions":
        st.write("Here we can see all the total number of injuries that happened in the daylight conditions.")
        query = """SELECT 
    ROUND(AVG(INJURIES_TOTAL), 4) AS avg_injuries_daylight,
    COUNT(*) AS total_daylight_crashes
FROM 
    traffic_crashesdata
WHERE 
    CRASH_HOUR >= 6
    AND CRASH_HOUR < 18;"""
        
        cursor.execute(query)
        
        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)


    if one == "Query 7: comparing the average number of injuries in darkness conditions":
        st.write("Here we can see all the total number of injuries that happened in the darkness conditions, so we can say that injuries only happened during the daylight conditions and there was no injuries that happened in the darkness conditions.")
        query = """SELECT 
    ROUND(AVG(INJURIES_TOTAL), 4) AS avg_injuries_nightime,
    COUNT(*) AS total_nightime_crashes
FROM 
    traffic_crashesdata
WHERE 
    CRASH_HOUR <= 6 
    AND CRASH_HOUR > 18;"""
        
        cursor.execute(query)
        
        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)

        

    if one == "Query 8: traffic control device condition type that has the highest average injuries per crash":
        st.write("Here we can see the device condition type that has the highest average injuries per crash and that is the missing device condition type and the lowest being the no controls device condition type.")
        query = """SELECT 
    DEVICE_CONDITION,
    COUNT(*) AS total_injuries,
    ROUND(AVG(INJURIES_TOTAL), 2) AS high_avg_injuries_per_crash
FROM 
    traffic_crashesdata
GROUP BY 
    DEVICE_CONDITION
ORDER BY 
    high_avg_injuries_per_crash DESC;"""
        
        cursor.execute(query)
        
        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)


    if one == "Query 9: the top 5 locations (latitude) with the highest crash frequency":
        st.write("Here we can see the top 5 locations (latitude) with the highest crash frequency.")
        query = """SELECT 
    LATITUDE,
    COUNT(*) AS highest_crash_frequency
FROM 
    traffic_crashesdata
WHERE 
    LATITUDE IS NOT NULL 
    AND LATITUDE != 0 
GROUP BY 
    LATITUDE
ORDER BY 
    highest_crash_frequency DESC
LIMIT 5;"""

        cursor.execute(query)
        
        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)

    if one == "Query 10: the top 5 locations (longitude) with the highest crash frequency":
        st.write("Here we can see the top 5 locations (longitude) with the highest crash frequency.")
        query = """SELECT 
    LONGITUDE,
    COUNT(*) AS highest_crash_frequency
FROM 
    traffic_crashesdata
WHERE 
    LONGITUDE IS NOT NULL 
    AND LONGITUDE != 0 
GROUP BY 
    LONGITUDE
ORDER BY 
    highest_crash_frequency DESC
LIMIT 5;"""

        cursor.execute(query)
        
        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)

    if one  == "Query 11: the top 5 streets with the highest injury rate":
        st.write("Here we can see the top 5 streets with the highest injury rate, where Russell Drive street has the highest injury rate of 47%.")
        query = """SELECT
    STREET_NAME,
    COUNT(*) INJURIES_TOTAL,
    ROUND((SUM(CASE WHEN INJURIES_TOTAL > 0 THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) AS HIGH_INJURY_RATE
FROM 
    traffic_crashesdata
GROUP BY 
    STREET_NAME
HAVING 
    COUNT(*) >= 10 
ORDER BY 
    HIGH_INJURY_RATE DESC
LIMIT 5;"""

        cursor.execute(query)
        
        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)


    if one == "Query 12: the most common crash type for each year":
        st.write("Here we can see all the most common crash types for each year.")
        query = """SELECT 
    year,
    CRASH_TYPE AS most_common_crash_type,
    INJURIES_TOTAL
FROM 
    traffic_crashesdata
ORDER BY 
    year DESC;"""
        
        cursor.execute(query)
        
        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)

        st.write("Here we can see the most common crash type for each year.")

    if one ==  "Query 13: the day of the week with the highest average crashes per hour":
        st.write("Here we can see that there are zero highest average crashes per hour in none of the day of the week.")
        query = """SELECT 
    DAYNAME(CRASH_DATE) AS day_of_week,
    COUNT(CRASH_RECORD_ID) / (COUNT(DISTINCT DATE(CRASH_DATE)) * 24) AS highest_average_crashes_per_hour
FROM 
    traffic_crashesdata
GROUP BY 
    DAYOFWEEK(CRASH_DATE), 
    DAYNAME(CRASH_DATE)
ORDER BY 
    highest_average_crashes_per_hour DESC
LIMIT 1;"""

        cursor.execute(query)

        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)

    if one == "Query 14: high risk time slots and the bucket that has the highest injury crashes":
        st.write("Here we can see that after grouping all the time slots into morning,afternoon,evening and night, the high risk time slot is night time slot as it has the highest number of injury crashes.")
        query = """SELECT 
    CASE 
        WHEN HOUR(CRASH_HOUR) BETWEEN 8 AND 11 THEN 'Morning (08:00 - 11:59)'
        WHEN HOUR(CRASH_HOUR) BETWEEN 12 AND 15 THEN 'Afternoon (12:00 - 15:59)'
        WHEN HOUR(CRASH_HOUR) BETWEEN 16 AND 19 THEN 'Evening (16:00 - 19:59)'
        ELSE 'Night (20:00 - 23:59)'
    END AS high_risk_time_slot,

    COUNT(*) AS highest_injury_crashes
FROM 
    traffic_crashesdata
GROUP BY 
    high_risk_time_slot
ORDER BY 
    highest_injury_crashes DESC;"""
        
        cursor.execute(query)

        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)


    if one == "Query 15: the top 3 contributing causes for each crash type":
        st.write("Here we can see the top 3 primary and secondary contributing causes for each crash type.")
        query = """SELECT 
    PRIM_CONTRIBUTORY_CAUSE,
    SEC_CONTRIBUTORY_CAUSE,
    CRASH_TYPE,  
    RANK() OVER (PARTITION BY PRIM_CONTRIBUTORY_CAUSE ORDER BY CRASH_TYPE DESC) AS top_3_causes

FROM
    traffic_crashesdata
    
LIMIT 3;"""

        cursor.execute(query)

        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)

    if one == "Query 16: the year-over-year growth rate of crashes":
        st.write("Here we can see the year over year growth rate of the crashes from the years 2020 - 2026, where the highest year over year growth rate is 33% in the year 2024.")
        query = """
WITH YearlyCounts AS (
    SELECT 
        year AS crash_year,
        COUNT(CRASH_RECORD_ID) AS current_crashes
    FROM 
        traffic_crashesdata
    GROUP BY 
        crash_year
)
SELECT 
    crash_year,
    current_crashes,
    LAG(current_crashes) OVER (ORDER BY crash_year) AS previous_crashes,
    ROUND(((current_crashes - LAG(current_crashes) OVER (ORDER BY crash_year)) / LAG(current_crashes) OVER (ORDER BY crash_year)) * 100, 2) AS yoy_growth_rate
FROM 
    YearlyCounts;"""
        
        cursor.execute(query)

        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)


    if one == "Query 17: hotspot zones grouped together":
        st.write("Here we can see all the hotspot zones latitude and longitude grouped together according to highest number of crashes.")
        query = """SELECT 
    ROUND(LATITUDE, 2) AS hotspot_zone_latitude,
    ROUND(LONGITUDE, 2) AS hotspot_zone_longitude,
    COUNT(*) AS highest_crashes
FROM
    traffic_crashesdata
WHERE 
    LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL
GROUP BY 
    hotspot_zone_latitude, hotspot_zone_longitude
ORDER BY 
    highest_crashes DESC;"""
        
        cursor.execute(query)

        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)

        
    if one == "Query 18: top 10 zones with highest crashes":
        st.write("Here we can see the top 10 zones with highest number of crashes.")
        query = """SELECT 
    ROUND(latitude, 3) AS zone_latitude,
    ROUND(longitude, 3) AS zone_longitude,
    COUNT(*) AS highest_number_of_crashes
FROM 
    traffic_crashesdata
    
WHERE LATITUDE IS NOT NULL 
AND LONGITUDE IS NOT NULL

GROUP BY
     zone_latitude, zone_longitude
ORDER BY 
     highest_number_of_crashes DESC
LIMIT 10;"""

        cursor.execute(query)

        result = cursor.fetchall()
        
        df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
        
        st.dataframe(df)











        




    


        



        








        


    



    