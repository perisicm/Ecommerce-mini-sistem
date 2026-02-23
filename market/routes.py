from market import app, db
from flask import render_template, redirect, url_for, flash, session, request
from market.models import Item


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/courses')
def courses_page():
    items = Item.query.all()
    return render_template('courses.html', items=items)


@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    return render_template('cart.html', cart_items=[], total_price=0)
