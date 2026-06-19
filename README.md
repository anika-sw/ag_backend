# AutomatedGroove Backend

Streaming services automatically scan audio for copyrighted content, and mute or block uploads featuring this content. This makes it difficult for content creators to find appropriate background music. Our app, AutomatedGroove, automatically generates royalty-free music for content creators, saving them time and money.

Find the frontend repository here: [AutomatedGroove Frontend](https://github.com/anika-sw/ag_frontend)

## Version Notes

**v2 (current):** Replaced Musicfy AI with [ElevenLabs](https://elevenlabs.io) for music generation. Musicfy's API became degraded and unreliable, returning server-side errors consistently.


## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Implementation](#implementation)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [License](#license)
- [Creators](#creators)


## Installation

1. Clone the repository to your local machine:
	```sh
	git clone https://github.com/anika-sw/ag_backend.git
	```
2. Navigate into the repository:
	```sh
	cd ag_backend
	```
3. Create a virtual environment:
	```sh
	python -m venv venv
	```
4. Activate the virtual environment:
	```sh
	source venv/bin/activate     # On Windows use `venv\Scripts\activate`
	```
5. Install dependencies:
	```sh
	pip install -r requirements.txt
	```


## Deployment

This backend is deployed on [Render](https://render.com). Render was chosen over Heroku because the Musicfy API can take longer than 30 seconds to generate a song. Heroku enforces a hard 30-second request timeout (H12 error) that cannot be configured away, which causes song generation requests to fail. Render does not have this limitation.


## Configuration

Set the following environment variables in a `.env` file (or as environment variables in your Render service):

-  `OPENAI_API_KEY`
-  `ELEVENLABS_API_KEY`
-  `RECAPTCHA_SECRET_KEY`

>_Note: You need to obtain your own API keys from **OpenAI**, **ElevenLabs**, and **Google reCAPTCHA** to use in this project._


## Implementation

1. Run the `flask` development server:
	```sh
	$ flask run
	```
2. To access the application locally, open a web browser and go to [http://localhost:5000](http://localhost:5000).


## API Documentation 

**Endpoint**: `/create_song_name`
- Method:  `POST`

- Description: Generates a song name based on the provided genre, mood, and tempo.

**Request Body**
The request body should be a JSON object containing the following fields:
```json
{
  "genre": ["pop"],
  "mood": ["happy"],
  "tempo": ["medium"]
}
```

**Response Body**
The response will be a JSON object containing a generated song name.
```
"Song Name”
``` 

**Endpoint**: `/create_song`

- Method:  `POST`

- Description: Generates an instrumental song based on the provided genre, mood, and tempo using the ElevenLabs API. The audio is saved server-side and a local file URL is returned.

**Request Body**
The request body should be a JSON object containing the following fields:
```json
{
  "genre": ["pop"],
  "mood": ["happy"],
  "tempo": ["medium"]
}
```

**Response Body**
```json
[
  {
    "file_url": "/songs/<filename>.mp3",
    "type": "music",
    "prompt": "the generated prompt sent to ElevenLabs",
    "provider": "elevenlabs"
  }
]
```

**Endpoint**: `/songs/<filename>`

- Method: `GET`

- Description: Serves a generated MP3 file by filename.

**Endpoint**: `/verify-recaptcha`

- Method:  `POST`

- Description: Passes a token to Google's reCAPTCHA server to verify a user's reCAPTCHA response.

**Request Body**
The request body should be a JSON object containing the following fields:
```json
{
	"secret": os.getenv("RECAPTCHA_SECRET_KEY"),
	"response": token,
}
```

**Response Body**
The response will be a JSON object containing the generated song url from the reCAPTCHA API.
```json
{
  "success": true|false,
  "challenge_ts": timestamp,  // timestamp of the challenge load (ISO format yyyy-MM-dd'T'HH:mm:ssZZ)
  "hostname": string,         // the hostname of the site where the reCAPTCHA was solved
  "error-codes": [...]        // optional
}
```


## Testing

Run the `pytest` testing framework:
```
$ pytest
```

## Project Structure

```plaintext
ag_backend/
├── __pycache__/       # Auto-populated bytcode files
├── .pytest_cache/     # Auto-populated pytest cache
├── app/                
│   ├── __pycache__/   # Auto-populated bytcode files
│   ├── __init__.py    # Directory marker
│   └── routes.py      # API routes and helper functions                  
├── tests/  
│   ├── __pycache__/   # Auto-populated bytcode files
│   ├── __init__.py    # Directory marker
│   ├── _test.py       # Test file
│   └── conftest.py    # Test configuration
├── venv/              # Virtual environment files        
├── .env               # Secret environment variables
├── .gitignore         # Files and directories to ignore in Git
├── LICENSE                     
├── package-lock.json  # Auto-populated during production deployment
├── README.md          # Project documentation
└── requirements.txt	 # Project dependencies
```


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Creators
- [**Shelby Willis**](#https://www.linkedin.com/in/shelby-willis-57004a234/)
- [**Sunny Muniz**](#https://www.linkedin.com/in/sunny-muniz-4838b8235/)
- [**Kit Sutliff**](#https://www.linkedin.com/in/kit-sutliff/)
- [**Anika Stephen Wilbur**](#https://www.linkedin.com/in/anika-stephen-wilbur/)