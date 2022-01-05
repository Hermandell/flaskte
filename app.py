from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from functools import wraps
#clases
from Server import MyServer

app = Flask(__name__)
# Esto es para que los objetos se ordenen
app.config['JSON_SORT_KEYS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
cors = CORS(app, resources={r"/user": {"origins": "http://127.0.0.1:5000"}})
#declarar la clase
myserver=MyServer()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if token !=myserver.token:
            return jsonify({'message': 'Token is missing !!'}), 401
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        return f(*args, **kwargs)
    return decorated


@cross_origin(origin='127.0.0.1',headers=['Content- Type','Authorization'])
@app.route('/user', methods=["GET"])
@token_required
def user():
    return myserver.obtenerData()


@app.route('/login', methods=["POST"])
def login():
    return myserver.login()



if __name__ == '__main__':
    app.run()


#-------------Programacion estrcturada-------------------

# abre el schema
# with open('schema.json') as f:
#     schema = load(f)
#
# app = Flask(__name__)
# # Esto es para que los objetos se ordenen
# app.config['JSON_SORT_KEYS'] = False
# app.config['CORS_HEADERS'] = 'Content-Type'
# CORS(app)
# cors = CORS(app, resources={r"/user": {"origins": "http://localhost:port"}})
#
#
# @app.route('/user', methods=["POST"])
# @cross_origin(origin='127.0.0.1',headers=['Content- Type','Authorization'])
# def user():
#
#     LoginUrl = ('https://itnleon.mindbox.app/login/autoriza-alumno')
#     Profile = ('https://itnleon.mindbox.app/alumnos/datos/generales')
#     #validar el json que tenga info
#     try:
#          data = json.loads(request.data)
#     except JSONDecodeError:
#          return jsonify(({"response": "Error en credenciales"})),500
#     else:
#         validar = Draft7Validator(schema)
#         errores = list(validar.iter_errors(data))
#         print(errores)
#         #aqui va el if not
#         ncontrol = data["ncontrol"]
#         password = data["password"]
#         print(type(data))
#         r = requests.get(LoginUrl)
#         bs = BeautifulSoup(r.text, 'html.parser')
#         csrf_token = bs.find('input', attrs={'name': '_token'})['value']
#         credentials = {
#             "_token": csrf_token,
#             "ncontrol": ncontrol,
#             "password": password
#         }
#         if (not errores):
#             if ((len(ncontrol) and len(password)) == 0):
#                 return jsonify({"response": "palabra vacia"})
#             # --------------------------------
#             s = requests.session()
#             s.post(LoginUrl, cookies=r.cookies, data=credentials)
#             profile = s.get(Profile)
#             print(profile.url)
#             if profile.status_code == 200:
#                 if profile.url != Profile:
#                     return ({"response": "Error de Usuario"})
#                 ProfileHtml = BeautifulSoup(profile.text, "html.parser")
#                 images = ProfileHtml.find('check-img')['image']
#                 ul_tags = ProfileHtml.find('ul', {'class': 'simple'})
#                 li_tags = ul_tags.find_all('li')
#                 # print(li_tags)
#                 info = list()
#                 for i in li_tags:
#                     datos_personales = (i.find('span').text.strip())
#                     info.append(datos_personales)
#
#                 return jsonify({
#                     "imageProfile": images,
#                     "nombre": info[0],
#                     "apellidoPaterno": info[1],
#                     "apellidoMaterno": info[2],
#                     "curp": info[3],
#                     "fechaNacimiento": info[4],
#                     "lugarNacimiento": info[5],
#                     "sexo": info[6]
#                 })
#             return ({"response": "Falle"})
#         else:
#             return jsonify({"Response": "Error en el response, revise usar strings"})
