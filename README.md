# Customer Support Chatbot For Tour Booking

A specialized chatbot for handling tour bookings, rescheduling, and cancellations using Redis cache for booking information management.

**Note: This repository is on the `twil-book` branch, which is separate from the `main` branch.**

## Project Structure
### Directory Overview

- `src/`: Main source code directory
  - `api/`: API routes and endpoints
  - `core/`: Core application logic and state management
  - `graphs/`: LangGraph configurations
  - `tools/`: External tool integrations
  - `prompts/`: Prompt templates and configurations
  - `config/`: Application settings and configurations

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
- **Redis**: Cache management for booking information

## Booking Rules and Constraints

1. **Date Validation**:
   - Bookings must be for future dates only
   - Maximum booking window is 30 days from current date
   - System validates dates before confirming bookings

2. **Rescheduling**:
   - Must be within the 30-day booking window
   - Original booking details are preserved in cache
   - Validation checks apply to new dates

3. **Cancellation**:
   - Available for any confirmed booking
   - Automatic cache cleanup upon cancellation

## Known Issues (as of December 27, 2024)

1. **Date Validation Bug**:
   - System incorrectly flags valid future dates as "old bookings"
   - Example: Request for "Jan 5 to Jan 8" returns error "01/05/2024 is old booking"
   - Status: Under Investigation

2. **Extended Booking Window Issue**:
   - System accepts bookings beyond the 30-day limit
   - Currently allows bookings up to 10 years in advance
   - Status: Fix Pending
   - Expected Behavior: Should reject bookings >30 days in advance

## Setup and Installation

1. Clone the repository
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
   REDIS_URL=your_redis_url
   GOOGLE_API_KEY=your_api_key
   TAVILY_API_KEY=your_tavily_key
   ```

5. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

## Contributing

When working on this branch:
1. Be aware of the current booking validation issues
2. Test any changes against the 30-day booking window requirement
3. Verify date validation logic for all booking operations

## Future Improvements

1. Implement proper date validation logic
2. Add booking window restrictions
3. Enhance error messages for invalid dates
4. Add automated tests for date validation scenarios