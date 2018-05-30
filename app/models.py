from app import db


class Query(db.Model):
    __tablename__ = 'query'
    # PLACEHOLDER DB CLASS
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String)
    title = db.Column(db.String)
    date = db.Column(db.String)
    trading_name = db.Column(db.String)
    address = db.Column(db.String)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    brand = db.Column(db.String)

    def __repr__(self):
        return "Query id: {}\n Product: {}\nDate: {}".format(self.id,
                                                             self.product,
                                                             self.date)



