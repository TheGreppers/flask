"""
UserGear model — stores per-user racing safety equipment with SFI spec tracking.
"""

from __init__ import db
from datetime import datetime


class UserGear(db.Model):
    __tablename__ = 'user_gear'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    spec = db.Column(db.String(50), default='Unknown')
    cert_date = db.Column(db.String(20), default='')       # YYYY-MM-DD or empty
    category = db.Column(db.String(100), default='')
    product_name = db.Column(db.String(255), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'spec': self.spec,
            'certDate': self.cert_date,
            'category': self.category,
            'productName': self.product_name,
        }

    @staticmethod
    def create(user_id, data):
        gear = UserGear(
            user_id=user_id,
            name=data.get('name', '').strip(),
            spec=data.get('spec', 'Unknown').strip(),
            cert_date=data.get('certDate', ''),
            category=data.get('category', ''),
            product_name=data.get('productName', ''),
        )
        db.session.add(gear)
        db.session.commit()
        return gear

    @staticmethod
    def get_by_user(user_id):
        return UserGear.query.filter_by(user_id=user_id).order_by(UserGear.created_at).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
