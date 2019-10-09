import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import glob
import cv2
import os


class DataReader:
    def __init__(self):
        self.countries = pd.read_excel('population -countries.xls', sep=' ', encoding='utf-8')
        self.world = pd.read_excel('population - world.xls', sep=' ', encoding='utf-8')
        self.deleteOtherCollums()

    def deleteOtherCollums(self):
        '''
        Delete no needed Columns in the countries population table
        '''

        self.countries = self.countries.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'])

    def getCountOfCountries(self):
        '''
        Get the count of Countries back
        :return: count of Countries
        '''
        return len(self.countries)

    def getCountOfYears(self):
        '''
        Get the count of recorded years back
        :return: count of recorded years
        '''
        return len(self.world)

    def getTop20Countries(self, year):
        '''
        Get 20 Countries, which have most population
        :return: The Dictionary of the Names of 20 Countries
        '''

        # remove all values from another years
        populationInYear = self.countries[['Country Name', str(year)]]
        # get top 20 countries
        populationInYear = populationInYear.nlargest(20, columns=str(year))
        #print (populationInYear)
        # convert the top 20 Dataframe to a dict
        top20Dict = populationInYear.set_index('Country Name').to_dict()
        return top20Dict.get(str(year))

    def getTop20CountriesInDataFrame(self, year):
        '''
        Get 20 Countries, which have most population
        :return: The Dictionary of the Names of 20 Countries
        '''

        # remove all values from another years
        populationInYear = self.countries[['Country Name', str(year)]]
        # get top 20 countries
        populationInYear = populationInYear.nlargest(20, columns=str(year))
        populationInYear = populationInYear.astype({str(year): int})

        return populationInYear

    def getFirstYear(self):
        return self.world.iloc[0,1]

    def getWorldPopulationInYearsDict(self):
        '''
        Get a Dictionary of world population, key = year, value = population
        :return: The Dictionary
        '''
        # delete fisrt column
        worldPopulation = self.world[['year', 'population']]
        # convert to dictionary
        worldPopulation = worldPopulation.set_index('year').to_dict()
        # print(worldPopulation.get('population'))
        return worldPopulation.get('population')

    def getHighestPopulationOfAllCountries(self):
        countries = self.countries.melt(id_vars='Country Name')
        countries = countries.rename(columns={'Country Name': 'country', 'variable': 'year', 'value': 'population'})
        countries = countries[~ countries.population.isna()]
        countries = countries.astype({'population': int})
        return countries.population.max()


#reader = DataReader()
#reader.deleteOtherCollums()
