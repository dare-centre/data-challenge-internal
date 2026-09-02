# DARE - Deluxe Data Challenge I

This repository contains the data and example code for the DARE Deluxe Data
Challenge I.

## Data
Data were prepared using the Jupyter notebook `00_Data_Preprocessing.ipynb`. We
will be using the files:

`data/daily_train_X_data.csv`\
`data/daily_train_y_data.csv`\
`data/daily_test_X_data.csv`\
`data/daily_test_y_data.csv`

## Code

You should use either...

- Python Jupyter notebook `01_Data_Challenge.ipynb`
or
- R Markdown file `R_01_Data_Challenge.Rmd`

to complete the challenge.

Those files have code for...

- Loading data.
- Scaling data.
- Splitting data into train/validation/test partitions.
- Example model training via simple linear regression and a neural network.
- Evaluating and plotting model performance.

Your task: develop a better model for prediction.

Predictive model performance will assessed with BSS, MAE, MSE and R<sup>2</sup>
metrics.

## Glossary

| Acronym       | Definition                   |
| :------------ | :--------------------------- |
| BSS           | Brier Skill Score            |
| MAE           | Mean Absolute Error          |
| MSE           | Mean Squared Error           |
| R<sup>2</sup> | Coefficient of Determination |

## Acknowledgements

Contributors: Joshua Simmons and Travis Stenborg.
