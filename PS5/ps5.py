# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
#Regular expression
import re
import numpy as np

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            #re.match(pattern, string, flags=0) attempts to match RE pattern to string with optional flags
            #re.match() only searches the beginning of the string while re.search() would search anywhere in the string
            #\d matches any single digit from [0-9]
            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - np.mean(x))**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """

    models = []
    
    for degree in degs:
        model = pylab.polyfit(x, y, degree)
        models.append(model)
    
    return models


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    num = ((y - estimated)**2).sum()
    den = ((y - np.average(y))**2).sum()
    return (1 - num / den)
    

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    #for each model
    for model in models:
        est_y = pylab.polyval(model, x)
        r_square = r_squared(y, est_y)
        
        #plot each model on a separate figure
        pylab.figure()
        pylab.plot(x, y, 'bo', label = 'Measured data')
        pylab.plot(x, est_y, 'r-', label = 'Fit of degree ' + str(len(model) - 1))
        pylab.legend()
        pylab.xlabel('Year')
        pylab.ylabel('Temperatures in Celsius')
        
        #if the model is linear
        if len(model) - 1 == 1:
            pylab.title('Temperatures in US, Fit of degree ' + str(len(model) - 1) + '\nR2 = ' +\
                        str(round(r_square,4)) + '\nSE over slope = ' +\
                        str(round(se_over_slope(x, y, est_y, model),4)))
        else:    
            pylab.title('Temperatures in US, Fit of degree ' + str(len(model) - 1) + '\nR2 = ' +\
                        str(round(r_square,4)))


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    avg_temps = []
    for year in years:
        yearly_avg_temp = 0
        
        for city in multi_cities:
            yearly_avg_temp += np.average(climate.get_yearly_temp(city, year))
        
        yearly_avg_temp /= len(multi_cities)
        avg_temps.append(yearly_avg_temp)
    
    return pylab.array(avg_temps)


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_avgs = []
    for i in range(len(y)):
        if i < window_length - 1:
            #the last element is excluded
            avg = sum(y[:i+1])/len(y[:i+1])
        else:
            starting_value = i - window_length + 1 
            avg = sum(y[starting_value : i + 1])/len(y[starting_value : i+1])
        moving_avgs.append(avg)
    return pylab.array(moving_avgs)
        

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return (sum((y - estimated)**2)/len(y))**0.5


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    std = []
    #for each year
    for year in years:
        #calculate averge daily temperature across the specified cities for each day in that year
        daily_temp = climate.get_yearly_temp(multi_cities[0], year)
        for city in multi_cities[1:]:
            daily_temp += climate.get_yearly_temp(city, year)            
        daily_temp /= len(multi_cities)
            
        #take the standard deviation for the daily averages for the whole year
        std.append(np.std(daily_temp))
    return pylab.array(std)


def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    #for each model
    for model in models:
        est_y = pylab.polyval(model, x)
        RMSE = rmse(y, est_y)
        
        #plot each model on a separate figure
        pylab.figure()
        pylab.plot(x, y, 'bo', label = 'Measured data')
        pylab.plot(x, est_y, 'r-', label = 'Fit of degree ' + str(len(model) - 1))
        pylab.legend()
        pylab.xlabel('Year')
        pylab.ylabel('Temperatures in Celsius')
        pylab.title('Temperatures in US, Fit of degree ' + str(len(model) - 1) + '\nRMSE = ' +\
                        str(round(RMSE,4)))



if __name__ == '__main__':

    # Part A.4
    #4.I Average temperatures in New York on January 10th 
    climate = Climate ('data.csv')
#    x = pylab.array(TRAINING_INTERVAL) 
#    y = []
#    for year in x:
#        #leading zeros are not allowed on numbers
#        y.append(climate.get_daily_temp('NEW YORK', 1, 10, year))
# 
#    y = pylab.array(y)
#    model = generate_models(x, y, [1])
#    evaluate_models_on_training(x, y, model)
#    
#    
#    #4.II Average annual temperatures in New York  
#    x = pylab.array(TRAINING_INTERVAL) 
#    y = []
#    for year in x:
#        y.append(np.average(climate.get_yearly_temp('NEW YORK', year))) 
#    y = pylab.array(y)
#    model = generate_models(x, y, [1])
#    evaluate_models_on_training(x, y, model)
#    
#
#    # Part B National yearly average
#    x = pylab.array(TRAINING_INTERVAL)  
#    y = gen_cities_avg(climate, CITIES, x)
#    model = generate_models(x, y, [1])
#    evaluate_models_on_training(x, y, model)
#
#
#    # Part C 5 Year Moving Average on national yearly average
#    x = pylab.array(TRAINING_INTERVAL)
#    y = gen_cities_avg(climate, CITIES, x)
#    y = moving_average(y, 5)
#    model = generate_models(x, y, [1])
#    evaluate_models_on_training(x, y, model)
#
#    
#    # Part D.2 Predicting
#    # Generate models on 5 year moving averages of the national yearly temp from 1961 - 2009 (training data)
#    x_training = pylab.array(TRAINING_INTERVAL)
#    y_training = gen_cities_avg(climate, CITIES, x_training)
#    y_training = moving_average(y_training, 5)
#    models = generate_models(x_training, y_training, [1, 2, 20])
#    evaluate_models_on_training(x_training, y_training, models)
#    
#    # Predict 5 year moving averages of the national yearly temp from 2010 to 2015 (test  data) with our models
#    x_test = pylab.array(TESTING_INTERVAL)
#    y_test = gen_cities_avg(climate, CITIES, x_test)
#    y_test = moving_average(y_test, 5)
#    evaluate_models_on_testing(x_test, y_test, models)
#    
#
#    # Part E Modeling extreme temperature (standard deviation)
#    x = pylab.array(TRAINING_INTERVAL)
#    y = gen_std_devs(climate, CITIES, TRAINING_INTERVAL)
#    y = moving_average(y, 5)
#    model = generate_models(x, y, [1])
#    evaluate_models_on_training(x, y, model)