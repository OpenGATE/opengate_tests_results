from datetime import datetime
import glob
import pandas as pd
import numpy as np
import altair as alt
import json
import shutil

def custom_and(x, y):
    if x == "" and y == "":
        return ""
    elif x == "":
        return y
    elif y == "":
        return x
    else:
        return (x and y)

# Import all results from different platform and create 1 result
files = glob.glob("dashboard_output_*.json")
intermediate_results = {}
for file in files:
    print(file)
    json_file = open(file, 'r')
    results2 = json.load(json_file)
    for key in results2.keys():
        if key in intermediate_results.keys():
            intermediate_results[key] = [custom_and(intermediate_results[key][0], results2[key][0])]
        else:
            intermediate_results[key] = [results2[key][0]]
    json_file.close()

# Add the result to the previous results
json_file_results = open('results.json', 'r')
results = json.load(json_file_results)
results["date"] = [datetime.now().strftime("%Y/%m/%d, %H:%M:%S")] + results["date"]
for key in results.keys():
    if key in intermediate_results.keys():
        results[key] = [intermediate_results[key][0]] + results[key]
    elif "date" not in key:
        results[key] = [""] + results[key]
for key in intermediate_results.keys():
    if key not in results.keys():
        results[key] = ["" for i in range(len(results["date"]))]
        results[key][0] = intermediate_results[key][0]
with open('results_save.json', 'w') as json_file_output:
    json.dump(results, json_file_output, indent=4)
json_file_results.close()
shutil.move('results_save.json', 'results.json')

# Create the DataFrame
json_file_results = open('results.json', 'r')
results = json.load(json_file_results)
source = pd.DataFrame(data=results)
print(source)

# Display the graph
source = source.reset_index()
source["index"].values[::-1]
source = source.melt(['index','date'], var_name='test', value_name='is_ok')
print(source)

domain = ["", False, True]
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

chart.save('index.html')

