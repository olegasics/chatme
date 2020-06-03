import requests

from sqlalchemy_serializer import SerializerMixin

from db_config import db

order_project = db.Table('order_project',
                        db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
                        db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
                        )

order_invoice = db.Table('order_invoice',
                        db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
                        db.Column('invoice_id', db.Integer, db.ForeignKey('invoice.id'), primary_key=True)
                        )


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    small_name = db.Column(db.String(10), nullable=False)
    number_phone = db.Column(db.String(30))
    projects = db.relationship('Project')


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=True)
    customer = db.Column(db.String(100), nullable=False)
    manager = db.relationship(Manager, lazy='joined', innerjoin=True)
    

class Ttn(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)


class Order(db.Model, SerializerMixin):
    serialize_only = (
        'id',
        'state_order',
        'sender',
        'receiver',
        'total_sum',
        'date_delivery',
        'doc_number'
    )
    
    id = db.Column(db.Integer, primary_key=True)
    state_order = db.Column(db.String(50))
    sender = db.Column(db.String(100))
    receiver = db.Column(db.String(100))
    carrier = db.Column(db.String(100), nullable=False)
    total_sum = db.Column(db.Float)
    cargo = db.Column(db.String(300))
    date_delivery = db.Column(db.String(100))
    date_send = db.Column(db.String(100))
    doc_number = db.Column(db.String(30))
    ttn = db.relationship('Ttn', backref='order', lazy='joined', uselist=False)
    projects = db.relationship('Project', secondary='order_project', lazy='joined',
                               backref=db.backref('orders', lazy='joined'))

    invoices = db.relationship('Invoice', secondary='order_invoice', lazy='joined',
                                backref=db.backref('orders', lazy=True))
    
