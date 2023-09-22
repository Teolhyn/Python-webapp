from flask import Flask, render_template, request
import pandas as pd
import datetime

app = Flask("testapp")

# TODO: Fetch updated price list once a day, and append it to the old list.

# Convert the CSV to Pandas Dataframe
def csv_to_dataframe(table: str):
    df = pd.DataFrame(pd.read_csv(table, delimiter=";", header=0))
    # Replace decimal ',' with '.'
    df["Hinta"] = df["Hinta"].str.replace(",", ".").astype(float)
    return df

# Calculate average price since the selected date
def average_price_since(dateBought: str, data: pd.DataFrame):
    listOfIndexes = data.index[data["DateTime"].str.contains(dateBought)]
    startFrom = int(listOfIndexes[-1])
    averagePrice = data["Hinta"].iloc[startFrom:].mean()
    return averagePrice


@app.route("/", methods=["GET", "POST"])
def date_example():

    if request.method == "POST":
        # get date
        form_date = request.form.get(
            "date"
        )  # in format 2012-10-25 or in Python String formatting %Y-%m-%d

        form_price = request.form.get(
            "price"
        )
        price = float(form_price)
        # create Python date from form_date and form_time. We use the python datetime string formmatting to describe how the date is built YYYY-MM-DD HH:MM
        date = datetime.datetime.strptime(form_date, "%Y-%m-%d").date()

        df = csv_to_dataframe("chart.csv")
        avgPrice = average_price_since(str(date), df)
        if (avgPrice < price):
            output = f"Keskimääräinen sähkön markkinahinta {date} eteenpäin on: {avgPrice:.2f} snt/kWh. Sinun hintasi oli {price:.2f} snt/kWh.\n Kerrostalossa pössisähkö olisi\
                    vuoden aikana säästänyt keskimäärin {2000*(price-avgPrice)/100:.2f}€, rivitalossa {3000*(price-avgPrice)/100:.2f}€, \
                    kaukolämmitteisessä omakotitalossa {7300*(price-avgPrice)/100:.2f}€ ja sähkölämmitteisessä omakotitalossa {19700*(price-avgPrice)/100:.2f}€."
        else:
            output = f"Keskimääräinen sähkön markkinahinta {date} eteenpäin on: {avgPrice:.2f} snt/kWh. Sinun hintasi oli {price:.2f} snt/kWh.\n Kerrostalossa pössisähkö olisi\
                    vuoden aikana tullut kalliimmaksi keskimäärin {abs(2000*(price-avgPrice)/100):.2f}€, rivitalossa {abs(3000*(price-avgPrice)/100):.2f}€, \
                    kaukolämmitteisessä omakotitalossa {abs(7300*(price-avgPrice)/100):.2f}€ ja sähkölämmitteisessä omakotitalossa {abs(19700*(price-avgPrice)/100):.2f}€."            
        return render_template("date_example.html", value=output)

    else:
        return render_template("date_example.html")

# TODO: Show errors as pop-up or similiar. Do not let it go to a default style, separate error page.
@app.errorhandler(500)
def internalServerError(error):
    e_message = 'Virhe laskussa!'
    return render_template("date_example.html", value=e_message)

if __name__ == "__main__":
    app.run()
