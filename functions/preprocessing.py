import os, glob
import pandas as pd
import numpy as np

################################################################################
################################################################################
##############################   MAIN FUNCTIONS   ##############################
################################################################################
################################################################################

def load_environode(data_dir,filestub,utc_to_aest=True):
    """
    Load downloaded data from Environode
    Input:
        - data_dir: directory where data is stored
        - filestub: filestub of data to load
        - utc_to_aest: convert data in UTC to AEST
    """

    files = glob.glob(os.path.join(data_dir,'{}*.csv'.format(filestub)))

    data_comb = []
    for this_file in files:
        print(this_file)
        data_in = pd.read_csv(this_file)
        data_comb.append(data_in)

    # merge files
    data_comb = pd.concat(data_comb).drop_duplicates()

    # add in date
    data_comb.sort_values(by='timestamp',inplace=True)
    if utc_to_aest:
        data_comb['Date'] = pd.to_datetime(data_comb['timestamp'],unit='ms',utc=True).dt.tz_convert('Australia/Sydney')
    else:
        data_comb['Date'] = pd.to_datetime(data_comb['timestamp'],unit='ms')
    return data_comb

################################################################################
################################################################################

def convert_environode_daily(data_in,type='9am',buffer=8):
    '''
    Convert data from Environode to daily - this makes clear the format
    of the Environode data (and rounding errors etc that the data has) and 
    works with the ol' 9am-9am rainfall data
    Input:
        - data_in: dict of dataframes of Environode data
        - type: type of data to average - either 'daily' or '9am'
        - buffer: number of minutes to subtract from each timestamp to ensure the 
        last observation at 9am remains in the correct day
    '''
    # load data
    # lets do a little work here - namely we would like daily means
    daily_data = []
    print('Summarising daily data per device - {} gauges'.format(len(data_in['device'].unique())))
    for this_device in data_in['device'].unique():
        dev_daily = data_in.query('device == @this_device').copy().set_index('Date')
        dev_daily = daily_averaging(dev_daily,type=type,buffer=buffer)
        # remove duplicates
        dev_daily = dev_daily.loc[~dev_daily.index.duplicated(keep='first'),:]
        # ensure we have every day
        dev_daily.index = dev_daily.index.tz_localize(None)
        dev_daily = dev_daily.reindex(
            pd.date_range(
                data_in['Date'].min().strftime('%Y-%m-%d'),
                data_in['Date'].max().strftime('%Y-%m-%d'),
                freq='D'
            ),
            fill_value=np.nan
        )
        dev_daily.index.name = 'Date'
        dev_daily.reset_index(inplace=True)
        # device col is never lost        
        print('Gauge: {} start: {} end: {}'.format(this_device,dev_daily['Date'].min(),dev_daily['Date'].max()))
        dev_daily.loc[:,'device'] = this_device
        daily_data.append(dev_daily)
    # combine and serve
    daily_data = pd.concat(daily_data,axis=0,ignore_index=True)
    return daily_data

################################################################################
################################################################################

col_convert_df = {
    'Time': 'Date',
    ' Rain Since 9am (mm)': 'rain',
    ' Temperature (C)': 'temp',
    ' Rel Humidity (%)': 'relhumidity',
    ' Solar Rad (kWh/m^2)': 'solarrad'
}

def load_llara_gauges(data_dir,gauge_names,col_convert=col_convert_df):
    '''
    Load data from the LLARA gauges
    Input:
        - data_dir: directory where data is stored
        - gauge_names: dict of gauge names and short names
        - col_convert: dict of column names ingest/convert names
    '''
    llara_data = []
    for short_name, this_gauge in gauge_names.items():
        print(this_gauge)
        # read only specific columns and ensure ? = NaN
        llara_data_tmp = pd.read_csv(
            os.path.join(data_dir,'llara',this_gauge),
            skiprows=3, index_col=0, parse_dates=True, 
            na_values=' ?',
            usecols = list(col_convert.keys()) 
        )
        llara_data_tmp.rename(columns=col_convert,inplace=True)
        # average rainfall over the day
        llara_data_rain = daily_averaging(llara_data_tmp[['rain']],type='9am',buffer=5)
        # average the others by day - need to discuss this strategy
        llara_data_other = daily_averaging(llara_data_tmp.drop(columns=['rain']),type='9am-mean')
        llara_data_tmp = pd.concat([llara_data_rain,llara_data_other],axis=1)

        llara_data_tmp.rename(
            columns={_: '{}_{}'.format(_,short_name) for _ in col_convert.values()},
            inplace=True)
        
        llara_data.append(llara_data_tmp)
    llara_data = pd.concat(llara_data,axis=1) 
    return llara_data

################################################################################
################################################################################

col_convert_silodf = {
    'Date': 'Date',
    'Rain': 'rain',
    'T.Max': 'tempmax',
    'T.Min': 'tempmin',
    'Evap': 'evap',
}

def load_silo_gauges(data_dir,gauge_names,col_convert=col_convert_silodf):
    # We will also load the silo data for the same period
    silo_data = []
    for short_name, this_gauge in gauge_names.items():
        silo_tmp = pd.read_csv(
            os.path.join(data_dir,'silo','{}'.format(this_gauge)),
            skiprows=35, index_col=0, parse_dates=True, delim_whitespace=True,
            usecols=list(col_convert.keys())
        )
        # rename to indicate gauge
        silo_tmp.rename(columns=col_convert,inplace=True)
        silo_tmp.rename(
            columns={_: '{}_{}'.format(_,short_name) for _ in col_convert.values()},
            inplace=True)
        silo_data.append(silo_tmp)
    silo_data = pd.concat(silo_data,axis=1)
    return silo_data

################################################################################
################################################################################
#############################   HELPER FUNCTIONS   #############################
################################################################################
################################################################################

def daily_averaging(daily_data,type='daily',buffer=8):
    '''
    Provide a daily average of the data
    Input:
        - daily_data: dataframe of daily data
        - type: type of data to average - either 'daily' or '9am'
        - buffer: number of minutes to subtract from each timestamp to ensure the 
        last observation at 9am remains in the correct day (important for a 
        cumulative variable like rainfall)
    '''
    if '9am' in type:
        daily_data.index = daily_data.index.round(freq='1T',ambiguous='NaT')
        # Rainfall resets at 9 AM local (9 AM even during DST) and is reported as the rainfall on the 
        # day of 9am finish so we need to shift by 24-9 hours to make the end time midnight
        # and incldue a little buffer less than the sample time Environode tends to 
        # count e.g., 09:00:02 as inclusive in the previous day's rainfall
        daily_data.index = daily_data.index.shift(24-9,freq='H').shift(-buffer,freq='T')
        # now we can simply take the daily max having shifted our local 9 AM to midnight
        if type == '9am-mean':
            daily_data = daily_data.resample('D').mean()
        else:
            daily_data = daily_data.resample('D').max()
    elif type == 'daily':
        daily_data = daily_data.resample('D').mean()
    
    return daily_data

################################################################################
################################################################################

import base64

def cheeky_check(str_in):
    if not type(str_in) is str:
        return False
    if base64.b64encode(str_in.encode("utf-8")) == b'b3BlbnNlc2FtZQ==':
        return True
    else:
        return False

################################################################################
################################################################################
