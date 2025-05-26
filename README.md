# URL Shortener Service

## Description
A simple URL shortening service that creates shortened URLs and tracks their usage.

## Requirements

- Python 3.8+

## Running the Application
```bash
# Example for Python
python app.py
```

The service will start on `http://localhost:8080`

## API Endpoints

You can access the following endpoints using Swagger UI at `http://localhost:8080/'

### Create Short URL
```bash
curl -X POST http://localhost:8080/shortener/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com"}'
```

### Access Shortened URL
```bash
curl -L http://localhost:8080/shortener/{shortCode}
```

### Get URL Statistics
```bash
curl http://localhost:8080/shortener/stats/{shortCode}
```

## Running Tests
```bash
python -m pytest
```

## Project Structure
```
.
├── README.md
├── SOLUTION.md
├── [main application file]
├── [test files]
└── [configuration/dependency files]
```

## Notes
- The application uses in-memory storage
- Short codes are case-sensitive
