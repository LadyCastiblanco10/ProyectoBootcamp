
from flask import Flask,jsonify,request
from Estudiante import EstudianteEjemplo
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
estudiantes = []
estudiantes2 = []


print(estudiantes)
estudianteNuevo = EstudianteEjemplo(1,"Jorge",31)
estudianteNuevo2 = EstudianteEjemplo(2,"Alejandra",30)
estudianteNuevo3 = EstudianteEjemplo(3,"Anna",31)

estudiantes.append(estudianteNuevo)
estudiantes.append(estudianteNuevo2)
estudiantes.append(estudianteNuevo3)

estudiantes2.append(estudianteNuevo.to_json())
estudiantes2.append(estudianteNuevo2.to_json())
estudiantes2.append(estudianteNuevo3.to_json())

for estudiante in estudiantes:
    print("El estudiante es: ",estudiante.identificacion,"-",estudiante.nombre,"-",estudiante.edad)

print(estudiantes2)

@app.route("/listaEstudiantes",methods=['GET'])
def listarEstudiantes():
    return jsonify(estudiantes2)

if __name__ == '__main__':
    app.run(debug=True)