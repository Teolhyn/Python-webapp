import pandas as pd

def excelToDataframe(table: str):
    df = pd.DataFrame(pd.read_csv(table, delimiter=";", header=0))
    #Replace decimal ',' with '.'
    df['Hinta'] = df['Hinta'].str.replace(',', '.').astype(float)
    return df

def averagePriceSince(dateBought: str, data: pd.DataFrame):
    listOfIndexes = data.index[data['DateTime'].str.contains(dateBought)]
    startFrom = int(listOfIndexes[-1])
    averagePrice = data['Hinta'].iloc[startFrom:].mean()
    return averagePrice 

if __name__ == "__main__":
    date = "2023-04-16"
    df = excelToDataframe("chart.csv")
    avgPrice = averagePriceSince(date, df)
    print("Keskimääräinen sähkön markkinahinta", date, "eteenpäin on:", "%.2f" % avgPrice, "snt/kWh")