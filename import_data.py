import csv
import psycopg2

# Database connection parameters
conn = psycopg2.connect(
    dbname="joy_of_painting",
    user="painting_user",
    password="brushstrokes123",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# Function to check for existing records before inserting
def check_and_insert(table, insert_values):
    columns = ', '.join(insert_values.keys())
    values_placeholder = ', '.join(['%s'] * len(insert_values))
    query = f"SELECT 1 FROM {table} WHERE {insert_values['painting_index']} = %s"  # Adjust the column you're using for duplicate check
    
    # Execute query
    cursor.execute(query, (insert_values['painting_index'],))  # Assuming `painting_index` is used for checking duplicates
    exists = cursor.fetchone()

    if not exists:  # If no duplicate found
        insert_query = f"INSERT INTO {table} ({columns}) VALUES ({values_placeholder})"
        cursor.execute(insert_query, tuple(insert_values.values()))
        conn.commit()
        print(f"Inserted: {insert_values}")
    else:
        print(f"Duplicate found for painting_index: {insert_values['painting_index']}")

# Function to process CSV and insert into respective table
def import_csv(file_path, table_name):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            insert_values = {
                "painting_index": row["painting_index"],
                "img_src": row["img_src"],
                "painting_title": row["painting_title"],
                "season": row["season"],
                "episode": row["episode"],
                "num_colors": row["num_colors"],
                "youtube_src": row["youtube_src"],
                "colors": row["colors"],  # String of colors
                "color_hex": row["color_hex"],  # String of hex values
                "Black_Gesso": row["Black_Gesso"],
                "Bright_Red": row["Bright_Red"],
                "Burnt_Umber": row["Burnt_Umber"],
                "Cadmium_Yellow": row["Cadmium_Yellow"],
                "Dark_Sienna": row["Dark_Sienna"],
                "Indian_Red": row["Indian_Red"],
                "Indian_Yellow": row["Indian_Yellow"],
                "Liquid_Black": row["Liquid_Black"],
                "Liquid_Clear": row["Liquid_Clear"],
                "Midnight_Black": row["Midnight_Black"],
                "Phthalo_Blue": row["Phthalo_Blue"],
                "Phthalo_Green": row["Phthalo_Green"],
                "Prussian_Blue": row["Prussian_Blue"],
                "Sap_Green": row["Sap_Green"],
                "Titanium_White": row["Titanium_White"],
                "Van_Dyke_Brown": row["Van_Dyke_Brown"],
                "Yellow_Ochre": row["Yellow_Ochre"],
                "Alizarin_Crimson": row["Alizarin_Crimson"]
            }
            check_and_insert(table_name, insert_values)

# Call the function to import data into the tables
import_csv("Cleaned_Colors_Used.csv", "colors_used")
# Call other import functions for subject_matter, episode_dates, if needed
# import_csv("subject_matter.csv", "subject_matter")
# import_csv("episode_dates.csv", "episode_dates")

# Close the connection
cursor.close()
conn.close()
