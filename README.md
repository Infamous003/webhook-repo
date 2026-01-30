# webhook-repo

This project captures GitHub repository events (push, pull request, merge) from [action-repo](https://github.com/Infamous003/action-repo) using **webhooks**. It stores events in MongoDB, and displays them in a minimal UI that auto updates every 15 seconds.


#### Architecture
![diagram](./diagram.png)

#### Tech Stack
- Flask
- MongoDB
- GitHub Webhooks
- Vanilla JS + HTML & CSS
- Ngrok (local testing)

#### Endpoints

1. `POST /webhook/receiver` - Receiver

`action-repo` sends action events to this endpoint, which classifies events into PUSH, PULL_REQUEST, and MERGE and stores them in MongoDB.

2. `GET /api/events` - Frontend UI polls to this endpoint.

Query Parameters:
  - `since`: period from when the events should be returned

Example Response:
```json
[
  {
    "action": "MERGE",
    "author": "Infamous003",
    "from_branch": "awesome-branch",
    "request_id": "3227727886",
    "timestamp": "2026-01-30T12:52:31+00:00",
    "to_branch": "main"
  },
  {
    "action": "PUSH",
    "author": "Infamous003",
    "from_branch": null,
    "request_id": "4637e3504a293685d8e0ea4530998eefc5a823e3",
    "timestamp": "2026-01-30T12:52:30+00:00",
    "to_branch": "main"
  },
  {
    "action": "PULL_REQUEST",
    "author": "Infamous03",
    "from_branch": "awesome-branch",
    "request_id": "3227727886",
    "timestamp": "2026-01-30T12:51:47+00:00",
    "to_branch": "main"
  }
]
```

3. `GET /` - serves the frontend page, displaying all the events and updating every 15 seconds.

#### Setup instructions

1. Clone the repository and cd into it
```bash
git clone https://github.com/Infamous003/webhook-repo.git
```

2. create and activate a virtual environment
```bash
python3 -m venv venv
```

On windows:
```bash
.\venv\Scripts\activate.bat
```

On Linux:
```bash
source venv/bin/activate
```

3. Set up env variables

Create a `.env` file in the root dir
```env
MONGO_URI=<mongo_uri>
MONGO_DB_NAME=<db_name>
```

The app uses `python-dotenv` to automatically load these variables when you run `run.py`

4. Make sure mongodb is installed and connected.

5. Run the server
```bash
python3 run.py
```

6. Expose the local server using ngrok and configure the webhook url in `action-repo`'s webhook settings.

If you're following the steps, the page should be available at `http://localhost:5000`