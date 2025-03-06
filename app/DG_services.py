import pandas as pd

def get_diversity_weights(province):
    df = pd.read_csv(r"app\static\diversity_weights_2023.csv")
    row = df[df["Province or territory of work"] == province]
    if not row.empty:
        return row.iloc[0, 1:].tolist()
    else:
        return [0,0,0,0]
