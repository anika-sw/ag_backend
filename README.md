# automated_groove_backend
Streaming services automatically scan audio for copyrighted content, and mutes or blocks uploads featuring this content. This makes it difficult for content creators to find appropriate background music. Our app automatically generates royalty-free music for content creators saving them time and money. 


## Table of Contents

- [Installation](#installation)
- Clone the repository to local machine
- git clone https://github.com/yourusername/yourproject.git
- Navigate into the repository
- cd yourproject
- Create a virtual environment
- python -m venv venv
- Activate the virtual environment
- source venv/bin/activate  # On Windows use `venv\Scripts\activate`
- Install dependencies
- pip install -r requirements.txt
  
- [Configuration](#configuration)
- Environment variables
- OPENAI_API_KEY
- MUSICFY_API_KEY

- [Usage](#usage)
- Run the development server
- flask run
- Access the application
- Open a web browser and go to http://localhost:5000

- [API Documentation](#api-documentation)
- ### Endpoint: `/create_song_name`

- **Method:** `POST`
- **Description:** Generates a song name based on the provided genre, mood, and tempo.

#### Request Body
The request body should be a JSON object containing the following fields:
```json
{
    "genre": ["pop"],
    "mood": ["happy"],
    "tempo": ["medium"]
}
```

#### Response Body
The response will be a JSON object containing the generated song name.
{"song_name”} type string

### Endpoint: `/create_song`

- **Method:** `POST`
- **Description:** Generates a song based on the provided genre, mood, and tempo by calling the Musicfy API.

#### Request Body
The request body should be a JSON object containing the following fields:

```json
{
    "genre": ["pop"],
    "mood": ["happy"],
    "tempo": ["medium"]
}
```

#### Response Body
The response will be a JSON object containing the generated song url link from the Musicfy API.

```json [ { "file_url": “https:/exampleurl”, "type": "music" } ]```

- [Testing](#testing)
- **Run pytest:**
- ```sh pytest ```


- [License](#license)
- This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
- 
- [Contact](#contact)
- The four of us