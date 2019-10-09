import matplotlib.pyplot as plt
import seaborn as sb
import os
import cv2

class Graph:
    def __init__(self, dataReader, yearsDict):
        self.dataReader = dataReader
        self.yearsDict = yearsDict
        self.NumberOfYears = dataReader.getCountOfYears()
        self.MaxPopulationPerCountry = dataReader.getHighestPopulationOfAllCountries()
        self.top = 20
        self.image_folder = '/Users/quochuy/Desktop/Github/Population-Census/Images'
        self.video_name = '/Users/quochuy/Desktop/Github/Population-Census/Images/Video.avi'

    def render(self):
        process = 0;
        for x in range(self.NumberOfYears):
            process = self.showLoading(process, x)

            thisYear = self.dataReader.getFirstYear() + x
            top20ThisYear = self.yearsDict.get(thisYear).countries
            data = self.dataReader.getTop20CountriesInDataFrame(thisYear)

            plt.figure(figsize=(15, 10))
            sb.set_style("dark")

            sb.barplot(x = str(thisYear),
                       y = "Country Name",
                       data = data,
                       palette=sb.color_palette("YlOrRd_r", 20))
            title = "biggest countries by population".upper() + '\n ' + str(thisYear)
            title_obj = plt.title(title)
            plt.setp(title_obj, color='orangered', fontsize=30)

            # Tạo và định dạng nhãn của các trục
            plt.tick_params(axis="y", labelsize=14, labelrotation=15, labelcolor="g")
            plt.tick_params(axis="x", labelsize=17, labelrotation=0, labelcolor="g",
                            bottom=True, top=True, labeltop=True, labelbottom=True)
            plt.xlim(right=(1.2 * self.MaxPopulationPerCountry))  # cố định trục x
            plt.xlabel('\nPopulation (by the Billion)', fontsize=20, color="g")  # Tạo nhãn trục x
            plt.ylabel('')  # Xóa nhãn trục y

            for t in range(self.top):
                value = f'{int(top20ThisYear[t].populationInYear):,}'  # Định dạng kiểu số: 123,456,000
                plt.text(top20ThisYear[t].populationInYear + 50000000, t,  # Tọa độ
                         value,  # Giá trị
                         color='deepskyblue', va="center", fontsize=17)  # Định dạng
                # Thêm thứ hạng vào biểu đồ
                plt.text(1000000, t,
                         str(t + 1),
                         color='lime', va="center", fontsize=17)

            # Tạo chữ trung tâm
            plt.text(610000000, 7,
                'TOTAL POPULATION OF THE WORLD',
                 color='orangered', va="center", fontsize=25)
            # Tạo tổng dân số thế giới ở trung tâm
            world_population = f'{int(self.yearsDict.get(thisYear).getWorldPopulationThisYear()):,}'  # Dân số thế giới
            plt.text(560000000, 10,  # Tọa độ
                world_population,  # Giá trị
                color='orangered', va="center", fontsize=80)  # Định dạng

            # Tạo chữ ký
            plt.text(1000000000, self.top - 1.5,
                'Võ Văn Thương & Quốc Huy Nguyễn \nHồ Chí Minh, tháng 9 năm 2019\nData sources: https://data.worldbank.org',
                color='royalblue', va="center", fontsize=13)

            # Lưu biểu đồ
            filename = 'population_' + str(thisYear) + '.png'
            plt.savefig('/Users/quochuy/Desktop/Github/Population-Census/Images/' + filename, dpi=30)
            plt.gca()
            plt.close()

    def showLoading(self, process, x):
        if process == 0 and x > self.NumberOfYears/100*20:
            print ("Rendering 20% done")
            return 20
        if process == 20 and x > self.NumberOfYears / 100 * 40:
            print ("Rendering 40% done")
            return 40
        if process == 40 and x > self.NumberOfYears / 100 * 60:
            print ("Rendering 60% done")
            return 60
        if process == 60 and x > self.NumberOfYears / 100 * 80:
            print ("Rendering 80% done")
            return 80
        if process == 80 and x == self.NumberOfYears - 1:
            print ("Rendering 100% done")
            return 100
        else:
            return process


