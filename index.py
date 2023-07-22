from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, jsonify, request, render_template
from goldys_data import goldys

app = Flask(__name__)

# Configurações do Swagger
SWAGGER_URL = '/api/docs'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API MM2"
    }
)

# Registro do blueprint do Swagger UI
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/brazilhangout/mm2', methods=['GET'])
def obter_goldys():
    return jsonify(goldys)


@app.route('/brazilhangout/mm2/<string:Name>', methods=['GET'])
def obter_goldy(Name):
    for goldy in goldys:
        if goldy['Nome'] == Name:
            return jsonify(goldy)
    return jsonify({'error': 'Goldy não encontrado'})


@app.route('/brazilhangout/mm2/<string:Name>', methods=['PUT'])
def editar_goldy(Name):
    goldy_alterada = request.get_json()
    for indice, goldy in enumerate(goldys):
        if goldy.get('Nome') == Name:
            goldys[indice].update(goldy_alterada)
            return jsonify(goldys[indice])


@app.route('/brazilhangout/mm2/adm', methods=['POST'])
def nova_goldy():
    nova_goldy = request.json
    goldys.append(nova_goldy)
    return jsonify(goldys)


@app.route('/brazilhangout/mm2/adm/<string:Name>', methods=['DELETE'])
def excluir_goldy(Name):
    for indice, goldy in enumerate(goldys):
        if goldy.get('Nome') == Name:
            del goldys[indice]
    return jsonify(goldys)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/swagger.json')
def swagger_json():
    swagger_data = {
        "swagger": "2.0",
        "info": {
            "version": "1.0",
            "title": "API MM2",
            "description": "Documentação da API"
        },
        "paths": {
            "/brazilhangout/mm2": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Retorna todos os goldys"
                        }
                    }
                }
            },
            "/brazilhangout/mm2/{Name}": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Retorna um goldy específico"
                        }
                    }
                },
                "put": {
                    "responses": {
                        "200": {
                            "description": "Edita um goldy"
                        }
                    }
                }
            },
            "/brazilhangout/mm2/adm": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "Cria um novo goldy"
                        }
                    }
                }
            },
        }
    }
    return jsonify(swagger_data)


if __name__ == '__main__':
    port = 80
    app.run(host='0.0.0.0', port=port)
