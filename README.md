---
date: 2024-04-23T16:37:55.196481
author: AutoGPT <info@agpt.co>
---

# emoji-explainer

create an endpoint that connects to groq https://console.groq.com and takes in an emoji as input and explains to the user the meaning of it

**Features**

- **Emoji Interpretation Interface** A simple and intuitive interface where users can input emoji characters and receive their meanings.

- **Connection to GROQ API** Securely connect to the GROQ API to fetch interpretations of emojis.

- **Responsive Design** Ensure the application is responsive and provides a consistent experience across various devices and screen sizes.

- **User Feedback System** Allow users to submit feedback on the emoji interpretations or report inaccuracies.


## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'emoji-explainer'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
