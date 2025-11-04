class EstudianteEjemplo:

    def __init__(self,identificacion,nombre,edad):
        self.identificacion = identificacion
        self.nombre = nombre
        self.edad = edad

    def to_json(self):
        return self.__dict__
