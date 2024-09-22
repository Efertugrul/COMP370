import pandas as pd

df = pd.read_csv('../../trimmed_2020_dataset.csv', header=None)

df[1] = pd.to_datetime(df[1], errors='coerce')
df[2] = pd.to_datetime(df[2], errors='coerce')
df[8] = pd.to_numeric(df[8], errors='coerce')


df = df.dropna(subset=[1,2,8])
df[8] = df[8].astype(int)
df['response time'] = (df[2] - df[1]).dt.total_seconds() / 3600
df = df[df['response time'] > 0]

df['month'] = df[1].dt.to_period('M')

df = df.rename(columns={8: 'zip_code'})

res_time_monthly = df.groupby(['month', 'zip_code'])['response time'].mean().reset_index()

res_time_monthly.to_csv('monthly_res_t.csv', index=False)