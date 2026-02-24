from flask_login import login_user, login_required, logout_user, current_user
from market import app, db
from flask import render_template, redirect, url_for, flash, session, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from sqlalchemy import func


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

    # KUPI SELECTED
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

    return render_template("cart.html",
                           cart_items=cart_items,
                           total_price=total_price)


@app.route('/add-to-cart/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):

    if "cart" not in session:
        session["cart"] = []

    if item_id not in session["cart"]:
        session["cart"].append(item_id)
        session.modified = True
        flash("Kurs dodat u korpu!", "success")

    return redirect(url_for('courses_page'))


@app.route('/remove-from-cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):

    if "cart" in session and item_id in session["cart"]:
        session["cart"].remove(item_id)
        session.modified = True
        flash("Kurs uklonjen iz korpe.", "warning")

    return redirect(url_for('cart_page'))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():

        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data
        )

        user_to_create.set_password(form.password1.data)

        db.session.add(user_to_create)
        db.session.commit()

        flash("Nalog je uspješno kreiran!", "success")
        return redirect(url_for('login_page'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()

        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash(f"Prijavljeni ste kao {attempted_user.username}", "success")
            return redirect(url_for('home_page'))
        else:
            flash("Neispravno korisničko ime ili lozinka.", "danger")

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    session.pop("cart", None)
    logout_user()
    flash("Uspješno ste se odjavili.", "info")
    return redirect(url_for('home_page'))


# ---------------- ADMIN ----------------

@app.route('/admin')
@login_required
def admin_dashboard():

    if not current_user.is_admin:
        flash("Nemate pristup ovoj stranici.", "danger")
        return redirect(url_for('home_page'))

    total_users = User.query.count()
    total_courses = Item.query.count()
    total_revenue = db.session.query(func.sum(User.total_spent)).scalar() or 0
    top_users = User.query.order_by(User.total_spent.desc()).limit(3).all()
    courses = Item.query.all()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_courses=total_courses,
        total_revenue=total_revenue,
        top_users=top_users,
        courses=courses
    )


@app.route('/add-course', methods=['POST'])
@login_required
def add_course():

    if not current_user.is_admin:
        return redirect(url_for('home_page'))

    name = request.form.get("name")
    price = request.form.get("price")
    description = request.form.get("description")

    new_course = Item(
        name=name,
        price=float(price),
        description=description
    )

    db.session.add(new_course)
    db.session.commit()

    flash("Kurs uspješno dodat!", "success")
    return redirect(url_for('admin_dashboard'))


@app.route('/delete-course/<int:course_id>')
@login_required
def delete_course(course_id):

    if not current_user.is_admin:
        return redirect(url_for('home_page'))

    course = Item.query.get_or_404(course_id)

    db.session.delete(course)
    db.session.commit()

    flash("Kurs obrisan.", "danger")
    return redirect(url_for('admin_dashboard'))