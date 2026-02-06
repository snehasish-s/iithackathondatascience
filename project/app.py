import os
import pickle
from flask import Flask, render_template, request

from model import load_model, predict

app = Flask(__name__)

# Load or train model at startup
MODEL, TARGET_NAMES = load_model()


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        try:
            # Expect 4 features for Iris
            f1 = float(request.form.get('f1', 0))
            f2 = float(request.form.get('f2', 0))
            f3 = float(request.form.get('f3', 0))
            f4 = float(request.form.get('f4', 0))
            out = predict([f1, f2, f3, f4])
            result = out
        except Exception as e:
            error = str(e)

    return render_template('index.html', result=result, error=error)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
