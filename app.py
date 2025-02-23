import io
import matplotlib.pyplot as plt
from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'

@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name

@app.cli.command()
def hello():
    """Just say hello."""
    click.echo('Hello, Human!')

@app.route('/chart')
def chart():
    # Generate a simple chart
    plt.figure(figsize=(5, 5))
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.title('Sample Chart')

    # Save the chart to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return Response(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
