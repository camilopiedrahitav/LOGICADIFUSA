

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
print("ok import")


concentracion = ctrl.Antecedent(np.arange(0, 11, 1), 'concentracion')
cansancio = ctrl.Antecedent(np.arange(0, 11, 1), 'cansancio')
estudio = ctrl.Consequent(np.arange(0, 6, 0.5), 'estudio')
print("Ok variables")


concentracion['baja'] = fuzz.trapmf(concentracion.universe, [0, 0, 2, 4])
concentracion['media'] = fuzz.trimf(concentracion.universe, [3, 5, 7])
concentracion['alta'] = fuzz.trapmf(concentracion.universe, [6, 8, 10, 10])


cansancio['bajo'] = fuzz.trapmf(cansancio.universe, [0, 0, 2, 4])
cansancio['medio'] = fuzz.trimf(cansancio.universe, [3, 5, 7])
cansancio['alto'] = fuzz.trapmf(cansancio.universe, [6, 8, 10, 10])


estudio['muy_poco'] = fuzz.trapmf(estudio.universe, [0, 0, 1, 2])
estudio['moderado'] = fuzz.trimf(estudio.universe, [1.5, 3, 4.5])
estudio['mucho'] = fuzz.trapmf(estudio.universe, [4, 5, 6, 6])
print("ok configuración")


concentracion.view()
cansancio.view()
estudio.view()

rule1 = ctrl.Rule(concentracion['alta'] & cansancio['bajo'], estudio['mucho'])
rule2 = ctrl.Rule(concentracion['media'] & cansancio['medio'], estudio['moderado'])
rule3 = ctrl.Rule(concentracion['baja'] | cansancio['alto'], estudio['muy_poco'])
rule4 = ctrl.Rule(concentracion['alta'] & cansancio['medio'], estudio['moderado'])
rule5 = ctrl.Rule(concentracion['media'] & cansancio['bajo'], estudio['mucho'])
print("ok reglas")


estudio_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
simulador = ctrl.ControlSystemSimulation(estudio_ctrl)

for regla in estudio_ctrl.rules:
    print(regla.antecedent, " --> ", regla.consequent)

valorConcentracion = np.double(input("Ingrese su nivel de concentración actual (0-10): "))
valorCansancio = np.double(input("Ingrese su nivel de cansancio actual (0-10): "))

simulador.input['concentracion'] = valorConcentracion
simulador.input['cansancio'] = valorCansancio
simulador.compute()

resultado = simulador.output['estudio']
print("Horas de estudio recomendadas:", round(resultado, 2))

estudio.view(sim=simulador)
plt.show()
