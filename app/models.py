from app import db


class Query(db.Model):
    __tablename__ = 'query'
    # PLACEHOLDER DB CLASS
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "Query id: {}".format(self.id)

