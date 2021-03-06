import requests

from flask.views import MethodView, request
from flask import render_template, url_for, redirect, flash
from flask_classy import FlaskView, route
from sqlalchemy.orm import  joinedload

from apps.fluidbusiness.models import Order, Manager, Project, Invoice, Ttn
from db_config import db, app, APP_KEY, SESSION_ID


class OrdersView(FlaskView):
    # @cache.cached(timeout=3600)
    def get(self):
        ended = request.args.get('ended')
        # query = db.session.query(Order).options(joinedload('invoices'), joinedload('ttn'))
        query = db.session.query(Order).options(joinedload('invoices'))
        orders = query.filter(Order.state_order != 'Заказ завершен').all()

        if ended == '0':
            orders = query.all()
        elif ended == '1':
            orders = query.filter(Order.state_order != 'Заказ завершен').all()

        projects = db.session.query(Project).options(joinedload('manager')).all()

        return render_template('orders.html', orders=orders, projects=projects, ended=ended)

    
    def patch(self, order_id):
        project_name = request.form.get('name')
        ttn_name = request.form.get('ttn')
        invoice_name = request.form.get('invoice')
        cargo = request.form.get('cargo')

        order = Order.query.get(order_id)
        project = Project.query.filter_by(name=project_name).first()
        ttn = Ttn.query.filter_by(name=ttn_name).first()

        if project:
            order.projects.append(project)
        
        if ttn is None:
            ttn = Ttn(name=ttn_name, order_id=order_id)
            db.session.add(ttn)
        else:
            order.ttn = ttn 

        if order.invoices:
            order.invoices[0].name = invoice_name
        else:
            invoice = Invoice(name=invoice_name, project_id=project.id)
            order.invoices.append(invoice)
        
        order.cargo = cargo
        db.session.commit()
        
        return order.to_dict()

    def post(self):
        project_name = request.form['name']
        cargo = request.form['cargo']
        status = request.form['status']
        sender = request.form['sender']
        receiver = request.form['receiver']
        document = request.form['document']
        carrier = request.form['carrier']
        ttn_name = request.form['ttn']

        project = Project.query.filter_by(name=project_name).first()

        try:
            invoice_name = request.form['invoice']
            if invoice_name == 'No invoice':
                invoice = Invoice.query.filter_by(name=invoice_name).first()
            invoice = Invoice(name=invoice_name, project_id=project.id)
        except Exception:
            invoice = Invoice.query.filter_by(name='No invoice').first()

        ttn = Ttn(name=ttn_name)
        
        order = Order(
            state_order=status, 
            sender=sender, 
            receiver=receiver, 
            doc_number=document, 
            carrier=carrier,
            ttn=ttn
        )

        order.projects.append(project)
        order.invoices.append(invoice)

        db.session.add(order)
        db.session.commit()
        
        return order.to_dict() 


class ManagersView(FlaskView):
    
    def get(self):
        managers = Manager.query.all()
        return render_template('manager.html', managers=managers)

    def post(self, endpoint='create'):
        name = request.form['name']
        small_name = request.form['small_name']
        number_phone = request.form['number_phone']
        manager = Manager(name=name, small_name=small_name, number_phone=number_phone)
        db.session.add(manager)
        db.session.commit()
        managers = Manager.query.all()
        return redirect({{ url_for('ManagerView:get') }})

    def update(self):
        pass

    def delete(self):
        pass


class ProjectsView(FlaskView):  

    def get(self):
        projects = Project.query.all()
        managers = Manager.query.all()
        return render_template('project.html', projects=projects, managers=managers)

   
    def post(self, endpoint='create'):
        name = request.form['name']
        manager_small_name = request.form['manager_small_name']
        manager = Manager.query.filter_by(small_name=manager_small_name).first()
        customer = request.form['customer']
        
        project = Project(name=name, manager_id=manager.id, customer=customer)
        manager.projects.append(project)

        db.session.add(project)
        db.session.commit()

        return redirect(url_for('ProjectView:get'))

    @route('/<project_name>')
    def get_by_name(self, project_name):
        project = db.session.query(Project).filter_by(name=project_name).options(joinedload('manager')).first()
        return render_template('info_project.html', project=project)


class LogistsView(FlaskView):
    # @cache.cached(timeout=3600)
    def get(self):
        projects = Project.query.all()
        orders = db.session.query(Order).options(joinedload('ttn')).all()
        return render_template('logist_settings.html', orders=orders, projects=projects)
    
    
    def post(self, endpoint='update-orders'):
        response = requests.post('https://api.dellin.ru/v3/orders.json', json={
                "appkey": APP_KEY,
                "sessionID": SESSION_ID,
                "page": 1,
                "orderDatesExtended": True,
                "orderBy": "ordered_at"
            })

        carrier = 'DL'    
            
        for order in response.json()['orders']:

            state_order = order['stateName']
            sender = order['sender']['name']
            receiver = order['receiver']['name']
            total_sum = order['totalSum']
            date_delivery = order['orderDates']['arrivalToOspReceiver']
            documents = order['documents']
            date_send = order['stateDate']

            if date_delivery is None:
                date_delivery = 'Unknown'
            
            try:
                # doc_number_old = documents[0].get('id')
                doc_number = documents[1].get('id')
            except Exception:
                doc_number = documents[0].get('id')

            order_check = Order.query.filter_by(doc_number=str(doc_number)).first() # TODO
            
            if order_check is None:
                new_order = Order(
                    state_order=state_order, 
                    sender=sender, 
                    receiver=receiver,
                    total_sum=total_sum,
                    date_delivery=date_delivery, 
                    doc_number=doc_number,
                    carrier=carrier,
                    date_send=date_send
                )
                db.session.add(new_order)
            else:
                order_check.doc_number = doc_number
                order_check.state_order = state_order
                date_send=date_send

        db.session.commit()

        return redirect(url_for('OrderView:get'))

