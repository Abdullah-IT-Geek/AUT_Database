from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from dash import dash_table
from plotly.subplots import make_subplots
import pandas as pd
import json

# 🗂️ Lade deine echten Daten aus mqtt_data.json
with open("mqtt_data.json", "r") as f:
    data = json.load(f)

# --- Final Weight DataFrame ---
final_weight_entries = data.get("final_weight", {})
final_weight_df = pd.DataFrame([
    {
        "bottle": entry["bottle"],
        "time": pd.to_datetime(entry["time"], unit="s"),
        "final_weight": entry["final_weight"]
    }
    for entry in final_weight_entries.values()
])

# --- Drop Oscillation DataFrame ---
drop_oscillation_entries = data.get("drop_oscillation", {})
drop_data = []
for entry in drop_oscillation_entries.values():
    bottle_id = entry.get("bottle")
    for i, val in enumerate(entry.get("drop_oscillation", [])):
        drop_data.append({
            "bottle": bottle_id,
            "sample": i,
            "oscillation": float(val)
        })
drop_df = pd.DataFrame(drop_data)


ground_truth_entries = data.get("ground_truth",{})
ground_truth_df = pd.DataFrame([
    {
        "bottle": entry["bottle"],
        "is_cracked": entry["is_cracked"]
    }
    for entry in ground_truth_entries.values()
])

dispencer_blue_entries = data.get("dispenser_blue",{})
dispenser_blue_df = pd.DataFrame([
    {
        "dispenser": entry["dispenser"],
        "bottle": entry["bottle"],
        "time": entry["time"],
        "fill_level_grams": entry["fill_level_grams"],
        "recipe": entry["recipe"],
        "vibration-index": entry["vibration-index"]
    }
    for entry in dispencer_blue_entries.values()
])

dispencer_green_entries = data.get("dispenser_green",{})
dispenser_green_df = pd.DataFrame([
    {
        "dispenser": entry["dispenser"],
        "bottle": entry["bottle"],
        "time": entry["time"],
        "fill_level_grams": entry["fill_level_grams"],
        "recipe": entry["recipe"],
        "vibration-index": entry["vibration-index"]
    }
    for entry in dispencer_green_entries.values()
])   

dispencer_red_entries = data.get("dispenser_blue",{})
dispenser_red_df = pd.DataFrame([
    {
        "dispenser": entry["dispenser"],
        "bottle": entry["bottle"],
        "time": entry["time"],
        "fill_level_grams": entry["fill_level_grams"],
        "recipe": entry["recipe"],
        "vibration-index": entry["vibration-index"]
    }
    for entry in dispencer_red_entries.values()
])  

temperature_entries = data.get("temperature",{})
temperature_df = pd.DataFrame([
    {
        "dispenser": entry["dispenser"],
        "time": entry["time"],
        "temperature_C": entry["temperature_C"]
    }
    for entry in temperature_entries.values()
])

df_dis_red = pd.merge(dispencer_red_entries, temperature_df, on="dispenser")
df_dis_blue = pd.merge(dispencer_blue_entries, temperature_df, on="dispenser")
df_dis_green = pd.merge(dispencer_green_entries, temperature_df, on="dispenser")

app = Dash(__name__)

# Liste der einzigartigen Bottle-IDs für Dropdown
bottles_unique = pd.concat([final_weight_df["bottle"], drop_df["bottle"]]).unique()

# 🔧 Layout
app.layout = html.Div([
    html.H1("Bottle Data Dashboard"),
    dcc.Dropdown(
        id="bottle-dropdown",
        options=[{"label": b, "value": b} for b in bottles_unique],
        value=bottles_unique[0]
    ),
    dcc.Graph(id="bottle-graph"),
    html.H2("Final Weight Tabelle"),
        dash_table.DataTable(
        data=final_weight_df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in final_weight_df.columns],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"}
    ),
])

# 🔄 Callback
@app.callback(
    Output("bottle-graph", "figure"),
    Input("bottle-dropdown", "value")
)
def update_graph(bottle_to_plot):
    fw = final_weight_df[final_weight_df["bottle"] == bottle_to_plot]
    osc = drop_df[drop_df["bottle"] == bottle_to_plot]

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Final Weight", "Drop Oscillation"))

    # Final Weight Plot
    if not fw.empty:
        fig.add_trace(
            go.Scatter(
                x=fw["time"],
                y=fw["final_weight"],
                mode="lines+markers",
                name="Final Weight"
            ),
            row=1, col=1
        )
    else:
        fig.add_annotation(
            text="Kein Final Weight vorhanden",
            x=0.5, y=0.5, showarrow=False,
            xref="x1 domain", yref="y1 domain",
            row=1, col=1
        )

    # Drop Oscillation Plot
    if not osc.empty:
        fig.add_trace(
            go.Scatter(
                x=osc["sample"],
                y=osc["oscillation"],
                mode="lines+markers",
                name="Drop Oscillation"
            ),
            row=1, col=2
        )
    else:
        fig.add_annotation(
            text="Keine Drop Oscillation vorhanden",
            x=0.5, y=0.5, showarrow=False,
            xref="x2 domain", yref="y2 domain",
            row=1, col=2
        )

    fig.update_layout(title_text=f"Plots für Bottle {bottle_to_plot}")

    return fig

#App starten
if __name__ == '__main__':
    app.run(debug=True)
