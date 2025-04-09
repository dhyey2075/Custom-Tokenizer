from tokenizer import Tokenizer


text = "Hello, how are you doing today? Hello you! Are you okay?"
tokenizer = Tokenizer()
simple_tokens = tokenizer.simple_tokens(text)
encodings = tokenizer.encode(simple_tokens)
decodings = tokenizer.decode(encodings[0], encodings[1])

print("Simple tokens: ", simple_tokens)
print("\n")
print("Token to id: ", encodings[1])
print("\n")
print("Encodings: ", encodings[0])
print("\n")
print("Decodings: ", decodings)