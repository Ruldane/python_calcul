import json
import os

from flask import Flask, render_template, request, redirect, jsonify, json
import csv
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/')
def my_home():  # put application's code here
    return render_template('index.html')


def test(data):
    return {data}


@app.route('/api/query', methods=['POST', 'GET'])
def api_post():
    if request.method == 'POST':
        req = request.json
        animal = req['animal']
        size = req['size']
        age = req['age']
        sterilise = req['sterilise']

        if sterilise == 'false' and animal == 'chien':
            path = animal + '/croquettesChiensLists/'+age+'/'+size+'.json'
            dataset = open_file_average(path)
        if sterilise == 'true' and animal == 'chien':
            if size == 'xsmall' or size == 'mini':
                pathsize = 'adulteXsmallMiniSterilisé'
            elif size == 'maxi' or size == 'geant':
                pathsize = 'geant'
            else:
                pathsize = 'medium'
            path = animal + '/croquettesChiensLists/'+age+'/AdulteSterilisé/'+pathsize+'.json'
            dataset = open_file_average(path)
        print(dataset)

        foods = calcul_average_price(dataset)
        print(foods)
        return jsonify(foods=foods, animal=animal, size=size, age=age, sterilise=sterilise)


def open_file_average(path):
    with open(os.path.join(os.path.dirname(__file__), path),
              'r') as f:
        data = json.loads(f.read())
        return data


def calcul_average_price_dog(dataset, size):
    xsmall_quantity = 0.115
    mini_quantity = 0.135
    medium_quantity = 0.230
    maxi_quantity = 0.350
    giant_quantity = 0.400
    average = (sum(dataset)/len(dataset))
    if (size == 'xsmall'):
        monthly_price = (average/xsmall_quantity)*30
    elif (size == 'mini'):
        monthly_price = (average / xsmall_quantity) * 30

    return average


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email}, {subject}, {message}')


def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, )
        csv_writer.writerow([email, subject, message])


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('thank_you.html')
        except:
            return 'did not save to database'
    else:
        return 'Something went wrong! Try againnnnnnnn'


if __name__ == '__main__':
    app.run()
