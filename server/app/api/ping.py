from flask_restx import Namespace, Resource
from app.logger import logger

ping_namespace = Namespace("ping")


class Ping(Resource):
    def get(self):
        logger.info("ping")
        return {"status": "success", "message": "pong!"}


ping_namespace.add_resource(Ping, "")
