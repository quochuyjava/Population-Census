import DataReader as reader
import Year
import Graph
import pandas as pd

# Variable declaration:
countriesData = pd.read_excel('population -countries.xls', sep=' ', encoding='utf-8')   # Link to excel file
worldData = pd.read_excel('population - world.xls', sep=' ', encoding='utf-8')
amountOfTopCountries = 20
imageOutputFolder = '/Users/quochuy/Desktop/Github/Population-Census/Images'
videoOutputFolder = '/Users/quochuy/Desktop/Github/Population-Census/Images/Video.avi'


def start():
    dataReader = reader.DataReader(countriesData, worldData, amountOfTopCountries)
    yearsDict = init_years(dataReader)
    graph = Graph.Graph(dataReader, yearsDict, imageOutputFolder, videoOutputFolder)
    graph.render()


def init_years(dataReader):
    yearsDict = {}
    first_year = dataReader.getFirstYear()
    worldPopulationInYears = dataReader.getWorldPopulationInYearsDict()
    for x in range(dataReader.getCountOfYears()):
        # print(first_year + x)
        this_year = first_year+x
        top_countries_in_this_year = dataReader.getTopCountries(this_year)
        yearsDict[first_year + x] = Year.Year(this_year, top_countries_in_this_year, worldPopulationInYears)
    return yearsDict


start()
