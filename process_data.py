import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

# Step 1: Read the Colors Used data from the CSV file
colors_used_df = pd.read_csv('Colors_Used.csv')

# Display the first few rows to verify the data
print("Colors Used Data:")
print(colors_used_df.head())

# Step 2: Clean the Colors Used data (e.g., remove unwanted characters in 'colors' column)
colors_used_df['colors'] = colors_used_df['colors'].apply(lambda x: x.strip("[]").replace("'", "").split(","))
colors_used_df['color_hex'] = colors_used_df['color_hex'].apply(lambda x: x.strip("[]").replace("'", "").split(","))
colors_used_df.to_csv('Cleaned_Colors_Used.csv', index=False)

print("\nCleaned Colors Used Data saved as 'Cleaned_Colors_Used.csv'")

# Step 3: Read the Subject Matter data from the CSV file
subject_matter_df = pd.read_csv('Subject_Matter.csv')

# Display the first few rows to verify the data
print("\nSubject Matter Data:")
print(subject_matter_df.head())

# Step 4: Clean the Subject Matter data (Optional: If needed, make sure there are no unnecessary quotes)
subject_matter_df['TITLE'] = subject_matter_df['TITLE'].apply(lambda x: x.strip('"'))
subject_matter_df.to_csv('Cleaned_Subject_Matter.csv', index=False)

print("\nCleaned Subject Matter Data saved as 'Cleaned_Subject_Matter.csv'")

# Step 5: Read the Episode Dates data from the CSV file
try:
    episode_dates_df = pd.read_csv('Episode_Dates.csv', header=None, names=['Episode', 'Title', 'Description'], on_bad_lines='skip')
    episode_dates_df['Title'] = episode_dates_df['Title'].apply(lambda x: x.strip('"'))
    episode_dates_df.to_csv('Cleaned_Episode_Dates.csv', index=False)
    print("Cleaned Episode Dates Data saved as 'Cleaned_Episode_Dates.csv'")

except pd.errors.ParserError as e:
    print(f"Error reading Episode_Dates.csv: {e}")

# Display the first few rows to verify the data
print("\nEpisode Dates Data:")
print(episode_dates_df.head())

# Step 6: Clean the Episode Dates data (e.g., separate the 'Title' and 'Description' if needed)
episode_dates_df['Title'] = episode_dates_df['Title'].apply(lambda x: x.strip('"'))

episode_dates_df.to_csv('Cleaned_Episode_Dates.csv', index=False)

print("\nCleaned Episode Dates Data saved as 'Cleaned_Episode_Dates.csv'")

# Step 7: Additional Data Analysis (Optional)

# Example: Count the number of episodes with specific subjects
# Counting how many episodes have 'TREE' from the subject matter data
tree_count = subject_matter_df['TREE'].sum()
print(f"\nNumber of episodes with 'TREE': {tree_count}")

# Example: Find episodes with 'SUN'
sun_episodes = subject_matter_df[subject_matter_df['SUN'] == 1]
print("\nEpisodes with 'SUN':")
print(sun_episodes[['EPISODE', 'TITLE']])

# Step 8: Plot the frequency of each subject across episodes
subject_counts = subject_matter_df.drop(columns=['EPISODE', 'TITLE']).sum()

# Plot the counts of each subject
subject_counts.plot(kind='bar', figsize=(10, 6))
plt.title('Subject Matter Frequency Across Episodes')
plt.xlabel('Subject Matter')
plt.ylabel('Frequency')
plt.show()

# Step 9: Output tables in console using tabulate
print("\nColors Used Data:")
print(tabulate(colors_used_df.head(), headers='keys', tablefmt='pretty'))

print("\nSubject Matter Data:")
print(tabulate(subject_matter_df.head(), headers='keys', tablefmt='pretty'))

print("\nEpisode Dates Data:")
print(tabulate(episode_dates_df.head(), headers='keys', tablefmt='pretty'))
