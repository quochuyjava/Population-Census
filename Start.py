import DataReader as reader
import Year
import Graph
import Country

yearsDict = {}

dataReader = reader.DataReader()


def init_years():
    first_year = dataReader.getFirstYear()
    worldPopulationInYears = dataReader.getWorldPopulationInYearsDict()
    for x in range(dataReader.getCountOfYears()):
        # print(first_year + x)
        this_year = first_year+x
        top20_in_this_year = dataReader.getTop20Countries(this_year)
        yearsDict[first_year + x] = Year.Year(this_year, top20_in_this_year, worldPopulationInYears)

init_years()
graph = Graph.Graph(dataReader, yearsDict)
graph.render()