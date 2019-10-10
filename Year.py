import Country
class Year:
    '''
        Describe a type Year for each year, it contains world's population in this year and top countries Objects
    '''

    def __init__(self, year, topCountries, WorldPopulationInYear):
        self.year = year
        self.worldPopulationThisYear = WorldPopulationInYear.get(year)
        self.countries = []
        # self.top20Countries = top20Countries
        for key in topCountries:
            value = topCountries.get(str(key))
            self.countries.append(Country.Country(key, value))

    def getWorldPopulationThisYear(self):
        return self.worldPopulationThisYear

    def getTopPopulationList(self):
        '''
        Return a list with Population of top Countries. Index 0: Most
        :return: List population with type Float
        '''
        List = []
        for country in self.countries:
            List.append(country.populationInYear)
        return List

    def getTopNameList(self):
        '''
        Return a list with Name of top Countries. Index 0: Country has most population
        :return: List population with type Str
        '''
        List = []
        for country in self.countries:
            List.append(country.name)
        return List
