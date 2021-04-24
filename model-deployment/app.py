import flask
import pickle
import pandas as pd

# load pre-trained model
with open(f'model/houseprice_model_rf.pkl', 'rb') as f:
    model = pickle.load(f)

app = flask.Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
    if flask.request.method == 'POST':
        overall_qual = flask.request.form['overallqual']
        gr_liv_area = flask.request.form['grlivarea']
        total_bsmt_sf = flask.request.form['totalbsmtsf']
        second_floor_sf = flask.request.form['secondfloorsf']
        garage_cars = flask.request.form['garagecars']
        print('Successfully received fields.')
        # print(overall_qual)
        # print(gr_liv_area)
        # print(total_bsmt_sf)
        # print(second_floor_sf)
        # print(garage_cars)

        input_variables = pd.DataFrame([[overall_qual, gr_liv_area, total_bsmt_sf, second_floor_sf, garage_cars]], 
            columns=['OverallQual', 'GrLivArea', 'TotalBsmtSF', '2ndFlrSF','GarageCars'],
            dtype=float
        )
        
        prediction = model.predict(input_variables)[0]
        print('Prediction:', prediction)

        return flask.render_template('index.html',
            original_input={
                'OverallQual': overall_qual,
                'GrLivArea': gr_liv_area,
                'TotalBsmtSF': total_bsmt_sf,
                'GarageCars': garage_cars
            },
            result = prediction
        )

if __name__ == '__main__':
    app.run(debug=True)
