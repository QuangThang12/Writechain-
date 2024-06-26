from flask import Flask, render_template, request, jsonify
import openai
import solana
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.publickey import PublicKey
from solana.keypair import Keypair
import base64

app = Flask(__name__)

# Initialize OpenAI with your API key
openai.api_key = 'your-openai-api-key'

# Solana client
solana_client = Client("https://api.devnet.solana.com")

# Example Solana wallet (you should replace with your own)
sender = Keypair()
receiver_public_key = PublicKey("ReceiverPublicKeyHere")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['user_input']
    
    # Call OpenAI API to get suggestions
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=user_input,
        max_tokens=50,
        n=4,  # number of suggestions
        stop=None
    )
    
    suggestions = [choice['text'].strip() for choice in response.choices]
    
    # Store suggestions on Solana blockchain
    transaction = Transaction()
    for suggestion in suggestions:
        message_bytes = suggestion.encode('utf-8')
        transfer_params = TransferParams(
            from_pubkey=sender.public_key,
            to_pubkey=receiver_public_key,
            lamports=len(message_bytes)  # Example: number of bytes as lamports
        )
        transaction.add(transfer(transfer_params))

    solana_client.send_transaction(transaction, sender)
    
    return jsonify(suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)
