###### Importing all the required Libraries
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.evaluation import load_evaluator
#########


############ Created this class to handle the queries by the customer
############ which makes use of Langchain Library


class Chatbot:

  api_key = ""

  ####### Memory is maintained for the session with the help of chat_history list. 
  chat_history = []  
  ######

  def __init__(self, api_key="OPENAI_API_KEY", chat_history=[]):
    self.api_key = api_key
    self.chat_history = chat_history

  def run(self):
    documents, i = self.load_docs()

    print("success to fetch the docs")

    db =  self.get_similar_docs(documents)

    print("success to initiate the db")

    chain = self.chatBot(db)

    print("success to initiate the Chain")

    return db, chain


  ############## Loads the documents from the text files

  def load_docs(self, directory='data'):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents, len(documents)

  ############## Divides each documents into smaller chunks for fast processing
  ############## Creates FAISS Vector store with OpenAIEmbeddings

  def get_similar_docs(self, documents):
    
    text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # Create embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
    # Create FAISS vector store
    db = FAISS.from_documents(texts, embeddings)

    # Create VectorStoreRetrieverMemory
    retriever = db.as_retriever()

    return db
  

  ############## From the Promt provided, the Chain is called from the LLM of model GPT 3.5 Turbo

  def chatBot(self, db):
    template = """
    ### Instruction : You are a pan card support agent that is talking to a customer. Use only the chat history and the following information.
    {context}
    Keep your replies short and informative.
    {chat_history}
    ### Input : {question}
    ### Response:
    """.strip()

    prompt = PromptTemplate(input_variables=["context", "question","chat_history"], template=template)

    llm = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo', openai_api_key=self.api_key)

    # chain = ConversationalRetrievalChain.from_llm(
    #     llm = llm,
    #     chain_type="stuff",
    #     retriever=db.as_retriever(),
    #     combine_docs_chain_kwargs={"prompt":prompt},
    #     return_source_documents = True,
    #     verbose=True
    # )

    chain1 = load_qa_chain(
      llm=llm,
      chain_type="stuff",
      prompt = prompt
    )

    return chain1


  #################### If chain, Vectorstore DB is provided, returns the response to the query

  def chat(self, chain, query, db):
  
    docs = db.similarity_search(query)

    answer = chain.run({
      "question":query, 
      "chat_history":self.chat_history,
      "input_documents":docs
    })

    self.chat_history.append((query, answer.strip()))

    return answer.strip()
  
  ########## Evaluvation of the chain
  
  def evaluvate(self, query, pred, ref):
    
    evaluator = load_evaluator("qa")

    evaluator.evaluate_strings(
        prediction=pred,
        input=query,
        reference=ref
    )
    

