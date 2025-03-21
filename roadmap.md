# Anime Game Bot Roadmap

This roadmap outlines the steps to build an automated bot that plays an anime comparison game ("Higher or Lower") by fetching scores from the Jikan API and storing data in a MongoDB database. The bot will automatically interact with the game website, compare scores, and choose the higher-scored anime.

## Phase 1: Planning and Setup
1. **Define Project Scope**
   - Understand the game mechanics and requirements
   - List features the bot should have:
     - Automatically open the game website in Brave browser
     - Scan for anime titles
     - Check a database for existing entries
     - Fetch scores from the Jikan API if not found in the database
     - Save new entries to the database
     - Compare scores and choose the higher one

2. **Set Up Development Environment**
   - Install Node.js and npm
   - Install Brave browser (if not already installed)
   - Install MongoDB (local or use MongoDB Atlas)
   - Install required tools:
     - Puppeteer (for browser automation)
     - Express (for backend server)
     - Mongoose (for MongoDB interaction)
     - Axios (for API requests)

3. **Create Folder Structure**
   - Organize the project into folders:
     - `server/` for the backend
     - `bot/` for the bot logic
     - `README.md` for documentation
     - `.env` for environment variables

## Phase 2: Backend Development
1. **Set Up MongoDB**
   - Create a MongoDB database (local or cloud-based)
   - Define a schema for storing anime data (title, score, and MAL ID)
   - Set up indexes for faster querying

2. **Build the Backend Server**
   - Set up an Express server
   - Create routes for:
     - Fetching anime data from the database
     - Saving new anime data to the database
   - Connect the server to MongoDB

3. **Test the Backend**
   - Use tools like Postman to test the API endpoints
   - Ensure data is correctly saved and retrieved from the database

## Phase 3: Bot Development
1. **Set Up Puppeteer**
   - Configure Puppeteer to launch Brave browser
   - Write a script to open the game website

2. **Implement Anime Title Extraction**
   - Use Puppeteer to extract the two anime titles from the game website
   - Develop algorithms to handle different formats and edge cases

3. **Implement Database Interaction**
   - Write functions to:
     - Check if an anime exists in the database
     - Save new anime data to the database
     - Update existing entries if needed

4. **Implement Jikan API Integration**
   - Write functions to fetch anime scores from the Jikan API
   - Handle API rate limits and errors
   - Implement caching to reduce API calls

5. **Implement Score Comparison**
   - Compare the scores of the two anime
   - Use Puppeteer to click the button for the higher-scored anime
   - Track success rate and decision logic

6. **Add Delay and Loop**
   - Add a delay between rounds to avoid overwhelming the game website
   - Implement random timing variations to appear more human-like
   - Loop the bot to keep playing continuously

## Phase 4: Testing and Debugging
1. **Test the Bot Locally**
   - Run the bot on a local test page to ensure it works as expected
   - Verify that:
     - Anime titles are correctly extracted
     - Scores are fetched and saved to the database
     - The bot chooses the correct anime

2. **Test the Bot on the Actual Game Website**
   - Run the bot on the actual game website
   - Monitor for any issues (e.g., anti-bot measures, API rate limits)
   - Collect performance metrics

3. **Debug and Optimize**
   - Fix any bugs or errors
   - Optimize the bot for speed and reliability
   - Reduce resource usage

## Phase 5: Deployment and Automation
1. **Deploy the Backend**
   - Deploy the backend server to a cloud platform (e.g., Heroku, Render, or Vercel)
   - Ensure the MongoDB connection is secure
   - Set up environment variables

2. **Run the Bot**
   - Run the bot script on your local machine or a server
   - Ensure it can run continuously without interruptions
   - Implement restart mechanisms for crashes

3. **Add Error Handling**
   - Handle edge cases (e.g., anime not found, API errors)
   - Add retries for failed requests
   - Implement logging for errors

## Phase 6: Documentation and Final Touches
1. **Write Documentation**
   - Update the README.md file with:
     - Project description
     - Setup instructions
     - Usage instructions
     - Troubleshooting guide

2. **Add Comments to Code**
   - Add comments to explain the code logic
   - Ensure the code is clean and readable
   - Refactor complex sections

3. **Test the Final Product**
   - Run the bot for an extended period to ensure stability
   - Verify that it performs well on the leaderboard
   - Document its success rate and limitations

## Phase 7: Future Enhancements
1. **Add a User Interface**
   - Build a simple UI to start/stop the bot and monitor its progress
   - Display statistics and performance metrics
   - Allow configuration changes

2. **Add Logging**
   - Log bot actions (e.g., anime titles, scores, choices) for debugging and analysis
   - Create visualizations of performance data
   - Implement alerts for unusual patterns

3. **Expand the Database**
   - Add more fields to the database (e.g., genres, popularity) for advanced analysis
   - Create a more sophisticated scoring algorithm that considers multiple factors
   - Implement machine learning to improve decision-making

4. **Improve Anti-Bot Measures**
   - Randomize delays and actions to avoid detection
   - Implement more human-like interaction patterns
   - Add CAPTCHA solving capabilities if necessary

## Timeline
- **Week 1**: Planning, setup, and backend development
- **Week 2**: Bot development and testing
- **Week 3**: Deployment, debugging, and documentation
- **Week 4**: Final touches and future enhancements