import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import glob
import cv2
import os


class DataReader:
    '''
        an Object of this Class could analyse data and give needed Information back
    '''
    def __init__(self, countriesData, worldData, amountOfTopCountries):
        self.countriesData = countriesData
        self.worldData = worldData

        self.deleteOtherCollums()
        self.amountOfTopCountries = amountOfTopCountries

    def deleteOtherCollums(self):
        '''
        Delete no needed Columns in the countries population table
        '''

        self.countriesData = self.countriesData.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'])

    def getCountOfCountries(self):
        '''
        Get the count of Countries back
        :return: count of Countries
        '''
        return len(self.countriesData)

    def getCountOfYears(self):
        '''
        Get the count of recorded years back
        :return: count of recorded years
        '''
        return len(self.worldData)

    def getTopCountries(self, year):
        '''
        Get a dictionary of Countries, which have most population
        :return: The Dictionary of the Names of Countries
        '''

        # remove all values from another years
        populationInYear = self.countriesData[['Country Name', str(year)]]
        # get top 20 countries
        populationInYear = populationInYear.nlargest(self.amountOfTopCountries, columns=str(year))
        # convert the top Dataframe to a dict
        topDict = populationInYear.set_index('Country Name').to_dict()
        return topDict.get(str(year))

    def getFirstYear(self):
        '''
        Get the earliest year in data
        :return: earliest year in type numpy.int64
        '''
        return self.worldData.iloc[0, 1]

    def getWorldPopulationInYearsDict(self):
        '''
        Get a Dictionary of world population, key = year, value = population
        :return: The Dictionary
        '''
        # delete fisrt column
        worldPopulation = self.worldData[['year', 'population']]
        # convert to dictionary
        worldPopulation = worldPopulation.set_index('year').to_dict()
        # print(worldPopulation.get('population'))
        return worldPopulation.get('population')

    def getHighestPopulationOfAllCountries(self):
        '''
        Get the highest population of all Countries in all years.
        :return: highest population. Type int
        '''
        countries = self.countriesData.melt(id_vars='Country Name')
        countries = countries.rename(columns={'Country Name': 'country', 'variable': 'year', 'value': 'population'})
        countries = countries[~ countries.population.isna()]
        countries = countries.astype({'population': int})
        return countries.population.max()


