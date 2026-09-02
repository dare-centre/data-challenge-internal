
###############################################################################
###############################################################################

append_rows <- function(df_input, n) {

  # Append n empty rows to an input dataframe.

  for (i in 1:n) {
    df_input[nrow(df_input) + 1, ] <- NA
  }

  return(df_input)

}

###############################################################################
###############################################################################

calculate_model_performance <- function(y_obs, y_mod) {

  # Calculate the model performance metrics:
  #  - BSS
  #  - R2
  #  - RMSE
  #  - MAE

  # Calculate the metrics

  bss <- 1 - {sum((y_obs[-1, ] - y_mod[-1, ])^2) / sum((y_obs[-1, ] - head(y_obs, -1))^2)}

  y_obs <- as.vector(y_obs[,1])
  y_mod <- as.vector(y_mod[,1])

  r2 <- MLmetrics::R2_Score(y_obs, y_mod)
  rmse <- Metrics::rmse(y_obs, y_mod)
  mae <- Metrics::mae(y_obs, y_mod)
  metrics_out <- list(
    "bss" = bss,
    "r2" = r2,
    "rmse" = rmse,
    "mae" = mae
  )
  return(metrics_out)
}

###############################################################################
###############################################################################

assess_model_prediction <- function(predictor, test = NULL) {

  # Plot the model performance for training, validation and test data.
  # Return the metrics for model performance.
  # Input:
  #    - predictor: A dataframe with,
  #        - train_y       observed values for training data
  #        - train_y_pred  predicted values for training data
  #        - val_y         observed values for validation data
  #        - val_y_pred    predicted values for validation data
  #        - test_y        observed values for test data
  #        - test_y_pred   predicted values for test data
  #   - test: NULL - provide password to get test set results
  # Output:
  #    - metrics: A dataframe with,
  #        - BSS
  #        - R2
  #        - RMSE
  #        - MAE
  #    - plots for train, validation and test performance

  # Calculate the metrics
  if (exists("train_y", predictor)) {
    train_metrics <- calculate_model_performance(
      predictor$train_y, predictor$train_y_pred
    )
    plot_model_fit(
      predictor$train_time, predictor$train_y[,1], predictor$train_y_pred[,1],
      mod_metrics = train_metrics,
      title = "Model fit for training data"
    )
  } else {
    train_metrics <- NULL
  }
  if (exists("val_y", predictor)) {
    val_metrics <- calculate_model_performance(
      predictor$val_y, predictor$val_y_pred
    )
    plot_model_fit(
      predictor$val_time, predictor$val_y[,1], predictor$val_y_pred[,1],
      mod_metrics = val_metrics,
      title = "Model fit for validation data"
    )
  } else {
    val_metrics <- NULL
  }
  test_bool <- cheeky_check(test)
  if (exists("test_y", predictor) & test_bool) {
    test_metrics <- calculate_model_performance(
      predictor$test_y, predictor$test_y_pred
    )
    plot_model_fit(
      predictor$test_time, predictor$test_y[,1], predictor$test_y_pred[,1],
      mod_metrics = test_metrics,
      title = "Model fit for test data"
    )
  } else {
    test_metrics <- NULL
  }

  # construct list
  metrics <- list(
    "Train" = train_metrics,
    "Validation" = val_metrics,
    "Test" = test_metrics
  )

  return(metrics)
}

###############################################################################
###############################################################################

inversescaler_predictor <- function(predictor, scaler) {

  # Inverse scale selected predictor dataframe columns.

  predictor$train_y[,1] <- DescTools::StripAttr(datawizard::rescale(predictor$train_y, to = scaler))
  predictor$train_y_pred[,1] <- DescTools::StripAttr(datawizard::rescale(predictor$train_y_pred, to = scaler))
  predictor$test_y[,1] <- DescTools::StripAttr(datawizard::rescale(predictor$test_y, to = scaler))
  predictor$test_y_pred[,1] <- DescTools::StripAttr(datawizard::rescale(predictor$test_y_pred, to = scaler))

  if (exists("val_y", predictor)) {
    predictor$val_y[,1] <- DescTools::StripAttr(datawizard::rescale(predictor$val_y, to = scaler))
    predictor$val_y_pred[,1] <- DescTools::StripAttr(datawizard::rescale(predictor$val_y_pred, to = scaler))
  }

  return(predictor)
}
