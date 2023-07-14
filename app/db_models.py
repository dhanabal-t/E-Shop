from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(UserMixin, db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	email = db.Column(db.String(50), nullable=False)
	phone = db.Column(db.Integer, nullable=False)
	password = db.Column(db.String(250), nullable=False)
	cart = db.relationship('Cart', backref='buyer')

	def add_to_cart(self, itemid, quantity):
		item_to_add = Cart(itemid=itemid, uid=self.id, quantity=quantity)
		db.session.add(item_to_add)
		db.session.commit()

	def remove_from_cart(self, itemid, quantity):
		item_to_remove = Cart.query.filter_by(itemid=itemid, uid=self.id, quantity=quantity).first()
		db.session.delete(item_to_remove)
		db.session.commit()

class Item(db.Model):
	__tablename__ = "items"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	price = db.Column(db.Float, nullable=False)
	category = db.Column(db.Text, nullable=False)
	image = db.Column(db.String(250), nullable=False)
	details = db.Column(db.String(250), nullable=False)
	price_id = db.Column(db.String(250), nullable=False)
	in_cart = db.relationship("Cart", backref="item")

class Cart(db.Model):
	__tablename__ = "cart"
	id = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	itemid = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
	quantity = db.Column(db.Integer, nullable=False, default=1)
