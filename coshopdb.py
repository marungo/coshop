class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    products = db.relationship('Product', secondary=commits, 
    				backref=db.backref('user',lazy='select'), lazy='select')

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name


commits = db.Table('commits',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('prod_id', db.Integer, db.ForeignKey('product.asin'))
)


class Product(db.Model):
    asin = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    price = db.Column(db.String(10))
    unit_price = db.Column(db.String(10))
    pack_of = db.Column(db.String(10))
    users = db.relationship('User', backref=db.backref('product',
    							lazy='dynamic'))


    def __init__(self, title, price, pack_of):
        self.title = title
        self.price = price
        self.pack_of = pack_of

    def __repr__(self):
        return '<Title %r>' % self.title


# user = User('John Doe', 'john.doe@example.com')
# db.session.add(user)
# db.session.commit()