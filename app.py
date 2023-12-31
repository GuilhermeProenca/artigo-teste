import streamlit as st
import pandas as pd
import numpy as np
import math
import joblib

from PIL import Image

idioma_selecionado = st.radio("Selecione o idioma - Select the language", ["Português - Portuguese", "Inglês - English"], index=0, key="language")

# Dicionário para mapear os textos em português e inglês
textos = {
    "Português - Portuguese": {
        "titulo": "Projeto Detecção de Medidas Corporais Através de Imagens Para Cálculos de Avaliação Física",
        "objetivo": "Objetivo: Com os dados de altura, peso, idade, gênero e imagem de frente/lado,\nfornecer informações sobre uma pessoa.",
        "foto de frente": "Foto de frente",
        "foto de lado": "Foto de lado",
        "carregar": "Carregue a imagem",
        "genero": "Gênero",
        "seleciona genero": "Selecione o gênero",
        "menu genero": ["Feminino", "Masculino"],
        "idade": "Idade",
        "exemplo idade": "Exemplo: 35 anos",
        "altura": "Altura",
        "exemplo altura": "Exemplo: 170 cm",
        "peso": "Peso",
        "exemplo peso": "Exemplo: 80 kg",
        "fator": "Fator de atividade",
        "seleciona fator": "Selecione uma opção",
        "menu fator": ["Sedentário - Pouco ou nenhum exercício", \
                      "Levemente ativo - Exercício leve de 1 a 3 dias por semana",\
                      "Moderadamente ativo - Pratica esportes de 3 a 5 dias por semana",\
                      "Muito ativo - Exercícios intensos de 5 a 6 dias por semana",\
                      "Extremamente ativo - Exercícios intensos diariamente ou até 2 vezes por dia"]
    },
    "Inglês - English": {
        "titulo": "Body Measurement Detection Project Through Images for Physical Assessment Calculations",
        "objetivo": "Objective: With height, weight, age, gender, and front/side image data,\nprovide information about a person.",
        "foto de frente": "Front photo",
        "foto de lado": "Side photo",
        "carregar": "Upload the image",
        "genero": "Gender",
        "seleciona genero": "Select the genre",
        "menu genero": ["Female", "Male"],
        "idade": "Age",
        "exemplo idade": "Example: 35 years",
        "altura": "Height",
        "exemplo altura": "Example: 170 cm",
        "peso": "Weight",
        "exemplo peso": "Example: 80 kg",
        "fator": "Activity factor",
        "seleciona fator": "Select an option",
        "menu fator": ["Sedentary - Little or no exercise", \
                       "Lightly Active - Light exercise 1 to 3 days a week",\
                       "Moderately active - Plays sports 3 to 5 days a week",\
                       "Very active - Intense exercise 5 to 6 days a week",\
                       "Extremely active - Intense exercise daily or up to twice a day"]
    }
}

# Atualiza os textos com base na seleção de idioma
titulo = textos[idioma_selecionado]["titulo"]
objetivo = textos[idioma_selecionado]["objetivo"]
foto_de_frente = textos[idioma_selecionado]["foto de frente"]
foto_de_lado = textos[idioma_selecionado]["foto de lado"]
carregar = textos[idioma_selecionado]["carregar"]
genero = textos[idioma_selecionado]["genero"]
seleciona_genero = textos[idioma_selecionado]["seleciona genero"]
menu_genero = textos[idioma_selecionado]["menu genero"]
idade = textos[idioma_selecionado]["idade"]
exemplo_idade = textos[idioma_selecionado]["exemplo idade"]
altura = textos[idioma_selecionado]["altura"]
exemplo_altura = textos[idioma_selecionado]["exemplo altura"]
peso = textos[idioma_selecionado]["peso"]
exemplo_peso = textos[idioma_selecionado]["exemplo peso"]
fator = textos[idioma_selecionado]["fator"]
seleciona_fator = textos[idioma_selecionado]["seleciona fator"]
menu_fator = textos[idioma_selecionado]["menu fator"]

# Exibição dos textos no Streamlit
st.title(titulo)
st.text(objetivo)

st.write("---")

st.markdown(f"### {foto_de_frente}")
uploaded_file1 = st.file_uploader(carregar, key="file1")

st.markdown(f"### {foto_de_lado}")
uploaded_file2 = st.file_uploader(carregar, key="file2")

st.markdown(f"### {genero}")
gender = st.selectbox(seleciona_genero, menu_genero)

st.markdown(f"### {idade}")
age = st.number_input(exemplo_idade, format="%i", min_value=18)

st.markdown(f"### {altura}")
measure_height = st.number_input(exemplo_altura, format="%.2f", min_value=100.0, step=0.10)

st.markdown(f"### {peso}")
weight = st.number_input(exemplo_peso, format="%.2f", min_value=40.0, step=0.10)

st.markdown(f"### {fator}")
activity_factor = st.selectbox(seleciona_fator, menu_fator, index=0, key="factor")

neck_measure = 38.0
measure_waist = 75.0
hip_measure = 90.0

#st.write(activity_factor.index)

# Coversão de variáveis
if (gender == "Feminino" or gender == "Female"):
    gender = "F"
else:
    gender = "M"

if (activity_factor == "Sedentário - Pouco ou nenhum exercício"):
    activity_factor = 0
elif(activity_factor == "Levemente ativo - Exercício leve de 1 a 3 dias por semana"):
    activity_factor = 1
elif(activity_factor == "Moderadamente ativo - Pratica esportes de 3 a 5 dias por semana"):
    activity_factor = 2
elif(activity_factor == "Muito ativo - Exercícios intensos de 5 a 6 dias por semana"):
    activity_factor = 3
else:
    activity_factor = 4

# Funções dos cálculos
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
        status_imc = "Obesidade I"
    elif(result_imc <= 39.99):
        status_imc = "Obesidade II (severa)"
    else:
        status_imc = "Obesidade III (mórbida)"
        
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
    st.write("---")
    st.write(f"% de gordura corporal: {round(result_gcm, 2)}", help="TESTE 1, 2, 3...")

    st.write("Status GCm: ", gcm_status, help="AJUDA!!!!")

    st.write(f"Massa gorda: {round(fat_mass, 2)} kg ({round(perc_fat_mass, 2)}%)") 
    st.write(f"Massa magra: {round(lean_mass, 2)} kg ({round(perc_lean_mass, 2)}%)")

    st.write(f"Peso residual: {round(result_residual_weight, 2)} kg ({round(perc_residual_weight, 2)}%)")

    st.write(f"IMC (kg/m2): {round(result_imc, 2)}")

    st.write(f"Status IMC: {imc_status}")

    st.write(f"Taxa de metabolismo basal (k/cal): {round(result_tmb, 0)}")

    st.write(f"Consumo de caloria diário (k/cal): {round(result_daily_calorie, 0)}")
