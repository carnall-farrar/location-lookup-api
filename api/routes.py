from flask import Blueprint, jsonify
from .models import CcgToStpLookup

server_bp = Blueprint('ccgToStp', __name__)


@server_bp.route('/', methods=['GET'])
def hello():
    return 'Hello world!'


@server_bp.route('/data')
def getData():
    data = CcgToStpLookup.query.all()
    return jsonify(data)
