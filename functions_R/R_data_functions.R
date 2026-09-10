
###############################################################################
###############################################################################

csv_to_dataframe <- function(file_name) {

  # Get data from a CSV file and convert it to a dataframe.

  # Build data paths with "here::here" for:
  # a) multiplatform portability,
  # b) starting directory flexibility.
  file_path <- here::here("data", file_name)

  # Attempt data import.
  df <- tryCatch({
    # Handle missing files.
    if (!file.exists(file_path)) {
      cat("Error. Missing file: ", file_path, ".", sep = "")
      return(data.frame())
    }

    # Handle accessible, but empty files.
    if (file.info(file_path)$size == 0) {
      cat("Warning. Empty file: ", file_path, ".", sep = "")
      return(data.frame())
    }

    # Get data.
    suppressMessages(
      as.data.frame(readr::read_csv(
        file = file_path,
        show_col_types = FALSE
      ))
    )

  }, error = function(e) {
    cat("Error. File: ", file_name, ". Message: ", e$message, sep = "")
    return(data.frame())
  })

}

###############################################################################
###############################################################################

load_daily_data <- function() {

  # Load the daily data.

  # Manage data imports via a list.
  list_import <- list(
    train_x = data.frame(),
    train_y = data.frame(),
    test_x = data.frame(),
    test_y = data.frame()
  )

  for (nm in names(list_import)) {

    # Attempt data import.
    list_import[[nm]] <- csv_to_dataframe(paste0("daily_", nm, "_data.csv"))

    # Convert date columns to row indices.
    row.names(list_import[[nm]]) <- dplyr::pull(
      list_import[[nm]], colnames(list_import[[nm]])[1]
    )
    list_import[[nm]] <- dplyr::select(list_import[[nm]], -1)

    # Remove spaces from column names.
    colnames(list_import[[nm]]) <- make.names(
      colnames(list_import[[nm]]), unique = TRUE
    )
  }

  list_import
}

###############################################################################
###############################################################################
