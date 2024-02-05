# House Prices Prediction Project

## Overview

This project focuses on predicting apartment prices using a hybrid regression technique. The methodology involves the synergistic combination of Gradient Boosting and Random Forest algorithms through a Stacking Regressor, with Lasso as the final estimator. Additionally, cosine similarity is incorporated for personalized recommendations.

## Archeticture

![Alt Text](/images/ml.PNG)


## Getting Started

### Prerequisites

- Python 3.11.0
- Libraries: NumPy, Pandas, Scikit-learn,matplotlib, BeautifulSoup, Selenium, FLask

## Usage

1. Collect data from the website using Selenium and BeautifulSoup.

2. Run Exploratory Data Analysis (EDA) to gain insights into the dataset.

3. Develop a `Preprocessing` class to handle data cleaning, feature engineering, and other necessary preprocessing tasks, ensuring the dataset is refined and   ready for analysis.

4. Evaluate different regression algorithms and choose Gradient Boosting and Random Forest as base algorithms.

5. Optimize the model using GridSearchCV and create a Hybrid Regression model.

6. Demonstrate model predictions and recommendations using cosine similarity. 