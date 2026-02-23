from flask_login import login_user, login_required, logout_user, current_user
from market import app, db
from flask import render_template, redirect, url_for, flash, session, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/courses')
def courses_page():
    items = Item.query.all()
    return render_template('courses.html', items=items)


@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart_page():
    if "cart" not in session:
        session["cart"] = []

    if request.method == "POST":
        selected_ids = request.form.getlist("selected_items")
        if selected_ids:
            selected_ids = list(map(int, selected_ids))
            selected_items = Item.query.filter(Item.id.in_(selected_ids)).all()
            total = sum(item.price for item in selected_items)

            if current_user.budget >= total:
                current_user.budget -= total
                current_user.total_spent += total
                db.session.commit()
                session["cart"] = []
                session.modified = True
                flash(f"Uspješno ste kupili kurseve u vrijednosti ${total:.2f}", "success")
            else:
                flash("Nemate dovoljno novca na računu!", "danger")

        return redirect(url_for("cart_page"))

    cart_items = Item.query.filter(Item.id.in_(session["cart"])).all()
    total_price = sum(item.price for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total_price=total_price)


@app.route('/add-to-cart/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
    if "cart" not in session:
        session["cart"] = []
    if item_id not in session["cart"]:
        session["cart"].append(item_id)
        session.modified = True
        flash("Course added to cart!", "success")
    return redirect(url_for('courses_page'))


@app.route('/remove-from-cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    if "cart" in session and item_id in session["cart"]:
        session["cart"].remove(item_id)
        session.modified = True
        flash("Course removed from cart.", "warning")
    return redirect(url_for('cart_page'))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists!", "danger")
            return redirect(url_for('register_page'))

        existing_email = User.query.filter_by(email_address=form.email_address.data).first()
        if existing_email:
            flash("Email already registered!", "danger")
            return redirect(url_for('register_page'))

        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data
        )
        user_to_create.set_password(form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for('login_page'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash(f"Logged in as {attempted_user.username}", "success")
            return redirect(url_for('home_page'))
        else:
            flash("Username or password incorrect", "danger")

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    session.pop("cart", None)
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('home_page'))