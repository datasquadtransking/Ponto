from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
import datetime

app = Flask(__name__)

# CONFIGURAÇÕES FIXAS
EMAIL_REMETENTE = "automac@transking.com.br"
SENHA_EMAIL = "P3dr0Tk2025"
EMAIL_DESTINATARIO = "weslleyworksilva@yahoo.com"
SMTP_SERVIDOR = "smtp.task.com.br"
SMTP_PORTA = 587

def enviar_email_task(dados):
    msg = EmailMessage()
    corpo = f"""
    📌 RELATÓRIO DE PONTO DIÁRIO - TRANSKING
    ----------------------------------
    Colaborador: {dados['nome']}
    CPF: {dados['cpf']}
    Data: {dados['data']}
    
    HORÁRIOS REGISTRADOS:
    - Entrada: {dados['entrada']}
    - Saída Almoço: {dados['saida_almoco']}
    - Retorno Almoço: {dados['retorno_almoco']}
    - Saída Final: {dados['saida_final']}
    ----------------------------------
    Enviado via Sistema de Contingência.
    """
    msg.set_content(corpo)
    msg['Subject'] = f"PONTO: {dados['nome']} - {dados['data']}"
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO

    try:
        server = smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_EMAIL)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    dados = {
        'nome': request.form['nome'],
        'cpf': request.form['cpf'],
        'entrada': request.form['entrada'],
        'saida_almoco': request.form['saida_almoco'],
        'retorno_almoco': request.form['retorno_almoco'],
        'saida_final': request.form['saida_final'],
        'data': datetime.datetime.now().strftime("%d/%m/%Y")
    }

    if enviar_email_task(dados):
        return f"<h1>Sucesso!</h1><p>Relatório de {dados['nome']} enviado com sucesso.</p>"
    else:
        return "<h1>Erro!</h1><p>Houve um problema ao enviar o e-mail. Verifique a conexão.</p>"

if __name__ == '__main__':
    app.run(debug=True)