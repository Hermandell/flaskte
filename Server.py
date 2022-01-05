from flask import jsonify, request
from bs4 import BeautifulSoup
import json
import requests
from jsonschema import Draft7Validator
from json import load, JSONDecodeError

with open('schema.json') as f:
    schema = load(f)

class MyServer:
    def __init__(self):
        self.LoginUrl = ('https://itnleon.mindbox.app/login/autoriza-alumno')
        self.Profile = ('https://itnleon.mindbox.app/alumnos/datos/generales')
        self.sr = requests
        self.sesion = self.sr.session()
        self.token=None

    def login(self):
        # validar el json que tenga info
        try:
            data = json.loads(request.data)
        except JSONDecodeError:
            return jsonify(({"response": "Error en credenciales"})), 500
        else:
            validar = Draft7Validator(schema)
            errores = list(validar.iter_errors(data))
            print(errores)
            # aqui va el if not
            ncontrol = data["ncontrol"]
            password = data["password"]
            print(type(data))
            r = requests.get(self.LoginUrl)
            bs = BeautifulSoup(r.text, 'html.parser')
            csrf_token = bs.find('input', attrs={'name': '_token'})['value']
            #print(csrf_token)
            self.token=csrf_token
            credentials = {
                "_token": csrf_token,
                "ncontrol": ncontrol,
                "password": password
            }
            if (not errores):
                if ((len(ncontrol) and len(password)) == 0):
                    return jsonify({"response": "palabra vacia"})
                # --------------------------------
                s = self.sesion
                s.post(self.LoginUrl, cookies=r.cookies, data=credentials)
            else:
                return jsonify({"Response": "Error en el response, revise usar strings"})
        return jsonify({"token": csrf_token})


    def obtenerData(self):
        self.login()
        s = self.sesion
        profile = s.get(self.Profile)
        print(profile.url)
        if profile.status_code == 200:
            if profile.url != self.Profile:
                return ({"response": "Error de Usuario"})
            ProfileHtml = BeautifulSoup(profile.text, "html.parser")
            images = ProfileHtml.find('check-img')['image']
            ul_tags = ProfileHtml.find('ul', {'class': 'simple'})
            li_tags = ul_tags.find_all('li')
            # print(li_tags)
            info = list()
            for i in li_tags:
                datos_personales = (i.find('span').text.strip())
                info.append(datos_personales)

            return jsonify({
                "imageProfile": images,
                "nombre": info[0],
                "apellidoPaterno": info[1],
                "apellidoMaterno": info[2],
                "curp": info[3],
                "fechaNacimiento": info[4],
                "lugarNacimiento": info[5],
                "sexo": info[6]
            })
        return ({"response": "Falle"})