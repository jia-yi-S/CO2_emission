import pandas as pd
import numpy
from sklearn.linear_model import LinearRegression
import pickle
import os

# get the current working directory
dir = os.getcwd()

# load the csv file to get the pandas dataframe of it
data = pd.read_csv(dir+'/src/lib/csv/co2_emission.csv')
print("Setup Complete")
print(data.head())

# find out all the unique country list
country = data.Entity.unique()
# the length of the country list
country_length = len(country)


# function to generate the prediction model of single country (not to be used if you are doing for all countries)
def generate_model_for_single_country(country_name):
    # find out the data of only given country from the original dataframe
    c = data.loc[data['Entity']==country_name]
    
    # get the year as x-value
    x = c['Year']
    # convert this to numpy array
    x = numpy.array(x)
    
    # get the Annual CO2 emissions (tonnes ) as the y-value
    y = c['Annual CO2 emissions (tonnes )']

    # initialize the model
    co_model = LinearRegression()

    # Fit the model
    co_model.fit(x.reshape(-1, 1),y)

    # testing of the above fitted model with 3 different years (optional step)
    b=numpy.array([2020,2021,1900])
    co_model.predict(b.reshape(-1, 1))

    # dump the model into the pickle file
    pickle.dump(co_model, open(dir+'/prediction/model_resource/{country}.pkl'.format(country=country_name.lower()),'wb'))


# function to generate the prediction model of all countries
def generate_model_for_all_countries():
    # iterate through each country for generating model
    for n, given_country in enumerate(country):
        # logging for keeping track of loop
        print(str(n+1) + '/' + str(country_length) + ': ' + str(i))
        
        # find out the data of only given country from the original dataframe
        a = data.loc[data['Entity']==given_country]
        
        # get the year as x-value
        x = a['Year']
        # convert this to numpy array
        x = numpy.array(x)
        
        # get the Annual CO2 emissions (tonnes ) as the y-value
        y = a['Annual CO2 emissions (tonnes )']
        
        # initialize the model
        co_model = LinearRegression()
        
        # Fit the model
        co_model.fit(x.reshape(-1, 1),y)
        
        # dump the model into the pickle file
        pickle.dump(co_model, open(dir+'/prediction/model_resource/{}.pkl'.format(given_country.lower()),'wb'))
        

if __name__ == '__main__':
    generate_model_for_all_countries()
