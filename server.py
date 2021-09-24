import json
import os

from flask import Flask, render_template, request, redirect, jsonify, json
import csv
from flask_cors import CORS

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
            path = animal + '/croquettesChiensLists/' + age + '/' + size + '.json'
            dataset = open_file_average(path)
        if sterilise == 'true' and animal == 'chien':
            if size == 'xsmall' or size == 'mini':
                pathsize = 'small'
            elif size == 'maxi' or size == 'geant':
                pathsize = 'big'
            else:
                pathsize = 'medium'
            path = animal + '/croquettesChiensLists/' + 'chiensSterilises/' + age + '/' + pathsize + '.json'
            dataset = open_file_average(path)

        averageCostToy = toyDog(animal, size)
        foods = calcul_average_price_dog_food(dataset, size)
        averageCostLeashCollar = leashCost(animal)
        healthCostDog = HealthCost(animal)

        return jsonify(foods=foods, averageCostToy=averageCostToy, healthCostDog=healthCostDog, averageCostLeashCollar=averageCostLeashCollar,
                       animal=animal, size=size, age=age,
                       sterilise=sterilise)


def open_file_average(path):
    with open(os.path.join(os.path.dirname(__file__), path),
              'r') as f:
        data = json.loads(f.read())
        return data


def HealthCost(animal):
    if animal == 'chien':
        dataHealthCost = open_file_average('chien/entretienAntiparasitaireChiens.json')
    healthCostDog = sum(dataHealthCost) / len(dataHealthCost)
    return healthCostDog


def leashCost(animal):
    if animal == 'chien':
        dataLeash = open_file_average('chien/laisseColliersChiens/laisseChiens.json')
        dataCollar = open_file_average('chien/laisseColliersChiens/colliersChiens.json')
    averageCostLeashCollar = (sum(dataLeash) / len(dataLeash) + (sum(dataCollar) / len(dataCollar)))
    return averageCostLeashCollar


def toyDog(animal, size):
    if animal == 'chien':
        if size == 'xsmall' or size == 'mini':
            pathsize = 'small'
        elif size == 'maxi' or size == 'geant':
            pathsize = 'big'
        else:
            pathsize = 'medium'
        dataToy = open_file_average('chien/jouetsChiensLists/' + pathsize + '.json')
    averageCostToy = sum(dataToy) / len(dataToy)
    return averageCostToy


def calcul_average_price_dog_food(dataset, size):
    xsmall_quantity = 0.115
    mini_quantity = 0.135
    medium_quantity = 0.230
    maxi_quantity = 0.350
    giant_quantity = 0.400
    average = (sum(dataset) / len(dataset))
    if size == 'xsmall':
        monthly_price = (average * mini_quantity) * 30
    elif size == 'mini':
        monthly_price = (average * xsmall_quantity) * 30
    elif size == 'medium':
        monthly_price = (average * medium_quantity) * 30
    elif size == 'maxi':
        monthly_price = (average * maxi_quantity) * 30
    elif size == 'geant':
        monthly_price = (average * giant_quantity) * 30
    return monthly_price


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
