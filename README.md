# Slack Movie App
This is a Slack app built with the [Bolt for Python framework][2] that pulls a list of movies and returns the details for users.

Contents
========
- [](#)
  - [Running locally](#running-locally)
    - [1. Setup environment variables](#1-setup-environment-variables)
    - [2. Setup your local project](#2-setup-your-local-project)
    - [3. Start servers](#3-start-servers)
    - [4. Configure your slack app](#4-configure-your-slack-app)
  - [File/Folder Structure](#filefolder-structure)
  - [Testing](#testing)
  - [Approach](#approach)
  - [Roadmap](#roadmap)
  - [Contributing](#contributing)
  - [License](#license)

## Running locally

### 1. Setup environment variables
You can get your Bot Token and Signing Secret on the [Basic Information][5] tab.
The [movie DB API instructions][6] walk you through getting a token.

```zsh
# Replace with your signing secret, token, and key
export SLACK_BOT_TOKEN=<your-bot-token>
export SLACK_SIGNING_SECRET=<your-signing-secret>
export API_KEY=<your-movie-api-key>
```

### 2. Setup your local project
```zsh
# Clone this project onto your machine
git clone https://github.com/edgartan/slack_movie_app.git

# Change into this project
cd src

# Setup virtual environment and install dependencies
pipenv install
```

### 3. Start servers

[Setup ngrok][3] to create a local requests URL for development.

```zsh
ngrok http 3000
pipenv run python app.py
```

### 4. Configure your slack app
Update your [Event Subscriptions][1] Request URL with your ngrok hostname followed by /slack/events
For example: http://ad646ed78782.ngrok.io/slack/events

Update your [Interactivity & Shortcuts][4] Request URL and Options Load URL with your ngrok hostname followed by /slack/events
For example: http://ad646ed78782.ngrok.io/slack/events

## File/Folder Structure
```text
.
└── src: he code used to create the actual slack app
   └── app.py: Entry point for the slack app, handles the interactions between the user and the rest of the application
   └── api.py: Handles the external calls to the Movie Database
   └── utils.py: Useful methods for cleaner looking code
   └── conftest.py: Used to define the test root path
   └── tests: All programmatic tests
   └── views: Contains the json files of the Slack Block Kits
```

## Testing
```zsh
# Navigate into the src directory
cd src

# Install Dev dependencies
pipenv install --dev

# Run tests
pipenv run python -m pytest
```
## Approach
I started by reading through the [Getting Started Guide for Bolt][7] as well as a couple other getting started resources. From there I laid out a general plan of what I was planning to accomplish.

1. Create a hello world slack app
2. Figure out the general workflow of how to send a message
3. Connect to the MovieDB API and return actual data
4. Modify the UI elements to meet the requirements with [Block Kits][10]
5. Create unit tests
6. Add better error handling and logging
7. Create a good readme

I knew I could tackle this project a little differently, as I would be the only developer working on this code, I could be messier and cleanup at the end to save myself time.
Time would be the biggest factor and I wanted to prioritize the requirements spelled out vs what I assumed was needed, preferring completeness/thoroughness over shiney things.
This approach is not necessarily how I would tackle this at work since we have a team of engineers that work on portions. I did still follow trunk-based developement.
I would have likely done testing, error handling, and logging with smaller items so that they could be easily picked up by my team members.

## Roadmap
As I finish items on my roadmap I will move them to the approach section. This roadmap gives me an ordered list of my top priorities as well as any upcoming changes I would like to make.

8. Deploy to cloud hosted environment manually([aws lambda][8])
8. Script out deployment
8. Create infrastructure as code (aws_cdk)
8. Create CI/CD pipeline (github actions)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT][9]

[1]: https://api.slack.com/apps/A029AU6BDD4/event-subscriptions?
[2]: https://slack.dev/bolt-python/
[3]: https://slack.dev/bolt-python/tutorial/getting-started#setting-up-events
[4]: https://api.slack.com/apps/A029AU6BDD4/interactive-messages?
[5]: https://api.slack.com/apps/A029AU6BDD4/general?
[6]: https://developers.themoviedb.org/3/getting-started/introduction
[7]: https://slack.dev/bolt-python/tutorial/getting-started
[8]: https://github.com/slackapi/bolt-python/tree/main/examples/aws_lambda
[9]: https://choosealicense.com/licenses/mit/
[10]: https://app.slack.com/block-kit-builder/

https://github.com/slackapi/bolt-examples-aws-re-invent-2020/tree/main/api-gateway-lambda/python
https://github.com/zappa/Zappa
https://chatbotslife.com/developing-your-own-bot-for-slack-and-serverless-deploy-a49136f68b7a