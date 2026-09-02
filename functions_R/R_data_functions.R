
###############################################################################
###############################################################################

# Legacy function, currently disabled.

#load_raw_data <- function() {
#
#  # Define a NULL variable reference to provide more graceful error
#  # handling in the event of failed data import.
#  raw_data <- NULL
#
#  # N.B. Assumes a header row is present.
#  raw_data <- readr::read_csv(
#    file = Gmisc::pathJoin(
#      funr::get_script_path(), "data", "raw_data",
#      "MiningProcess_Flotation_Plant_Database.csv"
#    ),
#    locale = readr::locale(decimal_mark = ","),
#    show_col_types = FALSE
#  )
#
#  return(raw_data)
#}

###############################################################################
###############################################################################

csv_to_dataframe <- function(file_name) {

  # Get data from a CSV and convert it to a dataframe.

  # Get data.
  df <- suppressMessages(
    as.data.frame(readr::read_csv(
      file = Gmisc::pathJoin(
        here::here(), "data",
        file_name
      ),
      show_col_types = FALSE
    ))
  )

  return(df)
}

###############################################################################
###############################################################################

load_daily_data <- function() {

  # Load the hourly data

  # Import data
  train_x <- csv_to_dataframe("daily_train_X_data.csv")
  train_y <- csv_to_dataframe("daily_train_y_data.csv")
  test_x <- csv_to_dataframe("daily_test_X_data.csv")
  test_y <- csv_to_dataframe("daily_test_y_data.csv")

  # Convert date columns to row indices.
  #
  row.names(train_x) <- pull(train_x, colnames(train_x)[1])
  row.names(train_y) <- pull(train_y, colnames(train_y)[1])
  row.names(test_x) <- pull(test_x, colnames(test_x)[1])
  row.names(test_y) <- pull(test_y, colnames(test_y)[1])
  #
  train_x <- select(train_x, -1)
  train_y <- select(train_y, -1)
  test_x <- select(test_x, -1)
  test_y <- select(test_y, -1)

  # Remove spaces from column names.
  colnames(train_x) <- make.names(colnames(train_x), unique = TRUE)
  colnames(train_y) <- make.names(colnames(train_y), unique = TRUE)
  colnames(test_x) <- make.names(colnames(test_x), unique = TRUE)
  colnames(test_y) <- make.names(colnames(test_y), unique = TRUE)

  return(list("train_x" = train_x, "train_y" = train_y,
              "test_x" = test_x, "test_y" = test_y))
}

###############################################################################
###############################################################################
