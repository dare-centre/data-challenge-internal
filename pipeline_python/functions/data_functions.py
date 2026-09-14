import os

import pandas as pd

###############################################################################
###############################################################################


def load_daily_data():
    """
    Load the daily data.
    """
    # Accommodate data access from a child directory or a grandchild directory.
    target_directory = "../data"
    if not os.path.isdir(target_directory):
        # Accommodate "data" access from one level down the directory tree.
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        target_directory = os.path.join(parent_directory, target_directory)

    # Manage Pandas data imports via a dictionary.
    dict_import = {
        "train_x": pd.DataFrame(),
        "train_y": pd.DataFrame(),
        "test_x": pd.DataFrame(),
        "test_y": pd.DataFrame()
    }

    for target_file in dict_import:
        try:
            # Attempt data import.
            target_filepath = os.path.join(
                target_directory, "".join(["daily_", target_file, "_data.csv"])
            )
            dict_import[target_file] = pd.read_csv(target_filepath, index_col=0, parse_dates=True)

        except FileNotFoundError:
            # Handle missing files.
            dict_import[target_file] = pd.DataFrame()
            print(f"Error. Missing file: {target_filepath}.")

        except pd.errors.EmptyDataError:
            # Handle accessible, but empty files.
            print(f"Warning. Empty file: {target_filepath}.")

    return (
        dict_import["train_x"],
        dict_import["train_y"],
        dict_import["test_x"],
        dict_import["test_y"]
    )

###############################################################################
###############################################################################
