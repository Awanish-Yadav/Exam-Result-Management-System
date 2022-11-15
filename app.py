import os
from rdms import app


if __name__ == '__main__':
    port = int(os.getenv('PORT'))
    app.run(debug=True, port=port)
