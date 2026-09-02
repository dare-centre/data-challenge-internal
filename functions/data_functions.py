import os
import pandas as pd

###############################################################################
###############################################################################

def load_raw_data():
    '''
    Load the data from the root directory
    '''
    raw_data = pd.read_csv(
        os.path.join(
            'data','raw_data',
            'MiningProcess_Flotation_Plant_Database.csv'
        ),
        decimal=',',index_col=0,parse_dates=True
    )
    return raw_data

###############################################################################
###############################################################################

def load_daily_data():
    '''
    Load the hourly ddata
    '''
    train_x = pd.read_csv(
        os.path.join(
            'data',
            'daily_train_X_data.csv'
        ),
        index_col=0,parse_dates=True
    )
    train_y = pd.read_csv(
        os.path.join(
            'data',
            'daily_train_y_data.csv'
        ),
        index_col=0,parse_dates=True
    )

    test_x = pd.read_csv(
        os.path.join(
            'data',
            'daily_test_X_data.csv'
        ),
        index_col=0,parse_dates=True
    )
    test_y = pd.read_csv(
        os.path.join(
            'data',
            'daily_test_y_data.csv'
        ),
        index_col=0,parse_dates=True
    )

    return train_x, train_y, test_x, test_y

###############################################################################
###############################################################################



###############################################################################
###############################################################################
