class Tokenizer:
    def simple_tokens(self, text):
        punctuations = '''!()-[]{};:'",<>./?@#$%^&*_~'''
        clean_text = ""

        for char in text:
            if char in punctuations:
                #Ignore the punctuations
                clean_text += ' '
            else:
                #Make all text to lowercase
                clean_text += char.lower()
        return clean_text.split()

    def encode(self, tokens: list[str]):
        freq = {}
        #counting freq of each word
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1

        #sorting acc to freq
        sorted_tokens = sorted(freq.items(), key=lambda x: (-x[1], x[0]))

        #making a token_to_id dict
        token_to_id = {token: idx + 1 for idx, (token, _) in enumerate(sorted_tokens)}

        #encode acc to freq
        encoded = [token_to_id[token] for token in tokens]

        return encoded, token_to_id

    def decode(self, encoding: list[int], token_to_id: dict):
        id_to_token = {v: k for k, v in token_to_id.items()}
        return [id_to_token[i] for i in encoding]
