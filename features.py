'''a list of functions that take a pandas dataframe'''

def mean_torque(df):
    return df.torque.mean()


def the_99th_percentile_torque(df):
    return df.torque.quantile(0.99)


def max_rate_of_change_of_torque(df):
    return df.torque.diff().max()


feature_input = {'mean_torque': mean_torque,
                 'the_99th_percentile_torque': the_99th_percentile_torque,
                 'max_rate_of_change_of_torque': max_rate_of_change_of_torque}
