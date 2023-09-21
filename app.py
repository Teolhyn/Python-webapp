from flask import Flask, render_template, request
import pandas as pd
import datetime

app = Flask('testapp')

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

@app.route('/date', methods=['GET', 'POST'])
def date_example():
    
    if request.method=="POST":
        
        # get date
        form_date = request.form.get('date') # in format 2012-10-25 or in Python String formatting %Y-%m-%d
        
        # create Python date from form_date and form_time. We use the python datetime string formmatting to describe how the date is built YYYY-MM-DD HH:MM

        date = datetime.datetime.strptime(form_date,"%Y-%m-%d").date()
        
        # create your database document
        # this is an example model
        # mydoc = models.Mydata()
        # mydoc.date = date  # save date to the 'date' field
        # mydoc.save()
        df = excelToDataframe("chart.csv")
        avgPrice = averagePriceSince(str(date), df)
        output = f"Keskimääräinen sähkön markkinahinta {date} eteenpäin on: {avgPrice:.2f} snt/kWh"
        return output
        
    else:
        
        return render_template("date_example.html")
    
if __name__ == '__main__':
    app.run()