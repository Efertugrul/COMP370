import argparse
import pandas as pd 

boroughs = ["MANHATTAN", "BRONX", "BROOKLYN", "QUEENS", "STATEN ISLAND"]

def parse():
    parser = argparse.ArgumentParser(description= "Complaints per borough given a date range.")
    parser.add_argument('-i', '--input', required=True, help= 'Path to input CSV.')
    parser.add_argument('-s', '--start', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('-e', '--end', required=True, help='End date (YYYY-MM-DD)')
    parser.add_argument('-o', '--output', help='Optional output CSV file path')

    return parser.parse_args()


def filter(df, start, end):
    if 1 not in df.columns:
        raise ValueError()

    df[1] = pd.to_datetime(df[1], errors='coerce')
    df =  df[df[1].notna()]
    return df[(df[1] >= start) & (df[1] <= end)]

def find(row):
    for col in range(len(row)):
        parts = str(row[col]).strip().upper().split(',')
        for part in parts:
            part = part.strip()
            if part in boroughs:
                return part
    return None

def count(df):
    c = []
    for i, row in df.iterrows():
        complaint_type = row[5]
        borough = find(row)

        if borough:
            c.append([complaint_type, borough])
    res = pd.DataFrame(c, columns=['complaint type', 'borough'])
    return res.groupby(['complaint type', 'borough']).size().reset_index(name = 'count')


def output(df, file = None):
    if file:
        df.to_csv(file, index= False)
    else:
        print(df.to_csv(index = False))

def main():
    args = parse()
    df = pd.read_csv(args.input, header=None, low_memory=False)
    filtered = filter(df,args.start, args.end)
    complaint_count = count(filtered)
    output(complaint_count, args.output)

if __name__ == '__main__':
    main()


#3.147.48.105