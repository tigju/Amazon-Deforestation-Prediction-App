# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
        """
### **Working Process**
Visit my Medium blog post for more detailed process: 
##### [Can We Predict Deforestation in Amazon Forests with Machine Learning?](https://medium.com/https://medium.com/@iuliia.stanina)

---

#### **Purpose**
The aim is to predict the location of an area where deforestation most likely to occur. I decided to try out 
different models such as **Ridge Model**, **Decision Tree**, **Random Forest** and **XGBoost** for my predictions 
and see which performs better. Since it is a spatial data, for the sake of simplicity I decided to treat the location
as it is in 2D space and not the sphere, and predict latitude and longitude as two separate values using two different models.
    

#### **Data Wrangling, Data Cleaning**
I used pandas profiling to look at my data and features closely and see the distribution, check for cardinality, zeros and nulls. 
Data set initially had 14 columns and 474930 rows. I took a sample from the dataset for the purposes of showing the process in a web app 
and got 47105 rows. There was a leakage features that I excluded from dataset and some zero values that I converted to nulls, later to 
sort them with Simple Imputer. Also, *'areakm_squared'* feature was very skewed, because it had outliers and I decided to remove all the
values that are more than 3 standard deviations from the mean. There were a lot of useless features like *'gid'*, *'origin_id'*, *'scene_id'* which were all unique, *'julday'*, *'dfsn'*, and some others didn't make any sence. 
I also split up the date into day/month/year which is possible become a good features in predictions. So, after the explorarion and 
clean-up I ended up with only five features: 
*'areakm_squared', 'day', 'month', 'year', 'states'*

#### **Feature Engineering**
Since the aim is to predict the coordinates of the deforestation, and my dataset didn't have latitude and longitude, but it had 
*'geometry'* feature, containing Polygons and Multipolygons, I decided to extract centroids of the deforested areas from them using
Geopandas. 

#### Target Distribution
To see the distribution of coordinates values from sample dataset I used simple Matplotlib.pyplot library. 
Latitude has normal distribution, but longitude is a little left-skewed. 
        """),
		html.Img(src='assets/coordinates-dist.jpg',className='img-fluid'),
 		dcc.Markdown(
        """
---

### **Choosing the Model**
---
I tried different models to see how they would perform in predictions for coordinates. The first one I chose is Ridge Model.
#### 1. Ridge Regression Model

For the validation metrics I used MAE (*mean absolute error*), RMSE (*root mean absolute error*) and 
R^2 (*R-squared*):
```
Ridge model validation MAE: 1.3298 lat
Ridge model validation MAE: 1.8627 lon
Ridge model Validation RMSE loss: 2.8657 lat
Ridge model Validation RMSE loss: 5.5378 lon
Ridge model Validation R^2 coefficient: 0.7945 lat
Ridge model Validation R^2 coefficient: 0.8753 lon
``` 
Metrics showed some good results, however on the graph we can see that Ridge model didn't do a good job.
        """),
        html.Img(src='assets/true-predicted-ridge.jpg',className='img-fluid'),
        dcc.Markdown(
        """

#
#
#### 2. Decision Tree Model
The next model I tried is *DecisionTreeRegressor* model. I used *TargetEncoder* and default hyperparameters. 
For validation data I used the same metrics:
```
Desicion Tree validation MAE: 1.7390 lat
Desicion Tree validation MAE: 3.5811 lon
Desicion Tree Validation RMSE loss: 5.3506 lat
Desicion Tree Validation RMSE loss: 19.1354 lon
Desicion Tree Validation R^2 coefficient: 0.6163 lat
Desicion Tree Validation R^2 coefficient: 0.5692 lon
```
Decision tree is also not so good in predicting locations
		"""),
		html.Img(src='assets/true-pred-dt.jpg',className='img-fluid'),
		dcc.Markdown(
        """

#
#
#### 3. Random Forest Model
I took another step and tried Random Forest Regressor. For the Random Forest I used *hyperparameter tuning* and
applied *RandomizedSearchCV*. With the *hyperparameter tuning* and *RandomizedSearchCV* I better scores for my validation
metrics:
```
Random Forest Validation MAE: 1.5652 lat
Random Forest Validation MAE: 2.4324 lon
Random Forest Validation RMSE loss: 3.9335 lat
Random Forest Validation RMSE loss: 8.2871 lon
Random Forest Validation R^2 coefficient: 0.7179 lat
Random Forest Validation R^2 coefficient: 0.8134 lon
```
Lets take a look at the scatter plot for Random Forest. It did much better that other models I tried so far.
		"""),
		html.Img(src='assets/true-predicted-rf.jpg',className='img-fluid'),
		dcc.Markdown(
        """

#
#
#### 3. XGBoost Model
For my last model I chose XGBoost Regressor. I use some *hyperparameters tuning* and *'early_stopping for this model'*
Metrics look a little worse that Random Forest: 
```
XGBoost Validation MAE: 1.5486 lat
XGBoost Validation MAE: 2.8789 lon
XGBoost Validation RMSE loss: 4.0418 lat
XGBoost Validation RMSE loss: 11.2123 lon
XGBoost Validation R^2 coefficient: 0.7101 lat
XGBoost Validation R^2 coefficient: 0.7476 lon
```
However, in my opinion, XGBoost Model predictions looks closer to true values on the scatter plot:
		"""),
		html.Img(src='assets/true-predicted-xgb.jpg',className='img-fluid'),
		dcc.Markdown(
        """

#
#
---
### Conclusion

		""")
    ],
)

layout = dbc.Row([column1])