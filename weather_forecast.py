import requests
from dotenv import load_dotenv
import os

tempList, humiditylist, weatherDescList, timeList, forecastList, completeDataList = [], [], [], [], [], []

def configure():
    load_dotenv()

def main():
    configure()
    print("5-Day (3-Hour-Step) Weather Forecast")
    print("NOTE: You'll need a big terminal window for this.")
    getLocation =  input("Enter your location here: ")
    conversionUnits = input("Would you like to view as F (Fahrenheit), C (Celcius) or K (Kelvin): ").upper()
    getLocationData(getLocation, conversionUnits)

def getLocationData(location, convUnits):
    URL = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={os.getenv('API_KEY')}"
    requestData = requests.get(URL) # Call the URL to get the data
    data = requestData.json() # Change the requestsData variable into json so it is readable
    if requestData.status_code == 404:
        raise ValueError("Invalid location, please try again.")
    elif requestData.status_code != 200:
        raise Exception(f"API failed with status code {requestData.status_code}")
    else:
        for forecast in data["list"]:
            forecastList.append(forecast)
        for x in range(len(forecastList)):
            tempList.append(forecastList[x]["main"]["temp"])
            humiditylist.append(forecastList[x]["main"]["humidity"])
            weatherDescList.append(forecastList[x]["weather"][0]["description"])
            timeList.append(forecastList[x]["dt_txt"])
        for y in range(len(tempList)):
            match convUnits:
                case "K":
                    completeDataList.append([f"{round(tempList[y], 2)}K", f"{humiditylist[y]}%", weatherDescList[y], timeList[y]])
                case "C":
                    completeDataList.append([f"{round(tempList[y] - 273.15, 2)}C", f"{humiditylist[y]}%", weatherDescList[y], timeList[y]])
                case "F":
                    completeDataList.append([f"{round(((((tempList[y] - 273.15) * 9)/5) + 32), 2)}F", f"{humiditylist[y]}%", weatherDescList[y], timeList[y]])
        outputForecast(completeDataList)

def outputForecast(dataList):
    print("\t   -------------------------------------")
    print("\t   |  5-Day (3-Hour) Weather Forecast  |")
    print("\t   -------------------------------------")
    tempStr, humidStr, weatherDescStr, timeStr = "", "", "", ""
    for a in range(len(dataList)):
        for b in range(len(dataList[a])):
            match b:
                case 0:
                    tempStr = f"| Temperature: {dataList[a][b]}"
                case 1: 
                    humidStr = f"| Humidity: {dataList[a][b]}"
                case 2:
                    weatherDescStr = f"| Weather Description: {dataList[a][b].capitalize()}"
                case 3:
                    timeStr = f"Time: {dataList[a][b]}"
        print(f"-----------------{timeStr}-----------------")
        print(f"{tempStr}\n{humidStr}\n{weatherDescStr}")
        print("-----------------------------------------------------------\n")

if __name__ == "__main__":
    main()