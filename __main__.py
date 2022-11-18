from __init__ import create_app

try:
    app = create_app()
except:
    print("Error")