from flask_login import UserMixin

from sweter import db, manager


class Medicines(db.Model):
    __tablename__ = "medicines"
    id_of_med = db.Column(db.Integer(), primary_key=True)
    med_name = db.Column(db.String(128), nullable=False)
    med_count = db.Column(db.Integer(), nullable=False)
    form_of_production = db.Column(db.String(60), nullable=False)
    id_of_manufacturer = db.Column(db.Integer(), db.ForeignKey('manufacturer.id_of_man'), nullable=False)
    cost = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.Integer(), db.ForeignKey('category.id_of_cat'), nullable=False)
    active_substance = db.Column(db.String(128), nullable=False)
    volume_of_active_substance = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, nullable=False)
    name_of_picture = db.Column(db.String(64) ,nullable=False)
    fk_sales_product = db.relationship("SalesProduct")
    fk_booking_product = db.relationship("BookingProduct")


class Manufacturer(db.Model):
    __tablename__ = "manufacturer"
    id_of_man = db.Column(db.Integer(), primary_key=True)
    title_of_man = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(128), nullable=False)
    fk_medicines = db.relationship("Medicines")


class Category(db.Model):
    __tablename__ = "category"
    id_of_cat = db.Column(db.Integer(), primary_key=True)
    name_of_cat = db.Column(db.String(128), nullable=False)
    fk_medicines = db.relationship("Medicines")


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id_of_user = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    telephone_number = db.Column(db.Integer())
    role = db.Column(db.String(8), nullable=False)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False, unique=True)
    address = db.Column(db.String(128))
    fk_sales = db.relationship("Sales")
    fk_booking = db.relationship("Booking")

    def get_id(self):
        return (self.id_of_user)



class Pharmacy(db.Model):
    __tablename__ = "pharmacy"
    id_of_phar = db.Column(db.Integer, primary_key=True)
    adress_of_phar = db.Column(db.String(128), nullable=False)
    number_of_phar = db.Column(db.Integer, unique=True)
    fk_booking = db.relationship("Booking")


class Sales(db.Model):
    __tablename__ = "sales"
    id_of_sales = db.Column(db.Integer(), primary_key=True)
    id_of_user = db.Column(db.Integer(), db.ForeignKey('user.id_of_user'))
    date = db.Column(db.DateTime(), nullable=False)
    fk_sales_product = db.relationship("SalesProduct")


class SalesProduct(db.Model):
    __tablename__ = "sales_product"
    id_of_prod_sales = db.Column(db.Integer(), primary_key=True)
    id_of_sales = db.Column(db.Integer, db.ForeignKey('sales.id_of_sales'))
    id_of_med = db.Column(db.Integer, db.ForeignKey('medicines.id_of_med'))
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)


class Booking(db.Model):
    __tablename__ = "booking"
    id_of_booking = db.Column(db.Integer(), primary_key=True)
    id_of_user = db.Column(db.Integer(), db.ForeignKey('user.id_of_user'))
    id_of_phar = db.Column(db.Integer(), db.ForeignKey('pharmacy.id_of_phar'))
    date = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.String(32), nullable=False)
    fk_booking_product = db.relationship("BookingProduct")


class BookingProduct(db.Model):
    __tablename__ = "booking_product"
    id_of_prod_booking = db.Column(db.Integer(), primary_key=True)
    id_of_booking = db.Column(db.Integer, db.ForeignKey('booking.id_of_booking'))
    id_of_med = db.Column(db.Integer, db.ForeignKey('medicines.id_of_med'))
    amount = db.Column(db.Integer, nullable=False)

db.create_all()

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)




