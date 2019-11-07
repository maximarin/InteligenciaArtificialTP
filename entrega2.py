import itertools
import re
from datetime import datetime
from simpleai.search import (backtrack, CspProblem, LEAST_CONSTRAINING_VALUE,
                             min_conflicts, MOST_CONSTRAINED_VARIABLE)
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
horarios = [10,11,14, 15, 16, 17]

variables = ["Django Girls","Introducción a Python","Keynote Diversidad","Keynote Core Developer","APIs Rest",
    "Diseño Sistemas Accesibles","Unit Testing","Editores de Código","Música Python","Software, negocios, contabilidad y mucho más",
     "Análisis de Imágenes","Satélites Espaciales","Lib PyPI","Introducción a Pandas"]

aulas = {
    1: "Magna",
    2: "42",
    3: "Laboratorio"
        }

def generar_problema_entrega2():

    dominios = {variable: [] for variable in variables}
    restricciones = []

    for horario in horarios:
        # Taller de Django Girls: requiere de computadoras, y se espera una asistencia de 40 personas.#
        dominios["Django Girls"].append(("Laboratorio", horario))

        # Cómo hacer APIs rest en Django: charla normal sin requerimientos de tamaño de sala ni horarios, pero requiere de proyector.#
        dominios["APIs Rest"].append(("Magna",horario))
        dominios["APIs Rest"].append(("42",horario))

        # Diseño de sistemas accesibles: charla normal, y el orador no puede subir por escaleras por una dificulta de salud, por lo que no puede ser en la planta alta.
        dominios["Diseño Sistemas Accesibles"].append(("Magna", horario))
        dominios["Diseño Sistemas Accesibles"].append(("Laboratorio", horario))

        # Cómo hacer unit testing en Python: charla normal, requiere proyector.#
        dominios["Unit Testing"].append(("Magna", horario))
        dominios["Unit Testing"].append(("42", horario))

        # Python para análisis de imágenes: charla normal pero con una demo interactiva que requiere que el público esté bien visible, por lo que no puede darse en el laboratorio.#
        dominios["Análisis de Imágenes"].append(("Magna", horario))
        dominios["Análisis de Imágenes"].append(("42", horario))

        # Editores de código para Python: charla normal, requiere proyector y sistema de audio, ya que el disertante no puede esforzar demasiado su voz.#
        dominios["Editores de Código"].append(("Magna",horario))

        # Cómo hacer música con Python: charla normal, requiere proyector, pero el orador es alguien famoso por lo que se espera bastante asistencia, más de 60 personas.
        dominios["Música Python"].append(("Magna",horario))
        dominios["Música Python"].append(("42",horario))

        # Cómo publicar tu lib en PyPI: charla normal que requiere proyector.
        dominios["Lib PyPI"].append(("Magna", horario))
        dominios["Lib PyPI"].append(("42", horario))

        # Introducción a Pandas para procesamiento de datos: charla normal con proyector, que por requerimientos de conexión a internet solo puede darse en la planta alta (la planta baja no posee conexión)
        dominios["Introducción a Pandas"].append(("42", horario))

        # Taller de introducción a Python: también requiere de computadoras, y debería darse por la mañana, para que los
        if horario <= 11:
            dominios["Introducción a Python"].append(("Laboratorio",horario))

            # Cómo ser un buen vendedor de software, negocios, contabilidad y mucho más:
            dominios["Software, negocios, contabilidad y mucho más"].append(("Laboratorio", horario))
            dominios["Software, negocios, contabilidad y mucho más"].append(("42", horario))

        # Keynote sobre diversidad: al ser keynote se espera que la mayor parte de la conferencia asista, por lo que se
        if horario > 11:
            dominios["Keynote Diversidad"].append(("Magna",horario))
            dominios["Keynote Core Developer"].append(("Magna",horario))

            # Python para satélites espaciales: charla normal que requiere proyector, y darse por la tarde, porque su orador no funciona bien de mañana.#
            dominios["Satélites Espaciales"].append(("Magna",horario))
            dominios["Satélites Espaciales"].append(("42",horario))


    def Keynote_SinOtrasCharlas(vars,vals):
        val1,val2 = vals
        valor = val1[1]
        return val1[1] != val2[1] #horarios diferentes

    def TodasCharlasDiferentes(vars, vals):  # Que no haya charlas en una misma aula y en un mismo horario.
         val1, val2 = vals
         return not val1 == val2

#Los keynote no pueden tener otras charlas en simultaneo. Son unicas en su horario.
    for var in variables:
        if var != "Keynote Diversidad":
            restricciones.append(((variables[2],var),Keynote_SinOtrasCharlas))
        if var != "Keynote Core Developer":
            restricciones.append(((variables[3],var),Keynote_SinOtrasCharlas))

    #Se generan combinaciones de dos variables, para saber si no hay charlas en el mismo lugar y misma hora.
    for vars in itertools.combinations(variables,2):
        restricciones.append(((vars[0],vars[1]),TodasCharlasDiferentes))


    return CspProblem(variables, dominios, restricciones)

def resolver(metodo_busqueda, iteraciones):
    problema = generar_problema_entrega2()

    if metodo_busqueda == "backtrack":
        resultado = backtrack(problema)

    elif metodo_busqueda == "min_conflicts":
        resultado = min_conflicts(problema, iterations_limit=iteraciones)

    return resultado


if __name__ == '__main__':
    metodo = "backtrack"
    iteraciones = None
    #viewer = BaseViewer()

    #metodo = "min_conflicts"
    #iteraciones = 100

    inicio = datetime.now()
    result = resolver(metodo, iteraciones)
    print("tiempo {}".format((datetime.now() - inicio).total_seconds()))
    print(result)
    print(repr(result))


    #problema = generar_problema_entrega2()
    #conflictos = _find_conflicts(problema, resultado)
    #print("Numero de conflictos en la solucion: {}".format(len(conflictos)))
