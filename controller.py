from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms import validators
import pickle
import gzip

# vInitialize Flask App
app = Flask(__name__)

# Initialize Form Class
# This form will take in the form data on the front end and use it to predict
# using a pre-loaded model
class PredictForm(FlaskForm):
    code = TextAreaField('Code to translate (max 800 chars):',
                         validators=[validators.required(),
                                     validators.length(max=800)])
    submit = SubmitField('Submit')

# load model and load it in memory

with gzip.open('data/model.pkl.gz') as fin:
    model, target_names = pickle.load(fin)

#model, target_names = ...

print("Model loaded in memory. Ready to roll!")

@app.route('/', methods=['GET', 'POST'])
def translate():
    prediction, code = None, None
    predict_form = PredictForm(csrf_enabled=False)

    if predict_form.validate_on_submit():

        # store the submitted values
        submitted_data = predict_form.data
        print(submitted_data)

        # Retrieve values from form
        code = submitted_data['code']

        # Predict the class corresponding to the code
        predicted_class_n = model.predict([code])[0]

        # Get the corresponding class name and make it pretty
        prediction = target_names[predicted_class_n].capitalize()
        print(prediction)

    # Pass the predicted class name to the fron-end
    return render_template('model.html',
                           predict_form=predict_form,
                           prediction=prediction)

# Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)