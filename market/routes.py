from market import app
from flask import render_template

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/courses')
def courses_page():
    return render_template('courses.html', items=[])


@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    return render_template('cart.html', cart_items=[], total_price=0)
