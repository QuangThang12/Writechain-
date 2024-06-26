from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Initialize OpenAI with your API key
openai.api_key = 'your-openai-api-key'

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
    return jsonify(suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)