from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
app.debug = True

x = {
    "count": 110,
    "next": "https://ion.tjhsst.edu/api/schedule?page=5",
    "previous": "https://ion.tjhsst.edu/api/schedule?page=3",
    "results": [
        {
            "url": "https://ion.tjhsst.edu/api/schedule/2022-09-01",
            "date": "2022-09-01",
            "day_type": {
                "name": "Blue Day",
                "special": False,
                "blocks": [
                    {
                        "order": 1,
                        "name": "Period 1",
                        "start": "8:40",
                        "end": "10:15"
                    },
                    {
                        "order": 2,
                        "name": "Period 2",
                        "start": "10:25",
                        "end": "12:00"
                    },
                    {
                        "order": 3,
                        "name": "Lunch",
                        "start": "12:00",
                        "end": "12:40"
                    },
                    {
                        "order": 4,
                        "name": "Period 3",
                        "start": "12:40",
                        "end": "14:15"
                    },
                    {
                        "order": 5,
                        "name": "Period 4",
                        "start": "14:25",
                        "end": "16:00"
                    }
                ]
            }
        }
    ]
}
@app.route("/")
def root():
    return redirect(url_for("view_schedule"))

@app.route("/schedule")
def view_schedule():
    day = x["results"][0]  # one day
    return render_template("schedule.html", day=day)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
