from flask_migrate import Migrate
from apps.fluidbusiness.views import ProjectsView, LogistsView, OrdersView, ManagersView
from apps.chat.views import RoomAPIView


from db_config import app, db

ProjectsView.register(app)
LogistsView.register(app)
OrdersView.register(app)
ManagersView.register(app)

migrate = Migrate(app, db)


if __name__ == '__main__':
    
    app.run(debug=True)