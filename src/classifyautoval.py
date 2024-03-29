from latexifier import latexify

from .auxiliar.externalFunctions import re, autovalores, autovectores, det_matriz
from .comprobaciones.comprobaciones import comprobarCoeficientes, esReal, matrizDiagonalizable
from .resp.definirPasos import getPasoMatriz, getPaso, getPasoAutovalores, getPasoAutovaloresComplejos
from .resp.obj.Paso import Paso
from .resp.obj.Pasos import Pasos


def c_p_a_real_distinto(aVect) -> Paso:
    """
    Clasificación del punto de equilibrio cuando los autovalores son reales y distintos
    :param aVect: autovalores, multiplicidad y autovectores
    :return: paso
    """
    aVal1 = aVect[0][0]
    aVal2 = aVect[1][0]
    if (aVal1 < 0 < aVal2) or (aVal1 > 0 > aVal2):
        signo, tipo = "de diferente signo", "punto de silla"
    elif aVal1 < 0 and aVal2 < 0:
        signo, tipo = "negativos", "punto estable"
    else:
        signo, tipo = "positivos", "punto inestable"
    pasos = Paso('', '', "Como los dos autovalores son reales y {}, el punto $(0,0)$ es un {}.".format(signo, tipo))
    return pasos


def c_p_a_complejo(aVect) -> list[Paso]:
    """
    Clasificación del punto de equilibrio cuando los autovalores son complejos (y distintos)
    :param aVect: autovalores, multiplicidad y autovectores
    :return: paso
    """
    aVal = aVect[0][0]
    alpha = re(aVal)
    signo = "menor que" if alpha < 0 else ("mayor que" if alpha > 0 else "igual a")
    tipo = "foco estable" if alpha < 0 else ("foco inestable" if alpha > 0 else "centro estable")
    paso = 'Re(lambda_1)=Re(lambda_2)={}'.format(latexify(alpha))
    pasoLatex = '{}(\\lambda_1)={}(\\lambda_2) = {}'.format('\\operatorname{Re}', '\\operatorname{Re}', latexify(alpha))
    pasos = [Paso(paso, pasoLatex, "Como los autovalores son complejos nos fijamos en la parte real"),
             Paso('', '', "Como la parte real es {} cero, el punto $(0,0)$ es un {}.".format(signo, tipo))]

    return pasos


def c_p_a_doble_diag():
    """
    Clasificación del punto de equilibrio cuando los autovalores iguales y la matriz diagonalizable
    :param aVal: autovalores, multiplicidad y autovectores
    :return: paso
    """
    pasos = Paso('', '',
                 "Como el autovalor $\\lambda$ es doble y la matriz $A$ es diagonalizable, el punto $(0,0)$ es un punto estelar.")
    return pasos


def c_p_a_doble_no_diag(aVal):
    """
    Clasificación del punto de equilibrio cuando los autovalores son iguales y la matriz no es diagonalizable
    :param aVal: autovalores, multiplicidad y autovectores
    :return: paso
    """
    signo = "positivo" if aVal > 0 else "negativo"
    tipo = "inestable" if aVal > 0 else "estable"
    pasos = Paso('','',
                    "Como el autovalor $\\lambda$ es doble, la matriz $A$ no es diagonalizable y el autovalor \\lambda={} es {}, el punto $(0,0)$ es un nodo impropio {}.".format(
                        latexify(aVal), signo, tipo))
    return pasos


'''-----------------------------------------------------'''


# Los autovectores pintan los ejes
def clasificar_punto_autoval(a, b, c, d):
    """
    Indica el tipo de punto de equilibrio que es el origen en función de cómo es el autovalor
    :param a: coeficiente 1ª fila 1ª columna
    :param b: coeficiente 1ª fila 2ª columna
    :param c: coeficiente 2ª fila 1ª columna
    :param d: coeficiente 2ª fila 2ª columna
    :return: JSON
    """
    A = comprobarCoeficientes(a, b, c, d)

    det = det_matriz(A)
    pasos = [getPasoMatriz(A, "Esta es la matriz de coeficientes asociado al sistema")]

    paso = 'det={}'.format(latexify(det))
    pasoLatex = '\\det(A)={}'.format(latexify(det))
    pasos.append(Paso(paso, pasoLatex,
                      "Como el determinante es ${}\\neq 0$, el único punto de equilibrio es el origen $(0,0)$".format(
                          latexify(det))))
    aVal = autovalores(A)
    aVect = autovectores(A)
    aVal1 = next(iter(aVal))  # primer autovalor
    keys = list(aVal.keys())
    if esReal(aVal1):  # real
        pasos.append(getPasoAutovalores(keys,
                                        "Hallamos los autovalores asociados al sistema"))
        if aVal[aVal1] == 1:  # autovalor simple
            pasos.append(c_p_a_real_distinto(aVect))
        else:  # autovalor doble
            if matrizDiagonalizable(A):  # autovalor doble diagonalizable
                pasos.append(c_p_a_doble_diag())
            else:  # autovalor doble, no diagonalizable
                pasos.append(c_p_a_doble_no_diag(aVal1))
    else:  # complejo
        pasos.append(getPasoAutovaloresComplejos(keys,
                                                 "Hallamos los autovalores asociados al sistema"))
        pasos = pasos + c_p_a_complejo(aVect)

    return Pasos(pasos).toJson()
