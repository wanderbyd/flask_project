from app import db

class Bookmark(db.Model):
    __tablename__ = 'bookmark'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    url = db.Column(db.Text, nullable=False)
    member = db.Column(db.Text, nullable=True)

    def __init__(self, title, url, member=None):
        self.title = title
        self.url = url
        self.member = member