import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
filepath = 'medical_examination.csv'
df = pd.read_csv(filepath)

# Add 'overweight' column
height_metre = df['height'] / 100
df['overweight'] = df['weight'] / (height_metre * height_metre)
df['overweight'] = (df['overweight'] > 25).astype(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = (df['cholesterol'] != 1).astype(int)
df['gluc'] = (df['gluc'] != 1).astype(int)


# Draw Categorical Plot
def draw_cat_plot():
  # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
  col_to_melt = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
  df_cat = pd.melt(df, id_vars='cardio', value_vars=col_to_melt, var_name = 'variable', value_name = 'Categorical Value')

  # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
  df_grouped = df_cat.groupby(['cardio', 'variable', 'Categorical Value']).size().reset_index(name='total')

  # Draw the catplot with 'sns.catplot()'
  g = sns.catplot(x='variable', y='total', hue='Categorical Value', col='cardio',data=df_grouped, kind='bar', height=6, aspect=1)

  # Get the figure for the output
  fig = plt.gcf()

  # Do not modify the next two lines
  fig.savefig('Catplot.png')
  return fig



# Draw Heat Map
def draw_heat_map():
  # Clean the data
  df_heat = df.loc[(df['ap_lo'] <= df['ap_hi']) & 
                  (df['height'] >= df['height'].quantile(0.025)) & 
                  (df['height'] <= df['height'].quantile(0.975)) & 
                  (df['weight'] >= df['weight'].quantile(0.025)) & 
                  (df['weight'] <= df['weight'].quantile(0.975))]
  
  # df_heat = df[df['ap_lo'] <= df['ap_hi']]
  # df_heat = df_heat[df_heat['height'] >= df_heat['height'].quantile(0.025)]
  # df_heat = df_heat[df_heat['height'] <= df_heat['height'].quantile(0.975)]
  # df_heat = df_heat[df_heat['weight'] >= df_heat['weight'].quantile(0.025)]
  # df_heat = df_heat[df_heat['weight'] <= df_heat['weight'].quantile(0.975)]
  

  # Calculate the correlation matrix
  corr = df_heat.corr()

  # Generate a mask for the upper triangle
  mask = np.triu(corr)

  # Set up the matplotlib figure
  fig, ax = plt.subplots(figsize=(10, 8))

  # Draw the heatmap with 'sns.heatmap()'
  sns.heatmap(corr, annot=True, fmt='.1f', cmap='coolwarm', mask=mask, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": 0.7})

  # Do not modify the next two lines
  fig.savefig('heatmap.png')
  return fig
