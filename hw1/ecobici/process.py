import os
import glob
import pandas as pd

data_folder = "data"
all_files = glob.glob(os.path.join(data_folder, "*.csv"))

print(all_files)

df = pd.concat((pd.read_csv(f, low_memory=False) for f in all_files))
df.to_csv("data.csv", index=False)
