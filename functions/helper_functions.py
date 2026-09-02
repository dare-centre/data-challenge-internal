import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


from functions.plotting_functions import plot_model_fit
from functions.preprocessing import cheeky_check

###############################################################################
###############################################################################

def calculate_model_performance(y_obs, y_mod, **kwargs):
    '''
    Calculate the model performance metrics:
    - BSS
    - R2
    - RMSE
    - MAE
    '''
    # Calculate the metrics
    bss = 1 - (np.sum((y_obs[1:] - y_mod[1:])**2) / np.sum((y_obs[1:]-y_obs[:-1])**2))
    r2 = r2_score(y_obs, y_mod)
    rmse = np.sqrt(mean_squared_error(y_obs, y_mod))
    mae = mean_absolute_error(y_obs, y_mod)
    metrics_out = {
        'bss': bss,
        'r2': r2,
        'rmse': rmse,
        'mae': mae
    }
    return metrics_out

###############################################################################
###############################################################################

def assess_model_prediction(pred_dict_in, test=None, **kwargs):
    '''
    Plot the model performance for training, validation and test data.
    Return the metrics for model performance.
    Input:
        - pred_dict: A dictionary with:
            - train_y: observed values for training data
            - train_y_pred: predicted values for training data
            - val_y: observed values for validation data
            - val_y_pred: predicted values for validation data
            - test_y: observed values for test data
            - test_y_pred: predicted values for test data
        - test: None - provide password to get test set results
    Output:
        - metrics: A pandas dataframe with:
            - BSS
            - R2
            - RMSE
            - MAE
        - plots for train, validation and test performance
    '''
    # deal with residual dataframes
    pred_dict = {k: v.values if isinstance(v, pd.DataFrame) or isinstance(v, pd.Series) else v for k, v in pred_dict_in.items()}

    # Calculate the metrics
    if not pred_dict['train_y'] is None:
        train_metrics = calculate_model_performance(
            pred_dict['train_y'], pred_dict['train_y_pred']
        )
        plot_model_fit(
            pred_dict['train_time'],pred_dict['train_y'], pred_dict['train_y_pred'], mod_metrics=train_metrics,
            title='Model fit for training data'
        )
    else:
        train_metrics = None
    if not pred_dict['val_y'] is None:
        val_metrics = calculate_model_performance(
            pred_dict['val_y'], pred_dict['val_y_pred']
        )
        plot_model_fit(
            pred_dict['val_time'],pred_dict['val_y'], pred_dict['val_y_pred'], mod_metrics=val_metrics,
            title='Model fit for validation data'
        )
    else:
        val_metrics = None
    test_bool = cheeky_check(test)
    if not pred_dict['test_y'] is None and test_bool:
        test_metrics = calculate_model_performance(
            pred_dict['test_y'], pred_dict['test_y_pred']
        )
        plot_model_fit(
            pred_dict['test_time'],pred_dict['test_y'], pred_dict['test_y_pred'], mod_metrics=test_metrics,
            title='Model fit for test data'
        )
    else:
        test_metrics = None
    
    # construct pandas dataframe
    metrics = pd.DataFrame(
        {
            'Train': train_metrics,
            'Validation': val_metrics,
            'Test': test_metrics
         }
    )
    metrics.index = [_.upper() for _ in metrics.index]

    return metrics

###############################################################################
###############################################################################

def inversescaler_pred_dict(predicted_data, scaler=None):
    '''
    Construct a dictionary with the model predictions and inverse transform if needed.
    '''
    if not scaler is None:
        predicted_data['train_y'] = scaler.inverse_transform(predicted_data['train_y'])
        predicted_data['train_y_pred'] = scaler.inverse_transform(predicted_data['train_y_pred'].reshape(-1,1))
        predicted_data['test_y'] = scaler.inverse_transform(predicted_data['test_y'])
        predicted_data['test_y_pred'] = scaler.inverse_transform(predicted_data['test_y_pred'].reshape(-1,1))
        if not predicted_data['val_y'] is None:
            predicted_data['val_y'] = scaler.inverse_transform(predicted_data['val_y'])
            predicted_data['val_y_pred'] = scaler.inverse_transform(predicted_data['val_y_pred'].reshape(-1,1))

    return predicted_data

###############################################################################
###############################################################################
