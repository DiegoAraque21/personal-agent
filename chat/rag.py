from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import NLTKTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import nltk
import ssl
from typing import List

# ssl._create_default_https_context = ssl._create_unverified_context

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

class RAG:

    def __init__(
        self,
        persist_dir: str = "chroma_store",
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.persist_dir = persist_dir
        self.model_name = model_name

        self.embedding = HuggingFaceEmbeddings(model_name=self.model_name)

        self._create_vstore()


    def _create_vstore(self):
        """
        Creates the vector store.
        :return: None
        """
        with open(f"knowledge/diego_araque_knowledge_base.txt", 'r', encoding='utf-8') as f:
            full_content = f.read()
        document = Document(page_content=full_content, metadata={"source": "knowledge_base"})
        self.vstores = Chroma.from_documents(documents=[document], embedding=self.embedding, persist_directory=self.persist_dir)

    def get_relevant_chunks(self, query: str, k: int = 4) -> List[str]:
        """
        Gets relevant chunks from the vector store using a similarity score threshold.
        Does NOT fall back to reading the full document.
        """
        retriever = self.vstores.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )

        docs = retriever.invoke(query)
        return [doc.page_content for doc in docs]


    