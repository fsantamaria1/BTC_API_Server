from server import create_app, configuration

try:
    #Run in development mode
    app = create_app(configuration_mode=configuration.Dev)
except:
    print("Error")

if __name__ == '__main__':
    app.run()