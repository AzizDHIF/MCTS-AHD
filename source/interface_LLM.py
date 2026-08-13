
import logging


class InterfaceAPI:
    _total_calls = 0
    
    def __init__(self, api_endpoint, api_key, model_LLM, debug_mode):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.client = model_LLM
        self.debug_mode = debug_mode
        self.n_trial = 5

    def get_response(self, prompt_content, temp=1.):

        logging.info(
            "=== PROMPT LLM (temp=%s) ===\n%s\n=== FIN PROMPT ===",
            temp, prompt_content
        )

        response = self.client.chat_completion(1, [{"role": "user", "content": prompt_content}], temperature=temp)
        ret = response[0].message.content

        logging.info(
            "=== REPONSE LLM ===\n%s\n=== FIN REPONSE ===",
            ret
        )

        InterfaceAPI._total_calls += 1

        logging.info(
            "=== TOTAL CALLS LLM ===\n%s\n=== FIN TOTAL CALLS ===",
            InterfaceAPI._total_calls
        )

        return ret