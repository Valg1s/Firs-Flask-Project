from datetime import datetime
from time import sleep

from flask import render_template, redirect, flash, url_for, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from PIL import Image

from app import app, db
from sweter.models import User, Medicines, Manufacturer, Sales, SalesProduct, Pharmacy, Booking, BookingProduct, \
    Category


@app.route('/')
@app.route('/main')
def home_page():
    return render_template('index.html')


@app.route('/<string:med_name>')
def info_med(med_name):
    med = (db.session.query(Manufacturer, Medicines)
           .join(Medicines, Medicines.id_of_manufacturer == Manufacturer.id_of_man)).filter(
        Medicines.med_name == med_name).first()
    name_of_picture = med[1].name_of_picture
    return render_template('medicine.html', name_of_picture=name_of_picture, med=med)


@app.route('/med', methods=['GET', 'POST'])
@login_required
def med():
    def take_med():
        med = (db.session.query(Manufacturer, Medicines)
               .join(Medicines, Medicines.id_of_manufacturer == Manufacturer.id_of_man)).all()
        return med

    print("Medhot:" + request.method)
    if request.method == "POST":
        search = request.form.get("search")
        print(search)
        if search == "":
            medicines = take_med()
        else:
            medicines = (db.session.query(Manufacturer, Medicines)
                .join(Medicines).filter_by(id_of_manufacturer=Manufacturer.id_of_man).filter_by(
                med_name=search)).all()
            if medicines is None:
                medecines = ((db.session.query(Manufacturer, Medicines)
                    .join(Medicines).filter_by(id_of_manufacturer=Manufacturer.id_of_man).filter_by(
                    category=Category.id_of_cat))).filter_by(name_of_cat=search).all()
    else:
        medicines = take_med()

    return render_template('medicines.html', medicines=medicines)


@app.route('/<string:med_name>/buy', methods=['GET', 'POST'])
def buy_med(med_name):
    med = Medicines.query.filter_by(med_name=med_name).first()
    if request.method == 'POST':
        count = request.form.get('count_of_med')
        if count == '':
            flash("Заповніть усі поля")
            return render_template('buy.html', med=med)
        count = int(count)
        if med.med_count < count:
            flash(f"На складі не має стільки товару, поточна кількість цього товару: {med.med_count}")
            return redirect(url_for('buy_med', med_name=med.med_name))
        id_of_user = current_user.get_id()
        date = datetime.utcnow()
        new_sales = Sales(id_of_user=id_of_user, date=date)

        db.session.add(new_sales)
        db.session.commit()

        sales_id = Sales.query.filter_by(id_of_user=id_of_user, date=date).first().id_of_sales

        new_salesprod = SalesProduct(id_of_sales=sales_id, id_of_med=med.id_of_med, amount=count,
                                     price=count * med.cost)

        db.session.add(new_salesprod)
        db.session.commit()

        med.med_count -= count

        db.session.commit()

        session['order_by'] = 'buy'

        return redirect(url_for('ticket'))

    return render_template('buy.html', med=med)


@app.route('/news')
def news():
    return render_template('news.html')


@app.route('/<string:med_name>/booking', methods=['GET', 'POST'])
def booking_med(med_name):
    med = Medicines.query.filter_by(med_name=med_name).first()
    pharmacy = Pharmacy.query.all()
    if request.method == 'POST':
        count = int(request.form.get('count_of_med'))
        if med.med_count < count:
            flash(f"На складі не має стільки товару, поточна кількість цього товару: {med.med_count}")
            return redirect(url_for('booking_med', med_name=med.med_name))
        if count > 10:
            flash(f"Ви перевищили ліміт в 10 товарів")
            return redirect(url_for('booking_med', med_name=med.med_name))
        id_of_user = current_user.get_id()
        id_of_phar = int(request.form.get('pharmacy'))
        date = datetime.utcnow()
        new_booking = Booking(id_of_user=id_of_user, id_of_phar=id_of_phar, date=date, status="В обробці")

        db.session.add(new_booking)
        db.session.commit()

        booking_id = Booking.query.filter_by(id_of_user=id_of_user, date=date).first().id_of_booking

        new_bookingprod = BookingProduct(id_of_booking=booking_id, id_of_med=med.id_of_med, amount=count)

        db.session.add(new_bookingprod)
        db.session.commit()

        med.med_count -= count

        db.session.commit()

        session['order_by'] = 'booking'

        return redirect(url_for('ticket'))

    return render_template('booking1.html', med=med, pharmacy=pharmacy)


@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
    type = session['order_by']
    id_of_user = current_user.get_id()

    if type == "buy":
        order = (db.session.query(SalesProduct, Sales)
                 .join(Sales).filter_by(id_of_sales=Sales.id_of_sales)
                 .filter_by(id_of_user=id_of_user)).order_by(
            SalesProduct.id_of_prod_sales.desc()).first()
    if type == "booking":
        order = (db.session.query(BookingProduct, Booking)
                 .join(Booking).filter_by(id_of_booking=Booking.id_of_booking)
                 .filter_by(id_of_user=id_of_user)).order_by(
            BookingProduct.id_of_prod_booking.desc()).first()
    print(order)
    return render_template('ticket.html', order_by=type, order=order)


@app.route('/registration', methods=['GET', 'POST'])
def reg_page():
    full_name = request.form.get('full_name')
    login = request.form.get('login')
    tel_number = request.form.get('tel_number')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not full_name or not login or not tel_number or not email or not password or not password2:
            flash("Введідь усі поля")
            return redirect(url_for('reg_page'))
        elif password != password2:
            flash("Паролі не співпали")
        elif User.query.filter_by(full_name=full_name).first() or User.query.filter_by(
                login=login).first() or User.query.filter_by(email=email).first():
            flash("Цей користувач вже зареєстрований. Переадресація...")
            sleep(1)
            return redirect(url_for('log_page'))
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(full_name=full_name, email=email, login=login, password=hash_pwd, role='user',
                            telephone_number=tel_number)

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('log_page'))
        return redirect(url_for('reg_page'))

    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def log_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            print("User was login")
            return redirect(url_for('home_page'))
        else:
            flash("Не правильний логін чи пароль ")
            return render_template("login.html")
    else:
        flash("Введіть данні")
        return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/cabinet')
@login_required
def cabinet():
    user_id = current_user.get_id()
    user = User.query.filter_by(id_of_user=user_id).first()

    orders_buy = (db.session.query(SalesProduct, Sales, Medicines)
        .join(Sales).filter_by(id_of_sales=Sales.id_of_sales)
        .filter_by(id_of_user=user_id).join(Medicines).filter(
        SalesProduct.id_of_med == Medicines.id_of_med)).all()
    orders_booking = (db.session.query(BookingProduct, Booking, Medicines, Pharmacy)
                      .join(Booking, BookingProduct.id_of_booking == Booking.id_of_booking)
                      .join(Medicines, BookingProduct.id_of_med == Medicines.id_of_med)
                      .join(Pharmacy, Booking.id_of_phar == Pharmacy.id_of_phar)
                      .filter(Booking.id_of_user == user_id)).all()

    return render_template("cabinet.html", user=user, orders_buy=orders_buy, orders_booking=orders_booking)


@app.route('/main/<string:name>:<string:password>')
@login_required
def admin_main(name, password):
    user_id = current_user.get_id()
    user = User.query.filter_by(id_of_user=user_id).first()
    if user.role == 'admin':
        if name == 'admin' and password == 'admin':
            id_of_orders = request.args.get('id')
            command = request.args.get('command')

            if id_of_orders is not None and command is not None:
                if command == "delete_booking":
                    post = (db.session.query(BookingProduct, Booking)
                            .join(Booking, BookingProduct.id_of_booking == Booking.id_of_booking)
                            .filter(BookingProduct.id_of_prod_booking == id_of_orders)).first()

                    db.session.delete(post[1])
                    db.session.delete(post[0])

                    db.session.commit()
                if command == "delete_sales":
                    post = (db.session.query(SalesProduct, Sales)
                            .join(Sales, SalesProduct.id_of_sales == Sales.id_of_sales)
                            .filter(SalesProduct.id_of_prod_sales == id_of_orders)).first()

                    db.session.delete(post[1])
                    db.session.delete(post[0])

                    db.session.commit()
                if command == "change_status":
                    post = Booking.query.filter_by(id_of_booking=id_of_orders).first()
                    post.status = "Виконано"

                    db.session.commit()

            orders_buy = (db.session.query(SalesProduct, Sales, Medicines)
                .join(Sales).filter_by(id_of_sales=Sales.id_of_sales).join(Medicines).filter(
                SalesProduct.id_of_med == Medicines.id_of_med)).all()
            orders_booking = (db.session.query(BookingProduct, Booking, Medicines, Pharmacy)
                              .join(Booking, BookingProduct.id_of_booking == Booking.id_of_booking)
                              .join(Medicines, BookingProduct.id_of_med == Medicines.id_of_med)
                              .join(Pharmacy, Booking.id_of_phar == Pharmacy.id_of_phar)).all()
            return render_template('admin.html', orders_buy=orders_buy, orders_booking=orders_booking)
        else:
            return redirect(url_for('home_page'))
    else:
        return redirect(url_for('home_page'))


@app.route('/<string:name>:<string:password>/add_med', methods=["GET", "POST"])
@login_required
def admin_add_med(name, password):
    user_id = current_user.get_id()
    user = User.query.filter_by(id_of_user=user_id).first()
    if user.role == 'admin':
        if name == 'admin' and password == 'admin':
            if request.method == "POST":
                med_name = request.form.get('name')
                count = request.form.get('count')
                form_of_production = request.form.get('form_of_prod')
                title_of_man = request.form.get('manufacturer_name')
                country = request.form.get('country_of_manufacturer')
                price = request.form.get('price')
                name_of_cat = request.form.get('name_category')
                active_substance = request.form.get('active_substance')
                volume_of_active_substance = request.form.get('volume_active_substance')
                volume = request.form.get('volume')
                picture = request.files['photo']

                if not med_name or not count or not form_of_production or not title_of_man or not country or not price or not name_of_cat or not active_substance or not volume_of_active_substance or not volume or not picture:
                    flash("Введіть усі дані")
                    return redirect(url_for('admin_add_med', name='admin', password='admin'))
                else:
                    name_of_picture = med_name.replace(' ', '') + ".png"

                    with Image.open(picture) as img:
                        img.save(f"./templates/static/images/{name_of_picture}")

                    man = Manufacturer.query.filter_by(title_of_man=title_of_man).first()
                    if not man:
                        manuf = Manufacturer(title_of_man=title_of_man, country=country)

                        db.session.add(manuf)
                        db.session.commit()

                        man = Manufacturer.query.filter_by(title_of_man=title_of_man).first().id_of_man

                    else:
                        man = man.id_of_man

                    cat = Category.query.filter_by(name_of_cat=name_of_cat).first()

                    if not cat:
                        category = Category(name_of_cat=name_of_cat)

                        db.session.add(category)
                        db.session.commit()

                        cat = Category.query.filter_by(name_of_cat=name_of_cat).first().id_of_cat

                    else:
                        cat = cat.id_of_cat

                    new_med = Medicines(med_name=med_name, med_count=count, form_of_production=form_of_production,
                                        id_of_manufacturer=man, cost=price, category=cat,
                                        active_substance=active_substance,
                                        volume_of_active_substance=volume_of_active_substance, volume=volume,
                                        name_of_picture=name_of_picture)

                    db.session.add(new_med)
                    db.session.commit()

                    db.session.close()

            return render_template('add_med.html')

@app.route('/repair')
def repair():
    return render_template('repair.html')