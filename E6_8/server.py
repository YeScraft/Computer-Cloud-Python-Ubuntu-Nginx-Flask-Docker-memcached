from flask import Flask, render_template, url_for, request, flash

import functools
from pymemcache.client.base import Client

import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

port = int(os.environ.get("PORT", 5000))

MEM_HOST = os.environ.get("MEM_HOST")
MEM_PORT = os.environ.get("MEM_PORT", 11211)

client = Client((MEM_HOST, MEM_PORT))


@functools.lru_cache(maxsize=3)
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)


def examine(number):
    try:
        number = int(number)
        return number
    except Exception:
        return False


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/fib_number", methods=['POST'])
def fib_number():
    if request.method == 'POST':
        if examine(request.form['number']):
            number = int(request.form['number'])
            f_number = client.get(str(number))

            if f_number:
                f_number = f_number.decode("utf-8")
                message = 'Данные взяты из memcached.'
                return render_template('fib_number.html', number=number, f_number=f_number, message=message)

            else:
                f_number = fibonacci(number)
                client.set(str(number), str(f_number))
                message = 'Данные вычисленны вновь!'
                return render_template('fib_number.html', number=number, f_number=f_number, message=message)

        else:
            flash("Вы должны ввести целое число!")

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)
