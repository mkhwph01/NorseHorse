import sys

from Project import app, db
from Project import views

def main():
    db.create_all()
    app.run(debug=True)
    return 0

if __name__=='__main__':
    sys.exit(main())