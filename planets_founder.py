import sqlite3
import csv
import io

# ====================================================
# Project: NASA Exoplanet Advanced Search Engine
# Developer: [Mohammed Ramli]
# Date: 18-11-2026
# Description: Professional Python & SQLite application 
#              to filter, convert, and analyze NASA data.
# ====================================================

print("==================================================")
print("     NASA Exoplanet Advanced Search Engine        ")
print("     Developed with Python & SQLite               ")
print("==================================================\n")

conn = sqlite3.connect('space_exploration.db')
cursor = conn.cursor()

# Create table structure
cursor.execute('DROP TABLE IF EXISTS Planets')
cursor.execute('''
CREATE TABLE Planets (
    Name TEXT,
    Temperature REAL,
    Diameter REAL
)
''')

filename = 'planets_data.csv'

try:
    with open(filename, mode='r', encoding='utf-8') as file:
        lines = [line for line in file if not line.strip().startswith('#')]

    clean_data = io.StringIO(''.join(lines))
    reader = csv.DictReader(clean_data)

    count = 0
    for row in reader:
        name = row.get('pl_name', '')
        temp_str = row.get('pl_eqt', '')
        rad_str = row.get('pl_rade', '')
        
        if name:
            try:
                # Convert Kelvin to Celsius and Earth radius to kilometers
                temp = float(temp_str) - 273.15 if temp_str else 0.0
                diameter = float(rad_str) * 12742.0 if rad_str else 0.0
                
                cursor.execute("INSERT INTO Planets VALUES (?, ?, ?)", 
                               (name, temp, diameter))
                count += 1
            except ValueError:
                continue

    conn.commit()
    print(f"Successfully imported {count} planets total!")

    # Dataset Diagnostic Report
    cursor.execute("SELECT COUNT(*) FROM Planets WHERE Temperature > 0")
    temp_available = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Planets WHERE Diameter > 0")
    diam_available = cursor.fetchone()[0]

    print("\n--------------------------------------------------")
    print("📊 DATASET DIAGNOSTIC REPORT:")
    print(f" - Planets with Temperature data: {temp_available} available")
    print(f" - Planets with Diameter data: {diam_available} available")
    print("--------------------------------------------------\n")

except FileNotFoundError:
    print(f"Error: File '{filename}' not found. Please make sure '{filename}' is in the directory.")

print("==========================================")
print("       Planet Search & Filter Menu        ")
print("==========================================")

try:
    choice = input("Do you want to search only the Habitable Zone (0°C to 100°C)? (y/n): ").strip().lower()

    use_temp = True
    use_diam = True
    min_temp, max_temp = 0.0, 0.0
    min_diam, max_diam = 0.0, 0.0

    if choice == 'y':
        min_temp, max_temp = 0.1, 100.0
        min_diam, max_diam = 0.0, 1000000.0
        print("\nTargeting Habitable Zone with fully recorded data...\n")
    else:
        print("\nEnter your custom search criteria (Type 'na' to skip any criteria):")
        
        # Temperature input with 'na' bypass option
        min_temp_input = input("Minimum Temperature (°C) [or type 'na']: ").strip().lower()
        if min_temp_input == 'na':
            use_temp = False
        else:
            min_temp = float(min_temp_input)
            max_temp = float(input("Maximum Temperature (°C): "))

        # Diameter input with 'na' bypass option
        min_diam_input = input("Minimum Diameter (km) [or type 'na']: ").strip().lower()
        if min_diam_input == 'na':
            use_diam = False
        else:
            min_diam = float(min_diam_input)
            max_diam = float(input("Maximum Diameter (km): "))
        
        print(f"\nSearching database...\n")

    # Build dynamic query conditions
    query_conditions = ["FROM Planets WHERE 1=1"]
    params = []

    if use_temp:
        query_conditions.append("AND Temperature BETWEEN ? AND ? AND Temperature > 0")
        params.extend([min_temp, max_temp])

    if use_diam:
        query_conditions.append("AND Diameter BETWEEN ? AND ? AND Diameter > 0")
        params.extend([min_diam, max_diam])

    base_query_where = " ".join(query_conditions)

    # 1. Count total matching planets
    cursor.execute(f"SELECT COUNT(*) {base_query_where}", tuple(params))
    total_matches = cursor.fetchone()[0]
    
    print(f"📊 Total matching planets found: {total_matches}")

    if total_matches > 0:
        # Smart Sorting: Prioritize records that contain complete data when a criteria is skipped
        order_clause = ""
        if not use_temp:
            order_clause = "ORDER BY CASE WHEN Temperature > 0 THEN 0 ELSE 1 END"
        elif not use_diam:
            order_clause = "ORDER BY CASE WHEN Diameter > 0 THEN 0 ELSE 1 END"

        # 2. Fetch top 10 results with smart sorting
        cursor.execute(f"""
            SELECT Name, Temperature, Diameter 
            {base_query_where}
            {order_clause}
            LIMIT 10
        """, tuple(params))
        
        results = cursor.fetchall()

        print(f"🌟 Showing the top {len(results)} matching planets (Prioritizing complete records):")
        for index, planet in enumerate(results, start=1):
            p_name = planet[0]
            p_temp = f"{round(planet[1], 2)}°C" if planet[1] > 0 else "Data Not Available"
            p_diam = f"{round(planet[2], 1)} km" if planet[2] > 0 else "Data Not Available"
            
            print(f" {index}. Planet: {p_name} | Temp: {p_temp} | Diameter: {p_diam}")
    else:
        print("No planets found matching your criteria.")

except ValueError:
    print("Error: Please enter valid numeric values or 'na'.")

conn.close()
