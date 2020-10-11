import pickle
import os
from pprint import pprint
import pandas as pd
import simplejson

# get current working directory
dir = os.getcwd()

# function to get the dictionary of countries and their repective country code
def get_country_and_code(country_only=False):
    # load csv into dataframe
    data = pd.read_csv(dir+'/src/lib/csv/co2_emission.csv')
    
    # country_only is true then return only list of unique countries
    if country_only:
        country = data.Entity.unique()
        return country
    # else create a dictionary of country and their repective code
    country_and_code = dict(zip(data.Entity, data.Code))
    return country_and_code


# function to get prediction data for given year for given year range
def prediction_per_country(country_name, year_lower_range, year_upper_range):
    # initialise data list
    data_list = list()
    # get the country with code dict
    country_and_code = get_country_and_code()
    
    # loop for each year and get respective prediction data for that year
    for i in range(year_lower_range, year_upper_range+1):
        # read the model pickle file (load the model)
        model = pickle.load(open(dir+'/prediction/model_resource/{}.pkl'.format(country_name.lower()), 'rb'))
        
        # use loaded model to predict the given year
        co_data = model.predict([[i]])
        
        # fit this prediction data into the required dict format
        data = {
            'Entity':country_name,
            'Code':country_and_code[country_name],
            'Year':str(i),
            'Annual CO2 emissions (tonnes )':str(co_data[0]),
        }
        # append this dict to data list which is to be returned by the function
        data_list.append(data)
    return data_list


# function to gather the overall prediction data for all countries
def overall_prediction(year_lower_range, year_upper_range):
    # get the list of all countries
    country_list = get_country_and_code()
    # initialize the list
    data_list = list()
    try:
        # iterate through each country in country_list
        for country in country_list:
            # get the prediction data for given country
            country_data = prediction_per_country(country, year_lower_range, year_upper_range)
            # add this to result list
            data_list += country_data
        # return the result list
        return data_list
    except Exception as e:
        print('Error in getting country prediction data and error is: ' + str(e))
   

# function to save the prediction data of all countries into the file
def save_prediction_file(year_lower_range, year_upper_range, path=dir+'/src/lib/'):
    # call overall_prediction for required year range
    country_prediction_data = overall_prediction(year_lower_range, year_upper_range)
    pprint(country_prediction_data)
    
    # open the file to save the prediction data so that it will reflect in the web page
    file =  open(path+'worldjsonWithPrediction.js', 'a')
    
    # write the data by converting it to json
    file.write(simplejson.dumps(country_prediction_data, ignore_nan=True))
    
    # close the file
    file.close()




if __name__ == '__main__':
    
    # call the save_prediction_file for given year range
    save_prediction_file(2018, 2099)