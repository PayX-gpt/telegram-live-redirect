from flask import Flask, request, redirect
import re

app = Flask(__name__)
LINK_PADRAO = "https://t.me/+Hs4dAVm7mMI2MmQx"
ultimo_link = LINK_PADRAO

@app.route("/")
def home():
    return "Servidor da Sigma Academy ativo!"

@app.route("/live")
def redirecionar_live():
    return redirect(ultimo_link, code=302)

@app.route("/webhook", methods=["POST"])
def receber_telegram():
    global ultimo_link
    dados = request.get_json()
    if not dados or "message" not in dados:
        return "Ignorado", 200

    texto = dados["message"].get("text", "")
    grupo_id = str(dados["message"]["chat"].get("id", ""))

    if grupo_id != "-1001437665629":
        return "Outro grupo", 200

    match = re.search(r"https://meet\.google\.com/[a-z\-]+", texto)
    if match:
        ultimo_link = match.group(0)
        print(f"[ATUALIZADO] Novo link do Meet: {ultimo_link}")

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
