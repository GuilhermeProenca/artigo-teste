import streamlit as st
import pandas as pd
import numpy as np
import math
import joblib

from PIL import Image

selected_language = st.radio("Selecione o idioma - Select the language", ["Português - Portuguese", "Inglês - English"], index=0, key="language")

# Dicionário para mapear os textos em português e inglês
texts = {
    "Português - Portuguese": {
        "title": "Projeto Detecção de Medidas Corporais Através de Imagens Para Cálculos de Avaliação Física",
        "objective": "Objetivo: Com os dados de altura, peso, idade, gênero e imagem de frente/lado,\nfornecer informações sobre uma pessoa.",
        "front_photo": "Foto de frente",
        "side_photo": "Foto de lado",
        "load": "Carregue a imagem",
        "gender": "Gênero",
        "gender_select": "Selecione o gênero",
        "gender_menu": ["Feminino", "Masculino"],
        "age": "Idade",
        "age_example": "Exemplo: 35 anos",
        "height": "Altura",
        "height_example": "Exemplo: 170 cm",
        "weight": "Peso",
        "weight_example": "Exemplo: 80 kg",
        "factor": "Fator de atividade",
        "factor_select": "Selecione uma opção",
        "factor_menu": ["Sedentário - Pouco ou nenhum exercício",\
                        "Levemente ativo - Exercício leve de 1 a 3 dias por semana",\
                        "Moderadamente ativo - Pratica esportes de 3 a 5 dias por semana",\
                        "Muito ativo - Exercícios intensos de 5 a 6 dias por semana",\
                        "Extremamente ativo - Exercícios intensos diariamente ou até 2 vezes por dia"],
        "status_gcm": ["Magreza",\
                       "Normal",\
                       "Sobrepeso",\
                       "Obesidade"],
        "status_imc": ["Muito abaixo do peso",\
                       "Abaixo do peso",\
                       "Peso normal",\
                       "Acima do peso",\
                       "Obesidade I",\
                       "Obesidade II (severa)",\
                       "Obesidade III (mórbida)"],
        "result_button": "Resultado"
    },
    "Inglês - English": {
        "title": "Body Measurement Detection Project Through Images for Physical Assessment Calculations",
        "objective": "Objective: With height, weight, age, gender, and front/side image data,\nprovide information about a person.",
        "front_photo": "Front photo",
        "side_photo": "Side photo",
        "load": "Upload the image",
        "gender": "Gender",
        "gender_select": "Select the genre",
        "gender_menu": ["Female", "Male"],
        "age": "Age",
        "age_example": "Example: 35 years",
        "height": "Height",
        "height_example": "Example: 170 cm",
        "weight": "Weight",
        "weight_example": "Example: 80 kg",
        "factor": "Activity factor",
        "factor_select": "Select an option",
        "factor_menu": ["Sedentary - Little or no exercise", \
                        "Lightly Active - Light exercise 1 to 3 days a week",\
                        "Moderately active - Plays sports 3 to 5 days a week",\
                        "Very active - Intense exercise 5 to 6 days a week",\
                        "Extremely active - Intense exercise daily or up to twice a day"],
        "status_gcm": ["Thinness",\
                       "Normal",\
                       "Overweight",\
                       "Obesity"],
        "status_imc": ["Very underweight",\
                       "Under weight",\
                       "Normal weight",\
                       "Overweight",\
                       "Obesity I",\
                       "Obesity II (severe)",\
                       "Obesity III (morbid)"],
        "result_button": "Result"
    }
}

# Atualiza os textos com base na seleção de idioma
title = texts[selected_language]["title"]
objective = texts[selected_language]["objective"]
front_photo = texts[selected_language]["front_photo"]
side_photo = texts[selected_language]["side_photo"]
load = texts[selected_language]["load"]
gender_text = texts[selected_language]["gender"]
gender_select = texts[selected_language]["gender_select"]
gender_menu = texts[selected_language]["gender_menu"]
age_text = texts[selected_language]["age"]
age_example = texts[selected_language]["age_example"]
height_text = texts[selected_language]["height"]
height_example = texts[selected_language]["height_example"]
weight_text = texts[selected_language]["weight"]
weight_example = texts[selected_language]["weight_example"]
factor_text = texts[selected_language]["factor"]
factor_select = texts[selected_language]["factor_select"]
factor_menu = texts[selected_language]["factor_menu"]

# Exibição dos textos iniciais no Streamlit
st.title(title)
st.text(objective)

st.write("---")

st.markdown(f"### {front_photo}")
uploaded_file1 = st.file_uploader(load, key="file1")

st.markdown(f"### {side_photo}")
uploaded_file2 = st.file_uploader(load, key="file2")

st.markdown(f"### {gender_text}")
gender = st.selectbox(gender_select, gender_menu)

st.markdown(f"### {age_text}")
age = st.number_input(age_example, format="%i", min_value=18)

st.markdown(f"### {height_text}")
measure_height = st.number_input(height_example, format="%.2f", min_value=100.0, step=0.10)

st.markdown(f"### {weight_text}")
weight = st.number_input(weight_example, format="%.2f", min_value=40.0, step=0.10)

st.markdown(f"### {factor_text}")
activity_factor = st.selectbox(factor_select, factor_menu, index=0, key="factor")

measure_neck = 38.0
measure_waist = 75.0
measure_hip = 90.0


# Coversão de variáveis
if (gender == "Feminino" or gender == "Female"):
    gender = "F"
else:
    gender = "M"


# Funções dos cálculos
def calc_bioimpedance(gender, measure_height, measure_neck, measure_waist, measure_hip):

    if (gender.upper() == "F"):
        gcm = (495 / (1.296 - 0.350 * math.log10(measure_hip + measure_waist - measure_neck) + 0.221 * \
                      math.log10(measure_height))) - 450
    else:
        gcm = (495 / (1.033 - 0.191 * math.log10(measure_waist - measure_neck) + 0.155 * \
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
    
    if (activity_factor == "Sedentário - Pouco ou nenhum exercício" or \
        activity_factor == "Sedentary - Little or no exercise"):
        daily_calorie = result_tmb * 1.2     
    elif (activity_factor == "Levemente ativo - Exercício leve de 1 a 3 dias por semana" or \
          activity_factor == "Lightly Active - Light exercise 1 to 3 days a week"):
        daily_calorie = result_tmb * 1.375    
    elif (activity_factor == "Moderadamente ativo - Pratica esportes de 3 a 5 dias por semana" or \
          activity_factor == "Moderately active - Plays sports 3 to 5 days a week"):
        daily_calorie = result_tmb * 1.55  
    elif (activity_factor == "Muito ativo - Exercícios intensos de 5 a 6 dias por semana" or \
          activity_factor =="Very active - Intense exercise 5 to 6 days a week"):
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
            status_gcm = texts[selected_language]["status_gcm"][0]
        elif((age == 18 and result_gcm <= 30.0) or \
            (age == 19 and result_gcm <= 31.0) or \
            (age <= 39 and result_gcm <= 32.0) or \
            (age <= 59 and result_gcm <= 33.0) or \
            (age >= 60 and result_gcm <= 35.0)):
            status_gcm = texts[selected_language]["status_gcm"][1]
        elif((age == 18 and result_gcm <= 35.0) or \
            (age == 19 and result_gcm <= 36.0) or \
            (age <= 39 and result_gcm <= 38.0) or \
            (age <= 59 and result_gcm <= 39.0) or \
            (age >= 60 and result_gcm <= 41.0)):
            status_gcm = texts[selected_language]["status_gcm"][2]
        else:
            status_gcm = texts[selected_language]["status_gcm"][3]
    else:
        if((age == 18 and result_gcm <= 9.0) or \
           (age == 19 and result_gcm <= 8.0) or \
           (age <= 39 and result_gcm <= 7.0) or \
           (age <= 59 and result_gcm <= 10.0) or \
           (age >= 60 and result_gcm <= 12.0)):
            status_gcm = texts[selected_language]["status_gcm"][0]
        elif((age == 18 and result_gcm <= 19.0) or \
            (age == 19 and result_gcm <= 19.0) or \
            (age <= 39 and result_gcm <= 19.0) or \
            (age <= 59 and result_gcm <= 21.0) or \
            (age >= 60 and result_gcm <= 24.0)):
            status_gcm = texts[selected_language]["status_gcm"][1]
        elif((age == 18 and result_gcm <= 23.0) or \
            (age == 19 and result_gcm <= 23.0) or \
            (age <= 39 and result_gcm <= 24.0) or \
            (age <= 59 and result_gcm <= 27.0) or \
            (age >= 60 and result_gcm <= 29.0)):
            status_gcm = texts[selected_language]["status_gcm"][2]
        else:
            status_gcm = texts[selected_language]["status_gcm"][3]
            
    return status_gcm


def status_imc(result_imc):
    
    if(result_imc < 17):
        status_imc = texts[selected_language]["status_imc"][0]
    elif(result_imc <= 18.49):
        status_imc = texts[selected_language]["status_imc"][1]
    elif(result_imc <= 24.99):
        status_imc = texts[selected_language]["status_imc"][2]
    elif(result_imc <= 29.99):
        status_imc = texts[selected_language]["status_imc"][3]
    elif(result_imc <= 34.99):
        status_imc = texts[selected_language]["status_imc"][4]
    elif(result_imc <= 39.99):
        status_imc = texts[selected_language]["status_imc"][5]
    else:
        status_imc = texts[selected_language]["status_imc"][6]
        
    return status_imc


result_gcm = calc_bioimpedance(gender, measure_height, measure_neck, measure_waist, measure_hip)

result_imc = calc_imc(weight, measure_height)

fat_mass, lean_mass, perc_fat_mass, perc_lean_mass = calc_body_composition(result_gcm, weight)

result_tmb = calc_tmb(weight, measure_height, age)

result_daily_calorie = calc_daily_calorie(result_tmb, activity_factor)

result_residual_weight, perc_residual_weight = calc_residual_weight(weight)
 
gcm_status = status_gcm(result_gcm, gender, age)

imc_status = status_imc(result_imc)

if st.button(texts[selected_language]["result_button"]):
    st.write("---")

    with st.sidebar:
        st.markdown("### Informações Adicionais")
        st.write("Se precisar de mais detalhes ou tiver dúvidas, entre em contato.")


    st.write(f"% de gordura corporal: {round(result_gcm, 2)}")

    st.write("Status GCm: ", gcm_status)

    st.write(f"Massa gorda: {round(fat_mass, 2)} kg ({round(perc_fat_mass, 2)}%)") 
    st.write(f"Massa magra: {round(lean_mass, 2)} kg ({round(perc_lean_mass, 2)}%)")

    st.write(f"Peso residual: {round(result_residual_weight, 2)} kg ({round(perc_residual_weight, 2)}%)")

    st.write(f"IMC (kg/m2): {round(result_imc, 2)}")

    st.write("kg/m", end="")

    # Exibir "^2" como uma potência com tamanho reduzido
    st.write("Texto com expoente: $x^2$")

    st.write(f"Status IMC: {imc_status}")

    st.write(f"Taxa de metabolismo basal (k/cal): {round(result_tmb, 0)}")

    st.write(f"Consumo de caloria diário (k/cal): {round(result_daily_calorie, 0)}")
