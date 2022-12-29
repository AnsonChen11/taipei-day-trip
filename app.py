from flask import *
from api.attraction.attraction import attraction
from api.auth.auth import auth
from api.booking.booking import booking
from api.thankyou.thankyou import thankyou
from api.orders.orders import orders
from api.historyOrders.history_orders import history_orders
from api.member.member import member

app=Flask(__name__)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False #可避免json自動排序

#blueprint
app.register_blueprint(attraction)
app.register_blueprint(auth)
app.register_blueprint(booking)
app.register_blueprint(thankyou)
app.register_blueprint(orders)
app.register_blueprint(history_orders)
app.register_blueprint(member)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)