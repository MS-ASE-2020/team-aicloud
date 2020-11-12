def get_validation_period(ts_data):
    """
    Evaluate how long should be the validation data set
    @param ts_data: the time series data
    @return: an integer represents the last k points for validation
    """
    total_sum = sum(ts_data)
    total_points = len(ts_data)
    per_point_sum = total_sum / total_points
    min_points = 5
    max_points = 48
    tolerance = 0.8
    vpts = 0
    # limit the validation points to be at least 5 data points and at most 48 data points
    if total_points <= min_points:
        return min_points

    cumSum = sum(ts_data[-min_points+1:])
    for i in range(min_points, min(max_points, total_points)):
        vpts = i
        cumSum += ts_data[-i]
        threshold = per_point_sum * i * tolerance
        if cumSum >= threshold:
            break

    return vpts


def round_non_negative_int(arr):
    return [round(p) if p > 0 else 0 for p in arr]
