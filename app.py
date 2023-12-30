import streamlit as st
import pandas as pd
import numpy as np
import math
import joblib

from PIL import Image

st.title("Projeto Detecção de Medidas Corporais Através de Imagens Para Cálculos de Avaliação Física")
st.text("Objetivo: Dada informações de altura, peso, idade, gênero e imagem de frente/lado, fornecer informações sobre uma pessoa.")

gender = st.selectbox("Gênero:", ("Feminino", "Masculino"))

if (gender == "Feminino"):
    gender = "F"
else:
    gender = "M"

age = st.number_input("Idade (Exemplo: 35 anos)", format="%i", min_value=1)

measure_height = st.number_input("Altura (Exemplo: 170 cm)", format="%f", min_value=1)

weight = st.number_input("Peso (Exemplo: 80 kg)", format="%f", min_value=1)

#activity_factor = st.selectbox(
#                                "Fator de atividade",
#                                ("Sedentário - Pouco ou nenhum exercício", \
#                                 "Levemente ativo - Exercício leve de 1 a 3 dias por semana",\
#                                 "Moderadamente ativo - Pratica esportes de 3 a 5 dias por semana",\
#                                 "Muito ativo - Exercícios intensos de 5 a 6 dias por semana",\
#                                 "Extremamente ativo - Exercícios intensos diariamente ou até 2 vezes por dia"),
#                                index=None,
#                                placeholder="Selecione o fator de atividade",
#                              )

activity_factor = 0

neck_measure = 38.0
measure_waist = 75.0
hip_measure = 90.0

def calc_bioimpedance(gender, measure_height, neck_measure, measure_waist, hip_measure):

    if (gender.upper() == "F"):
        gcm = (495 / (1.296 - 0.350 * math.log10(hip_measure + measure_waist - neck_measure) + 0.221 * \
                      math.log10(measure_height))) - 450
    else:
        gcm = (495 / (1.033 - 0.191 * math.log10(measure_waist - neck_measure) + 0.155 * \
                      math.log10(measure_height))) - 450
    
    return gcm


def calc_imc(weight, measure_height):
    
    imc = ((weight) / ((measure_height / 100) ** 2))
    
    return imc


def calc_body_composition(result_gcm, weight):
    
    fat_mass = (result_gcm / 100) * weight
    
    lean_mass = weight - fat_mass
    
    perc_fat_mass = (fat_mass * 100) / (fat_mass + lean_mass)
    
    perc_lean_mass = (lean_mass * 100) / (fat_mass + lean_mass)
    
    return fat_mass, lean_mass, perc_fat_mass, perc_lean_mass


def calc_tmb(weight, measure_height, age):
    
    if (gender.upper() == "F"):
        tmb = 655 + (9.6 * weight) + (1.8 * measure_height) - (4.7 * age)
    else:
        tmb = 66 + (13.7 * weight) + (5 * measure_height) - (6.8 * age)
        
    return tmb


def calc_daily_calorie(result_tmb, activity_factor):
    
    if(activity_factor == 0):
        daily_calorie = result_tmb * 1.2     
    elif(activity_factor == 1):
        daily_calorie = result_tmb * 1.375    
    elif(activity_factor == 2):
        daily_calorie = result_tmb * 1.55  
    elif(activity_factor == 3):
        daily_calorie = result_tmb * 1.725
    else:
        daily_calorie = result_tmb * 1.9
        
    return daily_calorie


def calc_residual_weight(weight):
    
    if (gender.upper() == "F"):
        residual_weight = weight * 0.208
    else:
        residual_weight = weight * 0.241
        
    perc_residual_weight = (residual_weight * 100) / weight
        
    return residual_weight, perc_residual_weight


def status_gcm(result_gcm, gender, age):
    
    if (gender.upper() == "F"):
        if((age == 18 and result_gcm <= 16.0) or \
           (age == 19 and result_gcm <= 18.0) or \
           (age <= 39 and result_gcm <= 20.0) or \
           (age <= 59 and result_gcm <= 22.0) or \
           (age >= 60 and result_gcm <= 23.0)):
            status_gcm = "Magreza"
        elif((age == 18 and result_gcm <= 30.0) or \
            (age == 19 and result_gcm <= 31.0) or \
            (age <= 39 and result_gcm <= 32.0) or \
            (age <= 59 and result_gcm <= 33.0) or \
            (age >= 60 and result_gcm <= 35.0)):
            status_gcm = "Normal"
        elif((age == 18 and result_gcm <= 35.0) or \
            (age == 19 and result_gcm <= 36.0) or \
            (age <= 39 and result_gcm <= 38.0) or \
            (age <= 59 and result_gcm <= 39.0) or \
            (age >= 60 and result_gcm <= 41.0)):
            status_gcm = "Sobrepeso"
        else:
            status_gcm = "Obesidade"
    else:
        if((age == 18 and result_gcm <= 9.0) or \
           (age == 19 and result_gcm <= 8.0) or \
           (age <= 39 and result_gcm <= 7.0) or \
           (age <= 59 and result_gcm <= 10.0) or \
           (age >= 60 and result_gcm <= 12.0)):
            status_gcm = "Magreza"
        elif((age == 18 and result_gcm <= 19.0) or \
            (age == 19 and result_gcm <= 19.0) or \
            (age <= 39 and result_gcm <= 19.0) or \
            (age <= 59 and result_gcm <= 21.0) or \
            (age >= 60 and result_gcm <= 24.0)):
            status_gcm = "Normal"
        elif((age == 18 and result_gcm <= 23.0) or \
            (age == 19 and result_gcm <= 23.0) or \
            (age <= 39 and result_gcm <= 24.0) or \
            (age <= 59 and result_gcm <= 27.0) or \
            (age >= 60 and result_gcm <= 29.0)):
            status_gcm = "Sobrepeso"
        else:
            status_gcm = "Obesidade"
            
    return status_gcm


def status_imc(result_imc):
    
    if(result_imc < 17):
        status_imc = "Muito abaixo do peso"
    elif(result_imc <= 18.49):
        status_imc = "Abaixo do peso"
    elif(result_imc <= 24.99):
        status_imc = "Peso normal"
    elif(result_imc <= 29.99):
        status_imc = "Acima do peso"
    elif(result_imc <= 34.99):
        status_imc = "Obesage I"
    elif(result_imc <= 39.99):
        status_imc = "Obesage II (severa)"
    else:
        status_imc = "Obesage III (mórbida)"
        
    return status_imc


result_gcm = calc_bioimpedance(gender, measure_height, neck_measure, measure_waist, hip_measure)

result_imc = calc_imc(weight, measure_height)

fat_mass, lean_mass, perc_fat_mass, perc_lean_mass = calc_body_composition(result_gcm, weight)

result_tmb = calc_tmb(weight, measure_height, age)

result_daily_calorie = calc_daily_calorie(result_tmb, activity_factor)

result_residual_weight, perc_residual_weight = calc_residual_weight(weight)
 
gcm_status = status_gcm(result_gcm, gender, age)

imc_status = status_imc(result_imc)

if st.button("Resultado"):
    st.write(f"% de gordura corporal: {round(result_gcm, 2)}")

    st.write("Status GCm: ", gcm_status)

    st.write(f"Massa gorda: {round(fat_mass, 2)} kg ({round(perc_fat_mass, 2)}%)") 
    st.write(f"Massa magra: {round(lean_mass, 2)} kg ({round(perc_lean_mass, 2)}%)")

    st.write(f"Peso residual: {result_residual_weight} kg ({round(perc_residual_weight, 2)}%)")

    st.write(f"IMC (kg/m2): {round(result_imc, 2)}")

    st.write(f"Status IMC: {imc_status}")

    st.write(f"Taxa de metabolismo basal (k/cal): {round(result_tmb, 0)}")

    st.write(f"Consumo de caloria diário (k/cal): {round(result_daily_calorie, 0)})
