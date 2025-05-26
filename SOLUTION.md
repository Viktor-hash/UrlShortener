# Solution Documentation

## Approach
Built a RESTful API service using Flask and flask-restx for the URL shortening service. Implemented a clean architecture with clear separation of concerns and comprehensive test coverage.

## Architecture Decisions

### URL Shortening Algorithm
Using Hashids library to generate short codes. This provides:
- Guaranteed unique codes based on incremental IDs
- Non-sequential, URL-safe output
- Minimum length of 6 characters
- Reversible encoding if needed

### Data Storage
Using two in-memory dictionaries:
- `url_store`: Maps short codes to URL data (original URL, visits, creation date)
- `url_to_code`: Maps original URLs to short codes for duplicate detection
Chosen for simplicity and fast access times in a demo environment.

### API Design
RESTful API with three main endpoints:
- POST /shortener/shorten: Create shortened URLs
- GET /shortener/{shortcode}: Redirect to original URL
- GET /shortener/stats/{shortcode}: Retrieve usage statistics

## Key Components

### URL Shortener Service
- Purpose: Handles URL shortening and storage
- Implementation: Uses Hashids for encoding, maintains counter for unique IDs
- Includes duplicate URL detection

### Statistics Tracking
- Purpose: Monitors URL usage and access patterns
- Implementation: Tracks visit count and creation timestamp
- Provides endpoint for retrieving statistics

## Trade-offs and Assumptions

### Trade-offs
- In-memory storage vs. Persistence: Chose in-memory for simplicity, sacrificing durability
- Single server vs. Distributed: Single server implementation limits scalability
- Simple vs. Complex short codes: Opted for longer but guaranteed unique codes

### Assumptions
- Service runs on a single instance
- Memory is sufficient for storage
- Short codes are case-sensitive

## Performance Considerations
- O(1) lookup time using dictionary storage
- Minimal computation overhead in short code generation
- No database I/O overhead
- Efficient duplicate URL detection

## Security Considerations
- Rate limiting could be added
- Hashids salt for unpredictable codes

## Future Improvements
If I had more time, I would:
1. Add persistent storage (Redis/PostgreSQL)
2. Implement rate limiting
3. Create a simple frontend
4. Add monitoring and logging
5. Implement user authentication
6. Add more tests cases for edge scenarios

## Challenges Faced
- Ensuring unique codes while handling duplicates
- Balancing code length with collision probability
- Designing clean test cases

## Time Breakdown
- Setup and planning: 20 minutes
- Core implementation: 1 hour 30 minutes
- Testing: 40 minutes
- Documentation: 25 minutes
- Total: ~3 hours