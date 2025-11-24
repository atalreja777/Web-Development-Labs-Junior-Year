from flask import Flask, render_template, request

app = Flask(__name__)

MEALS = {"spaghetti": 10.00,"chicken": 12.00,"salad": 8.00, "paneer":14.35}

DRINKS = {"none": 0.00,"soda": 2.00,"tea":1.50, "beer": 3.20}

order_amt = 0
amt_money_gained = 0.0


@app.route('/')
def meal_form():
    return render_template("order_form.html", meals=MEALS, drinks=DRINKS)


@app.route('/summary')
def order_summary():
    global order_amt, amt_money_gained

    meal_choice = request.args.get("meal","no meal choice given")
    drink_choice = request.args.get("drink","no drink choice given")

    meal_qty_str = request.args.get("meal_qty","0")
    drink_qty_str = request.args.get("drink_qty","0")

    senior = request.args.get("senior")   
    notes = request.args.get("notes", "no notes give")

    if meal_qty_str.isdigit():
        meal_qty=int(meal_qty_str)
    else:
        meal_qty = 0

    if drink_qty_str.isdigit():
        drink_qty=int(drink_qty_str)
    else:
        drink_qty =0

    meal_price = MEALS.get(meal_choice, 0.0)
    drink_price = DRINKS.get(drink_choice, 0.0)

    meal_total = meal_price * meal_qty
    drink_total = drink_price * drink_qty

    subtotal = meal_total + drink_total

    discount = 0.0
    if senior:  
        discount = subtotal * 0.10

    total = subtotal - discount

    order_amt += 1
    amt_money_gained += total

    return render_template(
        "order_summary.html",meal_choice=meal_choice, drink_choice=drink_choice, meal_qty=meal_qty, drink_qty=drink_qty, meal_total=meal_total, drink_total=drink_total, subtotal=subtotal, discount=discount,total=total,senior=senior, notes=notes
    )


@app.route('/manager')
def manager_view():
    return render_template( "manager.html", order_amt=order_amt, amt_money_gained=amt_money_gained)


if __name__ == "__main__":
    app.debug = True
    app.run()
