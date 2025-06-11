import pandas as pd
import json
import matplotlib.pyplot as plt

# Pfad zur JSON-Datei
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

# --- Bottle-ID auswählen und plotten ---
bottle_to_plot = "49632838"

# Plot final weight (falls vorhanden)
fw = final_weight_df[final_weight_df["bottle"] == bottle_to_plot]
if not fw.empty:
    plt.figure()
    plt.plot(fw["time"], fw["final_weight"], marker="o")
    plt.title(f"Final Weight – Bottle {bottle_to_plot}")
    plt.xlabel("Zeit")
    plt.ylabel("Gewicht [g]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print(f"❌ Kein Final Weight für Bottle {bottle_to_plot}")

# Plot drop oscillation (falls vorhanden)
osc = drop_df[drop_df["bottle"] == bottle_to_plot]
if not osc.empty:
    plt.figure()
    plt.plot(osc["sample"], osc["oscillation"])
    plt.title(f"Drop Oscillation – Bottle {bottle_to_plot}")
    plt.xlabel("Sample #")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print(f"❌ Keine Drop-Oszillation für Bottle {bottle_to_plot}")
