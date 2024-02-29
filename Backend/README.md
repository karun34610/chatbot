## Python Script running the langchain LLM model for chatbot running on Knowledge base

### How to run ?

1. clone the repository, (requirement : Python installed)
2. pip install flask
3. pip install flask-cors
4. In the root directory of the folder, run "python app.py"
5. Make sure that OPENAI_API_KEY is replaced in the ChatBot class

### File Structure

1. app.py contains the routes
2. Functions > Chatbot.py contains the ChatBot class
3. data folder contains the knowledge base

### API details

1. LOCALHOST_URL
2. Method : GET
3. Query Params : {"query":"<QUERY>"}
4. Response : {"answer":"<RESPONSE>"}
