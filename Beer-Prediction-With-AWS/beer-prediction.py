#Pergunta ao usuário o tipo de cerveja
while(True):
    print("\n Qual o tipo da cerveja?\n 1 - Ale\n 2 - Barleywine\n 3 - IPA\n 4 - Porter\n 5 - Stout\n 6 - Tripel")
    try:
        tipoCerveja = int(input(" > "))
        if tipoCerveja >= 1 and tipoCerveja <= 6:
            break
    except ValueError: 
        tipoCerveja = 0.0

    print ("Tipo de cerveja inválido.")
    
#De acordo com o tipo de cerveja, define os valores das variáveis
IsAle           = 1 if tipoCerveja == 1 else 0
IsBarleywine    = 1 if tipoCerveja == 2 else 0
IsIPA           = 1 if tipoCerveja == 3 else 0
IsPorter        = 1 if tipoCerveja == 4 else 0
IsStout         = 1 if tipoCerveja == 5 else 0
IsTripel        = 1 if tipoCerveja == 6 else 0

#Nome do tipo de cerveja
tipoNome = "Ale" if tipoCerveja == 1 else "Barleywine" if tipoCerveja == 2 else "IPA" if tipoCerveja == 3 else "Porter" if tipoCerveja == 4 else "Stout" if tipoCerveja == 5 else "Tripel" if tipoCerveja == 6 else "Não identificado"

#Pergunta ao usuário o teor alcoólico
while(True):
    print("\n Qual o teor alcoólico? (3.0 a 15.0)")
    try:
        teorAlcoolico = float(input(" > "))
        if teorAlcoolico >= 3.0 and teorAlcoolico <= 15.0:
            break
    except ValueError: 
        teorAlcoolico = 0.0

    print ("Teor alcoólico inválido.")
       
#Mensagem de introdução à predição
print("\n----------------------------------------------------------------------------------")
print(" A predição será realizada com os seguintes parâmetros:")
print("   > Tipo de Cerveja: ", tipoNome)
print("   > Teor alcoólico:  ", teorAlcoolico)
print(" ")
print(" Aguarde enquanto aquecemos os motores...")
print("----------------------------------------------------------------------------------")

#Inicialização do client da AWS
import boto3
client = boto3.client('machinelearning', 
                      aws_access_key_id='x', 
                      aws_secret_access_key='y', 
                      region_name='us-east-1')

#Monta o payoad de chamada da API
record = {
    'IsAle':        str(IsAle),
    'IsBarleywine': str(IsBarleywine),
    'IsIPA':        str(IsIPA),
    'IsPorter':     str(IsPorter),
    'IsStout':      str(IsStout),
    'IsTripel':     str(IsTripel),
    'abv':          str(teorAlcoolico),
}

#Chamada da API
response = client.predict(
    MLModelId='ml-yFV54ggXiis',
    Record=record,
    PredictEndpoint='https://realtime.machinelearning.us-east-1.amazonaws.com'
)

#Obtem o valor da predição na resposta da API
try:
    import json
    new_rate = response["Prediction"]["predictedValue"]
except ValueError:
    new_rate = -1
    print (" Valor de predição inválido.")
    
#Define uma mensagem de acordo com a predição
msg_pred = ""
if (new_rate <= 2):
    msg_pred = "Sua cerveja seria intragável. Precisa melhorar."
elif (new_rate <= 3):
    msg_pred = "Ainda dá pra melhorar..."
elif (new_rate <= 4):
    msg_pred = "Boa combinação. Não é a melhor no entanto."
else:
    msg_pred = "Excelente cerveja. Me chame para a inauguração!"


#Mensagem de finalização da predição
if (new_rate >= 0):
    print("\n====================================================================================")
    print(" Predição realizada com sucesso. Sua nova cerveja possuiria a seguinte avaliação:")
    print("   > %.2f" % new_rate)
    print("   >", msg_pred)
    print("====================================================================================")
