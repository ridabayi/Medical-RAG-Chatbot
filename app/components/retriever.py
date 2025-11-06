# retriever.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.components.llm import load_llm
from app.components.vector_store import load_vector_store # N'oubliez pas d'implémenter cette fonction
from app.config.config import HUGGINGFACE_REPO_ID, HF_TOKEN
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

CUSTOM_PROMPT_TEMPLATE = """Répondez à la question médicale suivante en 2–3 lignes maximum en utilisant uniquement les informations fournies dans le contexte.

Context:
{context}

Question:
{question}

Réponse:
"""

def create_qa_chain():
    """Crée la chaîne RAG complète."""
    try:
        logger.info("🔍 Démarrage de la création de la chaîne QA...")

        # 1. Chargement de la base de données vectorielle (Retriever)
        db = load_vector_store()
        if db is None:
            # S'assurer que load_vector_store lève une CustomException en cas d'échec
            raise CustomException("Le Vectorstore n'a pas pu être chargé (db est None).") 
        logger.info("✅ Vectorstore chargé avec succès.")

        # 2. Chargement du LLM
        # La fonction load_llm lève maintenant une CustomException en cas d'échec
        llm = load_llm(huggingface_repo_id=HUGGINGFACE_REPO_ID, hf_token=HF_TOKEN)
        logger.info("✅ LLM chargé avec succès.")

        # 3. Création des composants de la chaîne
        # Utilisez l'objet 'db' pour créer le retriever
        retriever = db.as_retriever(search_kwargs={"k": 2})
        prompt = ChatPromptTemplate.from_template(CUSTOM_PROMPT_TEMPLATE)

        # 4. Assemblage de la chaîne RAG
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        logger.info("✅ Chaîne QA créée avec succès.")
        return rag_chain

    except CustomException as ce:
        # Capture les erreurs spécifiques levées par load_llm ou load_vector_store
        logger.error(f"❌ Échec de l'initialisation de la chaîne QA: {ce}")
        import traceback
        traceback.print_exc()
        return None
        
    except Exception as e:
        # Capture toutes les autres erreurs imprévues
        logger.error("❌ Exception inattendue lors de la création de la chaîne QA:")
        import traceback
        traceback.print_exc()
        return None