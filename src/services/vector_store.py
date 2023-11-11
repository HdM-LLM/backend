from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from dotenv import load_dotenv, find_dotenv
import openai
import os

# Read local .env file and load API key
_ = load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]


# Load the document, split it into chunks, embed each chunk and load it into the vector store.
def load_document(document_path, db):
    # Load the document
    raw_documents = TextLoader(document_path).load()
    # Split the document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # Embed each chunk and load it into the vector store
    documents = text_splitter.split_documents(raw_documents)

    # Check if vector store exists
    if db is None:
        # Create a new vector store
        db = Chroma.from_documents(
            documents, OpenAIEmbeddings(), persist_directory="./data/vector_store"
        )
    else:
        text_ids = db.add_documents(documents)
        # Check if all documents were added to the vector store
        if len(text_ids) != len(documents):
            raise ValueError(
                f"Could not add all documents to vector store. {len(text_ids)} of {len(documents)} added."
            )
        else:
            print(f"Added {len(text_ids)} documents to vector store.")
    print(f"Document {document_path} loaded.")
    return db


# Search for similar documents in the vector store.
def search_similar_db(db, query, top_n=100):
    print(f"Searching for '{query}'...")
    similar_documents = db.similarity_search_with_relevance_scores(
        query, k=top_n)
    print(f"Found {len(similar_documents)} similar documents.")
    unique_metadata_similarity = {}
    for document in similar_documents:
        print(f"Similarity: {document[1]:.2f}")
        print(document[0].metadata)
        print("-" * 50)
        # print(document[0].page_content)

        if document[0].metadata not in unique_metadata_similarity.values():
            unique_metadata_similarity[document[0].metadata["source"]] = [
                document[1]]
        else:
            unique_metadata_similarity[document[0].metadata["source"]].append(
                document[1]
            )

    # Calculate average similarity for each metadata
    for key, value in unique_metadata_similarity.items():
        unique_metadata_similarity[key] = sum(value) / len(value)

    # Sort by similarity in descending order
    unique_metadata_similarity = dict(
        sorted(
            unique_metadata_similarity.items(), key=lambda item: item[1], reverse=True
        )
    )

    print("Combined similarity for each metadata:")
    for key, value in unique_metadata_similarity.items():
        print(f"{key}: {value:.2f}")


def init_db():
    # Check if vector store exists
    if os.path.exists("./data/vector_store"):
        print("Vector store already exists.")
        db = Chroma(
            persist_directory="./data/vector_store",
            embedding_function=OpenAIEmbeddings(),
        )
    else:
        db = None
    return db


db = init_db()

# Load documents into vector store
# db = load_document("./src/services/vector_input_data/perfect.txt", db)
# db = load_document("./src/services/vector_input_data/medium.txt", db)
# db = load_document("./src/services/vector_input_data/bad.txt", db)
# db = load_document(
#     "./src/services/vector_input_data/marketing_cover_letter.txt", db)

# Search for embeddings in the vector store that are similar to the query
search_similar_db(
    db,
    "Sehr gute Programmierkenntnisse in Java, sowie ein abgeschlossenes Studium der Informatik. Mehrjährige Erfahrung in dem Beruf sind von Vorteil."
)
