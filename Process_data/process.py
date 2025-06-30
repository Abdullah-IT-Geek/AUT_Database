import pandas as pd
import json
import matplotlib.pyplot as plt


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
drop_entries = data.get("drop_oscillation", {})
drop_data = []
for entry in drop_entries.values():
    bottle_id = entry.get("bottle")
    for i, val in enumerate(entry.get("drop_oscillation", [])):
        drop_data.append({
            "bottle": bottle_id,
            "sample": i,
            "oscillation": float(val)
        })

drop_df = pd.DataFrame(drop_data)

table_bottle_unique = drop_df["bottle"].unique()
print("Eindeutige Bottle-IDs:", table_bottle_unique)


# Auswahl der ersten 4 Flaschen
bottle_id_table = table_bottle_unique[:4]

# Erstelle eine Figure mit 2 Subplots (1 Zeile, 2 Spalten)
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# -------- Final Weight Plot (linker Subplot) --------
for bottle_to_plot in bottle_id_table:
    fw = final_weight_df[final_weight_df["bottle"] == bottle_to_plot]
    if not fw.empty:
        axs[0].plot(fw["time"], fw["final_weight"], marker="o", label=f"Bottle {bottle_to_plot}")

axs[0].set_title("Final Weight – Erste 4 Bottles")
axs[0].set_xlabel("Zeit")
axs[0].set_ylabel("Gewicht [g]")
axs[0].legend()
axs[0].grid(True)

# -------- Drop Oscillation Plot (rechter Subplot) --------
for bottle_to_plot in bottle_id_table:
    osc = drop_df[drop_df["bottle"] == bottle_to_plot]
    if not osc.empty:
        axs[1].plot(osc["sample"], osc["oscillation"], label=f"Bottle {bottle_to_plot}")

axs[1].set_title("Drop Oscillation Erste 4 Bottles")
axs[1].set_xlabel("Sample")
axs[1].set_ylabel("Amplitude")
axs[1].legend()
axs[1].axhline(y=0, color='black', linestyle='--', linewidth=2, label="Null-Linie")
axs[1].grid(True)

plt.tight_layout()
plt.show()
