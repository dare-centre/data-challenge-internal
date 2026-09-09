# DARE - Deluxe Data Challenge I

This repository contains the data and example code for the DARE Deluxe Data
Challenge I.

## Table of Contents

- [Data](#data)
- [Getting Started](#getting-started)
- [Glossary](#glossary)
- [Acknowledgements](#acknowledgements)

## Data

Data were prepared using the Jupyter notebook `00_Data_Preprocessing.ipynb`. We
will be using the files:

`data/daily_train_X_data.csv`\
`data/daily_train_y_data.csv`\
`data/daily_test_X_data.csv`\
`data/daily_test_y_data.csv`

## Getting Started

### Challenge

The challenge should be attempted using either...

- Python Jupyter notebook `01_Data_Challenge.ipynb`
  or
- R Markdown file `R_01_Data_Challenge.Rmd`.

Those files have code for...

- Loading data.
- Scaling data.
- Splitting data into train/validation/test partitions.
- Example model training via simple linear regression and a neural network.
- Evaluating and plotting model performance.

Your task: develop a better model for prediction.

Predictive model performance will assessed with
[BSS, MAE, MSE and R<sup>2</sup>](#glossary) metrics.

### Visual Studio Code on Windows

For those tackling the challenge with Python in Visual Studio Code (VS Code) on
Windows, you may want to create a Python virtual environment for the challenge.

<details>
<summary>Creating a Python Virtual Environment</summary>

<br>

If you have the Python Launcher for Windows, you can create a Python virtual
environment, for your default Python installation, from the VS Code terminal
via:

    py -m venv .venv

Using the virtual environment name `.venv` is considered best practice.
Alternatively, if you have more than one Python installation, you can create a
version-specific virtual environment. E.g., for Python 3.13:

    py -3.13 -m venv .venv

</details>

<details>
<summary>Linking a Python Virtual Environment to VS Code</summary>

<br>

Once a Python virtual environment has been created for the challenge, it should
be linked to VS Code.

1. Press `Ctrl + Shift + P` to open the VS Code Command Palette.

2. Type or select **Python: Select Interpreter**.

3. Select the newly created virtual environment from the drop-down list.

</details>

## Glossary

| Acronym       | Definition                   |
| :------------ | :--------------------------- |
| BSS           | Brier Skill Score            |
| MAE           | Mean Absolute Error          |
| MSE           | Mean Squared Error           |
| R<sup>2</sup> | Coefficient of Determination |

## Acknowledgements

This work was supported by the Australian Research Council Training Centre in
Data Analytics for Resources and Environments (project ICI9010031).

Contributors: Joshua Simmons and Travis Stenborg.
