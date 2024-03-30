from transformers import AutoTokenizer, AutoModel, AutoConfig
from langchain.llms.base import LLM
from typing import List, Optional

class GLM(LLM):
    max_token: int = 2048
    temperature: float = 0.001
    top_p = 0.9
    tokenizer: object = None
    model: object = None
    
    history_len: int = 1024
    
    def __init__(self):
        super().__init__()
        
    @property
    def _llm_type(self) -> str:
        return "GLM"
            
    def load_model(self, llm_device="gpu",model_name_or_path=None):
        model_config = AutoConfig.from_pretrained(model_name_or_path, trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path,trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_name_or_path, config=model_config, trust_remote_code=True).half().cuda()

    def _call(self,prompt:str,history:List[str] = [],stop: Optional[List[str]] = None):
        response, _ = self.model.chat(
                    self.tokenizer,prompt,
                    history=history[-self.history_len:] if self.history_len > 0 else [],
                    max_length=self.max_token,temperature=self.temperature,
                    top_p=self.top_p)
        return response

# PATH = "D:/Yu/rag/chatglm3-6b"
# # sys.path.append(modelpath)
# llm = GLM()
# llm.load_model(model_name_or_path = PATH)