from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import google.generativeai as genai
import os
import textwrap
import PyPDF2

# Configuration de l'API Google Generative AI
GOOGLE_API_KEY = 'AIzaSyBmCdVkJC9cxHyCkj-Tf08WRRe5oANsQ7I'
genai.configure(api_key=GOOGLE_API_KEY)

# Utilisation du modèle de génération Google
model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY, temperature=0.2)

# Fonction pour afficher du texte en Markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Charger et diviser plusieurs PDF à partir d'un répertoire
<<<<<<< HEAD
pdf_directory = "C:/ChatBot-main/data"
=======
pdf_directory = "C:/Users/user/Desktop/M3/deepLearning/flask/ChatBot-main/data"

>>>>>>> 0e92508580462dc9fe6c3eff840b591b7d6d55c8
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

pages = []
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_directory, pdf_file)
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pages.append(page.extract_text())  # Extract text from each page

# Préparer le texte pour l'intégration avec les embeddings
text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
context = "\n\n".join(str(page) for page in pages)
texts = text_splitter.split_text(context)

# Générer les embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

# Vérification des embeddings
if not texts:
    raise ValueError("No text found to generate embeddings.")

embedding_vectors = embeddings.embed_documents(texts)
if len(embedding_vectors) == 0:
    raise ValueError("Embeddings generation resulted in an empty list.")

# Créer les objets Document à partir des textes
documents = [Document(page_content=text) for text in texts]

# Création du vecteur index en utilisant Chroma
vector_index = Chroma.from_documents(documents=documents, embedding=embeddings)

# Modèle de question et de réponse pour la cybersécurité
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Keep the answer as concise as possible and focus on cybersecurity best practices. Always say "thanks for asking!" at the end of the answer.
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

# Chaîne de récupération et de réponse
qa_chain = RetrievalQA.from_chain_type(
    model,
    retriever=vector_index.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)
