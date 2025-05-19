import requests
import yaml

# Load configuration
def load_config():
    with open("config/config.yaml", "r") as config_file:
        return yaml.safe_load(config_file)

class PersuaderAgent:
    def __init__(self, config):
        self.model_name = config['model']['ollama_model']
        self.ollama_url = config['model']['ollama_url']

    def generate_response(self, prompt, stream=False):
        """
        Send a prompt to the Ollama API and get a response from the model.
        
        Args:
            prompt (str): The input text to send to the model
            stream (bool): Whether to stream the response or not
            
        Returns:
            The model's response as a string
        """
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": stream
        }
        
        try:
            response = requests.post(self.ollama_url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            if stream:
                # Handle streaming response
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        json_response = json.loads(line)
                        text_chunk = json_response.get("response", "")
                        full_response += text_chunk
                        print(text_chunk, end="", flush=True)
                    if json_response.get("done", False):
                        print()  # Add newline at the end
                        break
                return full_response
            else:
                # Handle non-streaming response
                json_response = response.json()
                return json_response.get("response", "")
                
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {e}")
            return None

    def query(self, conversation, question):
        # Generate the response from the model
        prompt = f"{conversation} Question: {question}"
        response = self.generate_response(prompt, stream=False)
        return response
