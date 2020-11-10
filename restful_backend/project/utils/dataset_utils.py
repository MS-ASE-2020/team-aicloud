import pandas as pd

def slice_dataset(path, group_by):
    df = pd.read_csv(path)
    # map indices to headers
    col = df.columns
    group_by_indices = list(map(lambda x: col[int(x)], group_by.strip('][').split(',')))
    return df.groupby(group_by_indices).groups.keys()

def get_sliced_dataset(path, group_by_key, group_by_val):
    df = pd.read_csv(path)
    # map indices to headers
    col = df.columns
    group_by_indices = list(map(lambda x: col[int(x)], group_by_key.strip('][').split(',')))
    return df.take(df.groupby(group_by_indices).groups[eval(group_by_val)])

def preview(path, num=5):
    df = pd.read_csv(path)
    return df.head(num)
