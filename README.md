# Customer Support Chatbot for Hotel Bookings

A conversational AI chatbot that manages hotel room bookings with secure verification and booking persistence.

## Key Features

1. **Secure Verification System**
   - Unique verification codes serve as booking IDs
   - Codes required for accessing and managing bookings
   - Session persistence across multiple days
   - Customer registration verification

2. **Booking Management**
   - Room booking and availability checking
   - Booking modifications using verification codes
   - Booking cancellation system
   - Customer detail persistence

3. **Database System**
   - SQLite database for reliable data storage
   - Customer information management
   - Booking history tracking
   - Verification code management

## Project Structure
### Directory Overview

- `src/`: Main source code directory
  - `api/`: API routes and endpoints
  - `core/`: Core application logic and state management
  - `graphs/`: LangGraph configurations
  - `tools/`: External tool integrations
  - `prompts/`: Prompt templates and configurations
  - `config/`: Application settings and configurations
  - `database/`: SQLite database and models
  - `verification/`: Verification system logic

- `tests/`: Test suites
  - `unit/`: Unit test cases
  - `integration/`: Integration test cases

- `docs/`: Project documentation
- `logs/`: Application log storage
- `scripts/`: Deployment and setup scripts

## Key Components

- **FastAPI**: Web framework for building the API
- **LangGraph**: Conversational AI graph management
- **Google Generative AI**: Language model
- **Tavily Search**: Information retrieval tool
- **SQLite**: Local database for storing booking and customer data

## Verification System

1. **Registration Process**
   - Customer provides necessary details
   - System generates unique verification code
   - Code is provided to customer for future reference

2. **Booking Management**
   - Verification code required for:
     - Viewing existing bookings
     - Modifying booking details
     - Cancelling reservations
     - Accessing customer information

3. **Security Measures**
   - Unique code generation
   - Validation checks
   - Session management
   - Data persistence

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd [project-directory]
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env`:
   ```
   DATABASE_URL=sqlite:///./hotel_bookings.db
   GOOGLE_API_KEY=your_api_key
   TAVILY_API_KEY=your_tavily_key
   ```

5. Initialize the database:
   ```bash
   python scripts/init_db.py
   ```

6. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

## Development Status

⚠️ **Note: This is a development version**
- Currently in testing phase
- Not yet deployed in production
- Requires comprehensive testing
- Use other branches for stable versions

## Testing Requirements

1. **Verification System**
   - Code generation and validation
   - Session persistence
   - Security measures

2. **Booking Operations**
   - Room availability checking
   - Booking creation and modification
   - Cancellation processes

3. **Database Operations**
   - Data persistence
   - Query performance
   - Concurrent operations

## Future Improvements

1. **Testing**
   - Implement comprehensive test suite
   - Add integration tests
   - Performance testing
   - Security testing

2. **Features**
   - Enhanced security measures
   - Automated booking confirmations
   - Multiple room type support
   - Payment integration

## Contributing

1. Create a new branch for features
2. Implement required tests
3. Submit pull requests with test results
4. Document any changes to the verification system

## License

MIT License