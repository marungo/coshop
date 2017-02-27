from coshop import db
from sqlalchemy.dialects.postgresql import JSON


# commits = db.Table('commits',
# 	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
# 	db.Column('prod_id', db.Integer, db.ForeignKey('product.asin'))
# )

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    # products = db.relationship('Product', secondary=commits, 
    # 				backref=db.backref('user',lazy='select'), lazy='select')

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name


class Product(db.Model):
    __tablename__ = 'products'

    asin = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(200))
    price = db.Column(db.String(10))
    unit_price = db.Column(db.String(10))
    pack_of = db.Column(db.String(10))
    url = db.Column(db.String(200))
    # users = db.relationship('User', backref=db.backref('product',
    # 							lazy='dynamic'))


    def __init__(self, asin, title, price, unit_price, pack_of,url):
        self.asin = asin
        self.title = title
        self.price = price
        self.unit_price = unit_price
        self.pack_of = pack_of
        self.url = url

    def __repr__(self):
        return '<Title %r>' % self.title

# def add_product_to_db(product):
# 	prod = Product(asin=product['asin'], title=product['title'],
# 					price=product['price'][0], unit_price=product['unit_price'],
# 					pack_of=product['pack_of'])
# 	db.session.add(prod)
# 	db.session.commit()

############ END DATABASE ###############