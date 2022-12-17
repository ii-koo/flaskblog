from webapp import run_app

app = run_app()

if __name__ == '__main__':
    app.run(debug=True, port=3000)
