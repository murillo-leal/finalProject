import os
from flask import url_for
import don_hermano.routes
import don_hermano.models

app = don_hermano.routes.app

if __name__ == '__main__':
    don_hermano.models.initialize()    
    app.run(debug=True, threaded=True)