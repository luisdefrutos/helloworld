import http.client
import sys
import os

# Añadir el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import util
from app.calc import Calculator

CALCULATOR = Calculator()
api_application = Flask(__name__)
#text/plain; charset=UTF-8
HEADERS = {"Content-Type": "text/plain;charset=UTF-8",  "Access-Control-Allow-Origin": "*"}


@api_application.route("/")
def hello():
    return "Hello from The Calculator!\n"


@api_application.route("/calc/add/<op_1>/<op_2>", methods=["GET"])
def add(op_1, op_2):
    try:
        num_1, num_2 = util.convert_to_number(op_1), util.convert_to_number(op_2)
        return ("{}".format(CALCULATOR.add(num_1, num_2)), http.client.OK, HEADERS)
    except TypeError as e:
        return (str(e), http.client.BAD_REQUEST, HEADERS)


@api_application.route("/calc/substract/<op_1>/<op_2>", methods=["GET"])
def substract(op_1, op_2):
    try:
        num_1, num_2 = util.convert_to_number(op_1), util.convert_to_number(op_2)
        return ("{}".format(CALCULATOR.substract(num_1, num_2)), http.client.OK, HEADERS)
    except TypeError as e:
        return (str(e), http.client.BAD_REQUEST, HEADERS)
    

    
@api_application.route("/calc/mul/<op_1>/<op_2>", methods=["GET"])
def mul(op_1, op_2):
    try:
        num_1, num_2 = util.convert_to_number(op_1), util.convert_to_number(op_2)
        return ("{}".format(CALCULATOR.multiply(num_1, num_2)), http.client.OK, HEADERS)
    except TypeError as e:
        return (str(e), http.client.BAD_REQUEST, HEADERS)
    
@api_application.route("/calc/div/<op_1>/<op_2>", methods=["GET"])
def div(op_1, op_2):
    try:
    
        
        num_1, num_2 = util.convert_to_number(op_1), util.convert_to_number(op_2)
        if num_2 == 0:
            raise ZeroDivisionError("La operación no es válida.El número divisor no puede ser cero.")
        return ("{}".format(CALCULATOR.divide(num_1, num_2)), http.client.OK, HEADERS)
    except TypeError as e:
        return (str(e), http.client.BAD_REQUEST, HEADERS)
    except ZeroDivisionError as e:
        return (str(e), http.client.BAD_REQUEST, HEADERS)



    
    
if __name__ == "__main__":
    api_application.run(host="0.0.0.0", port=5000, debug=True)

