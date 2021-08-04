import os
from api import create_app

port = int(os.environ.get('PORT', 8080))
server = create_app()

if __name__ == '__main__':
    from waitress import serve
    serve(server,host="0.0.0.0",port=port)