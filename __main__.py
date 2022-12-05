from server import create_app, configuration

#Run in development mode
app = create_app(configuration_mode=configuration.Dev)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    # app.run()