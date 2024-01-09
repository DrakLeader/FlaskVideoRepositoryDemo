from flask import Flask, render_template

app = Flask(__name__)

# Register other module's blueprint

# Global config


# Home route
@app.route('/')
def home():
    return render_template('index.html')




if __name__ == '__main__':
    app.run()
