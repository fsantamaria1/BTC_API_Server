from server import create_app, configuration

#Run in development mode
app = create_app(configuration_mode=configuration.Dev)

if __name__ == '__main__':
    app.run()