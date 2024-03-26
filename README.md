# Analyzing Factors Affecting Car Prices in the Cambodian Automobile Market

This repository contains the code and data for the analysis of factors affecting car prices in the Cambodian automobile market. The study utilizes data obtained from Khmer24, a popular platform for buying and selling vehicles in Cambodia. The analysis includes exploratory data analysis (EDA) and the application of various regression algorithms to predict car prices based on different factors.

## Key Findings from Exploratory Data Analysis (EDA)

- Toyota emerges as the most favored car company among customers, with the highest number of sales.
- Some car companies have limited data points, necessitating further analysis to draw meaningful inferences about them.
- Luxury car brands like Lamborghini, Ferrari, and Rolls-Royce offer cars across a wide price range, appealing to different customer segments.
- Cars with petrol fuel systems dominate the market and are available at various price points.
- Daewoo and Suzuki have a smaller presence in the dataset, warranting additional data for analyzing the lowest price range car companies.

The exploratory data analysis has provided valuable insights and serves as a solid foundation for further analysis and decision-making based on the data.

## Model Performance

The following table summarizes the performance of various regression algorithms on the dataset:

| Model               | Training Score | Testing Score | Algorithm             |
|---------------------|----------------|---------------|-----------------------|
| Linear Regression   | 68.6840        | 66.1456       | Linear Regression     |
| Linear Regression   | 68.6840        | 66.1456       | Linear Regression     |
| Linear Regression   | 68.6703        | 66.1096       | Linear Regression     |
| Ridge Regression    | 68.6920        | 66.1509       | Ridge Regression      |
| Lasso Regression    | 68.0999        | 65.6792       | Lasso Regression      |
| Linear Regression   | 68.6926        | 66.1433       | Linear Regression     |
| Ridge Regression    | 68.6804        | 66.1939       | Ridge Regression      |
| Lasso Regression    | 65.0722        | 62.9610       | Lasso Regression      |

## Future Directions

To gain deeper insights and improve predictive accuracy, future analysis could consider the following avenues:

- Exploring additional variables and their impact on car sales.
- Investigating customer preferences for specific car models.
- Conducting market segmentation to target different customer groups effectively.

## Dependencies

The analysis is conducted using Python programming language and several libraries including pandas, numpy, scikit-learn, and matplotlib. Make sure to install these dependencies before running the code.

## Usage

To replicate the analysis or explore the dataset further, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the Jupyter Notebook or Python scripts provided in the repository.

## Dataset

The dataset used in this analysis is not included in this repository due to its size and possible restrictions. However, the code provided here can be adapted to analyze other similar datasets.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

---

By Sobon Menghorng- menghorngmeakh@gmail.com - 01/07/2023
