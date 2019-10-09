import Country
class Year:

    def __init__(self, year, top20Countries, WorldPopulationInYear):
        self.year = year
        self.worldPopulationThisYear = WorldPopulationInYear.get(year)
        self.countries = []
        # self.top20Countries = top20Countries
        for key in top20Countries:
            value = top20Countries.get(str(key))
            self.countries.append(Country.Country(key, value))

    def getWorldPopulationThisYear(self):
        return self.worldPopulationThisYear

    def getTopCountriesThisYear(self):
        return self.countries
