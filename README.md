# Apartment Prices Prediction Project

## Overview

This project focuses on predicting apartment prices using a hybrid regression technique. The methodology involves the synergistic combination of Gradient Boosting and Random Forest algorithms through a Stacking Regressor, with Lasso as the final estimator. Additionally, cosine similarity is incorporated for personalized recommendations.

## Architecture

![Alt Text](/images/ml.PNG)

## Usage

1. Collect data from the website using Selenium and BeautifulSoup.

2. Run Exploratory Data Analysis (EDA) to gain insights into the dataset.

3. Develop a `Preprocessing` class to handle data cleaning, feature engineering, and other necessary preprocessing tasks, ensuring the dataset is refined and   ready for analysis.

4. Evaluate different regression algorithms and choose Gradient Boosting and Random Forest as base algorithms.

5. Optimize the model using GridSearchCV and create a Hybrid Regression model.

6. Demonstrate model predictions and recommendations using cosine similarity.

## Getting Started

### Prerequisites

- Python 3.11.0
- Libraries: NumPy, Pandas, Scikit-learn,matplotlib, BeautifulSoup, Selenium, FLask

### Installation
1. Clone the repository:

   ```bash
   git clone https://github.com/MdRiBen/ApartementPricePredictionInMorocco.git

2. Create a folder named: ApartmentPricePredictionInMorocco/Models.
    
3. Navigate to the Processing Folder:
    ```bash
    cd ApartementPricePredictionInMorocco/processing

4. Run the load_models file:

    ```bash
    jupyter nbconvert --to script load_models.ipynb
    python load_models.py

5. Navigate to the Web Application Folder:

    ```bash
    cd ../webApplication

6. run the application:
    ```bash
    python app.py



