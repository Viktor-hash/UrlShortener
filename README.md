# URL Shortener Service

## Description
A simple URL shortening service that creates shortened URLs and tracks their usage.

## Requirements
No specific language requirement - Python 3.8+, Java 11+, Go 1.19+ all fine, just document your choice

## Installation

There is a setup script to run `sh setup.sh` this will ask you what language you are going to use, and setup the project structure for you.

```bash
# Example for Python
pip install -r requirements.txt

# Example for Java
mvn clean install

# Example for Go
go mod download
```

## Running the Application
```bash
# Example for Python
python app.py

# Example for Java
java -jar target/url-shortener.jar

# Example for Go
go run main.go
```

The service will start on `http://localhost:8080`

## API Endpoints

### Create Short URL
```bash
curl -X POST http://localhost:8080/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com"}'
```

### Access Shortened URL
```bash
curl -L http://localhost:8080/{shortCode}
```

### Get URL Statistics
```bash
curl http://localhost:8080/api/stats/{shortCode}
```

## Running Tests
```bash
# Example commands
python -m pytest
mvn test
go test ./...
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
