import pandas as pd

# FIXME: fix errors when served with Nginx
def slice_dataset(path, group_by):
    df = pd.read_csv(path)
    # map indices to headers
    col = df.columns
    if (group_by == '[]'):
        return ['[]']
    group_by_indices = list(map(lambda x: col[int(x)], group_by.strip('][').split(',')))
    return df.groupby(group_by_indices).groups.keys()

def get_sliced_dataset(path, group_by_key, group_by_val):
    df = pd.read_csv(path)
    # map indices to headers
    col = df.columns
    if group_by_key == '[]':
        return df
    group_by_indices = list(map(lambda x: col[int(x)], group_by_key.strip('][').split(',')))
    return df.take(df.groupby(group_by_indices).groups[eval(group_by_val)])

def preview(path, num=5):
    df = pd.read_csv(path)
    return df.head(num)

def str2list(job_obj):
    groupby_key = job_obj.groupby_indexs
    groupby_key = str2listofint(groupby_key)
    target_idx = int(job_obj.target_indexs.strip('][').split(',')[0])
    ts_idx = int(job_obj.timestamp_indexs.strip('][').split(',')[0])
    return groupby_key, target_idx, ts_idx

def str2listofint(a):
    if a.strip('][').split(',') == ['']:
        a = []
    else:
        a = a.strip('][').split(',')
    return a

"""
handle missing values
"""
# FIXME: fix errors when served with Nginx
def preprocess(path):
    df = pd.read_csv(path)
    df.fillna(method='pad')
    df.to_csv(path)

def user_file_path(userID, file_name):
    return 'user_{0}/{1}'.format(userID, filename)

def model_file_path(user_id, model_id, model_name):
    return 'user_{0}/{1}/{2}'.format(user_id, model_name, model_id)