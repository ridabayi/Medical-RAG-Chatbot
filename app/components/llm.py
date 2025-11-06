from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from app.config.config import HF_TOKEN, HUGGINGFACE_REPO_ID
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_llm(huggingface_repo_id: str = HUGGINGFACE_REPO_ID, hf_token: str = HF_TOKEN):
    """
    Load a conversational LLM from Hugging Face.
    Compatible with langchain-huggingface >= 1.1.0
    """
    try:
        logger.info(f"💬 Loading conversational LLM: {huggingface_repo_id}")

        # 👉 On passe désormais les hyperparamètres directement
        endpoint = HuggingFaceEndpoint(
            repo_id=huggingface_repo_id,
            task="conversational",
            huggingfacehub_api_token=hf_token,
            temperature=0.3,
            max_new_tokens=256,
            top_p=0.95,
            do_sample=True
        )

        llm = ChatHuggingFace(llm=endpoint)

        logger.info("✅ Conversational LLM loaded successfully.")
        return llm

    except Exception as e:
        from traceback import format_exc
        error_msg = (
            f"Échec du chargement du LLM ({huggingface_repo_id}). "
            f"Vérifiez le HF_TOKEN et le REPO_ID. | Error: {e}\n{format_exc()}"
        )
        logger.error(error_msg)
        raise CustomException(error_msg) from e
