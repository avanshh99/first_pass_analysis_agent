import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions

# Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
embedding_model = "models/embedding-001"

class GeminiEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __call__(self, texts):
        result = genai.embed_content(
            model=embedding_model,
            content=texts,
            task_type="retrieval_document"
        )
        return result["embedding"]

def process_pdf(file):
    try:
        # Initialize ChromaDB with explicit data path
        chroma_path = os.path.join(os.getcwd(), "chroma_data")
        os.makedirs(chroma_path, exist_ok=True)
        
        chroma_client = chromadb.PersistentClient(path=chroma_path)
        
        # Clear existing collection if it exists
        try:
            chroma_client.delete_collection("pitchdeck")
        except:
            pass  
        
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, "uploaded_pdf.pdf")
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(file.read())
            
            # Process the PDF
            loader = PyPDFLoader(temp_path)
            documents = loader.load()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_documents(documents)
            
            collection = chroma_client.create_collection(
                name="pitchdeck",
                embedding_function=GeminiEmbeddingFunction()
            )
            
            for i, chunk in enumerate(chunks):
                collection.add(
                    documents=[chunk.page_content],
                    metadatas=[chunk.metadata],
                    ids=[str(i)]
                )
            
            return collection
            
        finally:
            # Clean up the temporary file and directory
            try:
                os.remove(temp_path)
                os.rmdir(temp_dir)
            except:
                pass
                
    except Exception as e:
        raise Exception(f"PDF processing failed: {str(e)}")