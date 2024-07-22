from datetime import datetime
import glob
import pandas as pd
import numpy as np
import altair as alt

def custom_and(x, y):
    if x[0] != x[0] and y[0]  != y[0]:
        return pd.Series([None])
    elif x[0] != x[0]:
        return y
    elif y[0] != y[0]:
        return x
    else:
        return pd.Series([x[0] and y[0]])

# Import all results from different platform and create 1 result
files = glob.glob("results_*.csv")
df = pd.read_csv(files[0], index_col=0, parse_dates=[0])
for file in files[1:]:
    df2 = pd.read_csv(file, index_col=0, parse_dates=[0])
    df = df.combine(df2, custom_and)
df.insert(0, "date", datetime.now())

# Add the result to the previous results
df_results = pd.read_csv("results.csv", index_col=0, parse_dates=[0])
frames = [df, df_results]
df_results = pd.concat(frames, ignore_index=True)
outputCsvFile = "results.csv"
df_results.to_csv(outputCsvFile)

# Display the graph
source = pd.read_csv(outputCsvFile, index_col=0, parse_dates=True)
source = source.reset_index()
source["index"].values[::-1]
source = source.melt(['index','date'], var_name='test', value_name='is_ok')

domain = [np.nan, False, True]
range_ = ['grey', 'red', 'green']

chart = alt.Chart(source, title="History of tests").mark_rect().encode(
    alt.X("index:O").title("Date"),
    alt.Y("test:N").title("Tests"),
    alt.Color("is_ok:O").title(None).scale(domain=domain, range=range_),
    tooltip=[
        alt.Tooltip("monthdate(date)", title="Date"),
        alt.Tooltip("is_ok:O", title="OK"),
    ],
).configure_view(
    step=13,
    strokeWidth=0
).configure_axis(
    domain=False
)

chart.save('chart.html')

