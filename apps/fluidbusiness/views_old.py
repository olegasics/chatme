import requests

from flask.views import MethodView, request
from flask import render_template, url_for, redirect
from sqlalchemy.orm import  joinedload

from apps.fluidbusiness.models import Order, Manager, Project, Invoice, Ttn
from db_config import db, app



class OrderAPIView(MethodView):
    # @cache.cached(timeout=3600)
    def get(self, order_id):
        ended = request.args.get('ended')
        # query = db.session.query(Order).options(joinedload('invoices'), joinedload('ttn'))
        query = db.session.query(Order).join('invoices')
        orders = query.filter(Order.state_order != 'Заказ завершен').all()

        if ended == '0':
            orders = query.all()
        elif ended == '1':
            orders = query.filter(Order.state_order != 'Заказ завершен').all()

        projects = db.session.query(Project).options(joinedload('manager')).all()

        return render_template('orders.html', orders=orders, projects=projects, ended=ended)

    def post(self, order_id):
        name = request.form['name']
        ttn_name = request.form['ttn']

        ttn = Ttn(name=ttn_name, order_id=order_id)
        db.session.add(ttn)

        project = Project.query.filter_by(name=name).first()
        try:
            invoice_name = request.form['invoice']
            if invoice_name == 'No invoice':
                invoice = Invoice.query.filter_by(name=invoice_name).first()
            invoice = Invoice(name=invoice_name, project_id=project.id)
        except Exception:
            invoice = Invoice.query.filter_by(name='No invoice').first()
        
        order = Order.query.get(order_id)
        # order.ttn.append(ttn)
        order.projects.append(project)
        order.invoices.append(invoice)
        
        db.session.commit()
        
        return order.to_dict()

    def update(self, order_id):
        return 'test'    


class ManagerAPIView(MethodView):
    
    def get(self):
        managers = Manager.query.all()
        return render_template('manager.html', managers=managers)

    def post(self):
        name = request.form['name']
        small_name = request.form['small_name']
        number_phone = request.form['number_phone']
        manager = Manager(name=name, small_name=small_name, number_phone=number_phone)
        db.session.add(manager)
        db.session.commit()
        return render_template('manager.html')

    def update(self):
        pass

    def delete(self):
        pass


class ProjectAPIView(MethodView):

    def test():
        return 'hi'

    def get(self):
        projects = Project.query.all()
        managers = Manager.query.all()
        return render_template('project.html', projects=projects, managers=managers)

    def post(self):
        name = request.form['name']
        manager_name = request.form['manager_small_name']
        manager = Manager.query.filter_by(small_name=manager_name).first()
        customer = request.form['customer']
        project = Project(name=name, manager_id=manager.id, customer=customer)
        db.session.add(project)
        project.manager.append(manager)
        db.session.commit()
        return render_template('project.html')

    def update(self):
        pass

    def delete(self):
        pass


class LogistAPIView(MethodView):
    # @cache.cached(timeout=3600)
    def get(self, id):
        projects = Project.query.all()
        orders = db.session.query(Order).options(joinedload('ttn')).all()
        return render_template('logist_settings.html', orders=orders, projects=projects)

    def post(self):
        response = requests.post('https://api.dellin.ru/v3/orders.json', json={
                "appkey": "94B2B188-D518-427B-B396-D36C0D877F34",
                "sessionID": "1DD2C5A6-D387-41CE-8197-A4F42118DA92",
                "page": 1,
                "orderDatesExtended": True,
                "orderBy": "ordered_at"
            })
            
        for order in response.json()['orders']:

            state_order = order['stateName']
            sender = order['sender']['name']
            receiver = order['receiver']['name']
            total_sum = order['totalSum']
            date_delivery = order['orderDates']['arrivalToOspReceiver']
            documents = order['documents']

            if date_delivery is None:
                date_delivery = 'Unknown'
            
            try:
                doc_number_old = documents[0].get('id')
                doc_number = documents[1].get('id')
            except Exception:
                doc_number = documents[0].get('id')

            order_check = Order.query.filter_by(doc_number=str(doc_number_old)).first() # TODO
            
            if order_check is None:
                new_order = Order(
                    state_order=state_order, 
                    sender=sender, 
                    receiver=receiver,
                    total_sum=total_sum,
                    date_delivery=date_delivery, 
                    doc_number=doc_number
                )
                db.session.add(new_order)
            else:
                order_check.doc_number = doc_number
                order_check.state_order = state_order

        db.session.commit()

        return redirect(url_for('order_api'))
