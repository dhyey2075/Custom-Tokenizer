# Simple Text Tokenizer API

A lightweight and easy-to-use Tokenization API built with FastAPI. It provides basic NLP functionality including text tokenization, frequency-based encoding, and decoding — all accessible via clean RESTful API endpoints.

## Features

- Simple text tokenization by removing punctuation and converting to lowercase
- Frequency-based token encoding (most frequent tokens get lower IDs)
- Token decoding back to original text
- RESTful API endpoints for all tokenization functions
- Lightweight and fast using FastAPI

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/tokenizer-api.git
cd tokenizer-api
```

2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Start the server
```bash
uvicorn server:app --reload
```

The API will be available at http://127.0.0.1:8000

## API Endpoints

- POST /tokenize — Tokenize input text  
- POST /encode — Encode list of tokens  
- POST /decode — Decode encoded list back to tokens  

Swagger/OpenAPI docs available at: http://127.0.0.1:8000/docs

## Example Usage

### Tokenize
**POST /tokenize**
```json
{
  "text": "Hello, how are you doing today?"
}
```

### Encode
**POST /encode**
```json
{
  "tokens": ["hello", "how", "are", "you", "doing", "today"]
}
```

### Decode
**POST /decode**
```json
{
  "encoded": [1, 2, 3, 4],
  "token_to_id": {
    "hello": 1,
    "how": 2,
    "are": 3,
    "you": 4
  }
}
```

## Project Structure

```
tokenizer-api/
├── tokenizer.py       # Core tokenization logic  
├── server.py          # FastAPI app and endpoints  
├── requirements.txt   # Python dependencies  
└── README.md          # Project documentation
```

## License

This project is licensed under the MIT License.

## Contributions

Feel free to open an issue or pull request with ideas, improvements, or bug fixes.

Made with ❤️ using Python and FastAPI.
