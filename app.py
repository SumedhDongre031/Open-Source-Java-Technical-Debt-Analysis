from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import numpy as np
from keras.models import load_model

app = Flask(__name__)

# Load the trained model
model = load_model('models/gru_model.h5')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle POST request for prediction
        input_data = [
            request.form.get('fanin'),
            request.form.get('fanout'),
            request.form.get('total_methods'),
            request.form.get('total_variables'),
            request.form.get('total_lines'),
            request.form.get('comment_lines'),
            request.form.get('occurences')
        ]
        input_data = [value for value in input_data if value is not None]
        input_df = pd.DataFrame([input_data], columns=['fanin', 'fanout', 'total_methods', 'total_variables', 'total_lines', 'comment_lines', 'occurences'])
        input_array = input_df.values.astype(float)
        prediction = model.predict(input_array)
        prediction = float(prediction[0][0])
        return jsonify({'prediction': prediction})
    else:
        # Handle GET request to render the index.html template
        return render_template('index.html')

@app.route('/v2')
def v2():
    # Redirect to v2.html
    #return redirect(url_for('v2'))
    return render_template('v2.html')

if __name__ == '__main__':
    app.run(debug=True)
