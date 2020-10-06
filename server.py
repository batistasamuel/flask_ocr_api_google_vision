from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from google.cloud import vision
from google.oauth2 import service_account
from numpy import asarray
from pdf2image import convert_from_path
import io
import re
import pandas as pd
import json
import os
import db as d

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Rota que apresenta os botões de envio da conta
@app.route('/flora/conta/', methods=['GET'])
def conta_upload_file():
    return render_template('upload.html')

# Rota para envio da conta
@app.route('/flora/conta/upload', methods=['POST'])
def conta_upload():

    # Credenciais service account google para uso da API
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
        r'/home/user/Documentos/path_to_your_key/googleKey.json'
    
    client = vision.ImageAnnotatorClient()
    
    # Caminho para a pasta local
    target = os.path.join(APP_ROOT, 'conta-images/')
    
    # Cria a pasta se ela não existir
    if not os.path.isdir(target):
            os.mkdir(target)
    
    # Nome da collection no banco
    conta_db_table = d.mongo.db.contas
    if request.method == 'POST':
        
        # Envio de multiplas contas
        for upload in request.files.getlist("conta_image"):
            filename = secure_filename(upload.filename)
            destination = "/".join([target, filename])
            upload.save(destination)
            
            # converte o pdf para uma imagem, geralmente a conta só tem uma página 
            pages = convert_from_path(destination, 500)
            for page in pages:
                page.save('fatura.png', 'PNG')

            
            # identificando a imagem da fatura usando a biblioteca io e colocando em content
            with io.open('fatura.png', 'rb') as image_file:
                content = image_file.read()

            # prepara a imagem para a api
            image = vision.types.Image(content=content)


            # faz OCR
            response = client.text_detection(image=image)

            # pega o texto da ocr
            texts = response.text_annotations


            # identifica as posições das bouding box com as informações desejadas em texts
            a_dict = ['124','137','138','202','234','349','350','365','366','375','376', \
                '384','385','387','388','390','391','393','394','396','397','400','401', \
                '403','404','406','407','426','416','427','428','440','447','452']
            
            # coloca a legenda de cada posição
            b_dict = ['conta_mes','vencimento','total','tusd','te','mes0','consumomes0', \
                'mes2','consumomes2','mes3','consumomes3','mes4','consumomes4','mes5', \
                'consumomes5','mes6','consumomes6','mes7','consumomes7','mes8','consumomes8', \
                'mes9','consumomes9','mes10','consumomes10','mes11','consumomes11','mes12', \
                'consumomes12','mes13','consumomes13','saldo','saldo_pm','part']
           

            lst={}
            
            
            # fazer um loop em text para pegar cada parte de texto que a ocr indentificou
            for i, text in enumerate(texts):
                

                # faz um loop em a_dict para pegar as posições pré definimos
                for j, key in enumerate(a_dict):

                    # transforma o que está em a_dict em numero
                    key=int(key)
                        
                    # pega a posição definida manualmente dentro do ocr total, eliminando o que não é desejado    
                    if key == i:
                        
                        # retorna a informação associada a posição definida manualmente
                        texto=text.description

                        # coloca um label na posição
                        descricao=b_dict[j]
                        
                        # insere tudo em um dicionário
                        lst.update({descricao: texto})

            # coloca a informação no mongodb            
            conta_db_table.insert({'conta_image': lst})


    return {'Geral': {'conta_mes': lst['conta_mes'], 'VENCIMENTO': lst['vencimento'], \
        'TOTAL_A_PAGAR': lst['total']}, 'Operacao': {'ENERGIA_ATIVA_FORNECIDA': lst['tusd'], \
        'ENERGIA_ATIVA_INJETADA': lst['te']}, 'Informacoes': {'Saldo': lst['saldo'], \
        'Saldo_a_expirar': lst['saldo_pm'], 'Participacao': lst['part']}, \
        'Historico': {lst['mes2']: lst['consumomes2'], lst['mes3']: lst['consumomes3'], \
        lst['mes4']: lst['consumomes4'], lst['mes5']: lst['consumomes5'], \
        lst['mes6']: lst['consumomes6'], lst['mes7']: lst['consumomes7'], \
        lst['mes8']: lst['consumomes8'], lst['mes9']: lst['consumomes9'], \
        lst['mes10']: lst['consumomes10'], lst['mes11']: lst['consumomes11'], \
        lst['mes12']: lst['consumomes12'], lst['mes13']: lst['consumomes13']}}

if __name__ == '__main__':
    app.run()