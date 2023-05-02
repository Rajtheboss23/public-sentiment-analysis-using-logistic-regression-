import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create a sample dataset
data = pd.read_csv(r"D:\News Sentiment\UserInterface\static\results\save.csv")

data["Sentiment"].replace({"Positive":4,"Negative":0,"Neutral":2}, inplace=True)
data.drop('Unnamed: 0', axis=1, inplace=True)
data.drop(["Posts", "PreprocessedPosts", "Source"], axis=1, inplace=True)
data.sort_values(by=['Sentiment'], inplace=True)

# Create a dataframe from the dataset
df = pd.DataFrame(data)

# Create the heatmap using seaborn
sns.heatmap(df, cmap="YlGnBu")

# Add labels and title

plt.ylabel("Index")
plt.title("Sentiment Heatmap")

# Show the plot
plt.show()
