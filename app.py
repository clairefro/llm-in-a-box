from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def prompt():
    data = request.json
    prompt_text = data.get('prompt')

    if not prompt_text:
        return jsonify({"error": "No prompt provided"}), 400

    # TODO: make port flexible
    ollama_api_url = 'http://localhost:11434/api/generate' 

    try:
        # TODO: make model flexible
        payload = {
          "model": "mistral",
          "prompt": prompt_text,
          "system": "talk like a pirate",
          "stream": False
        }

        response = requests.post(ollama_api_url, json=payload)

        if response.status_code == 200:
            ollama_res = response.json()
            api_res = {
              "model": ollama_res["model"],
              "response": ollama_res["response"],
              "total_duration": ollama_res["total_duration"],
              "prompt_eval_duration": ollama_res["prompt_eval_duration"],
              "eval_duration": ollama_res["eval_duration"] ,
              "load_duration": ollama_res["load_duration"]
            }

            return jsonify(api_res), 200
        else:
            return jsonify({"error": "Error from Ollama API", "status_code": response.status_code}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
