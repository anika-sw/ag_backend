# AutomatedGroove Backend

Streaming services automatically scan audio for copyrighted content, and mute or block uploads featuring this content. This makes it difficult for content creators to find appropriate background music. Our app, AutomatedGroove, automatically generates royalty-free music for content creators, saving them time and money. 

Find the frontend repository here: [AutomatedGroove Frontend](https://github.com/KitSutliff/automated_groove_frontend)


## Table of Contents

[Installation](#installation)
[Configuration](#configuration)
[Implementation](#implementation)
[API Documentation](#api-documentation)
[Testing](#testing)
[License](#license)
[Contact](#contact)


## Installation

1. Clone the repository to your local machine:
	```sh
	$ git clone https://github.com/KitSutliff/automated_groove_backend.git
	```
2. Navigate into the repository:
	```sh
	$ cd automated_groove_backend
	```
3. Create a virtual environment:
	```sh
	$ python -m venv venv
	```
4. Activate the virtual environment:
	```sh
	$ source venv/bin/activate     # On Windows use `venv\Scripts\activate`
	```
5. Install dependencies:
	```sh
	$ pip install -r requirements.txt
	```


## Configuration

Set the following environment variables in a `.env` file:

-  `OPENAI_API_KEY`
-  `MUSICFY_API_KEY`

>_Note: You need to obtain your own API keys from both **OpenAI** and **Musicfy AI** to use in this project._


## Implementation

1. Run the `flask` development server:
	```sh
	$ flask run
	```
2. To access the application locally, open a web browser and go to [http://localhost:5000](http://localhost:5000).


## API Documentation 

### Endpoint: `/create_song_name`

**Method:**  `POST`
**Description:** Generates a song name based on the provided genre, mood, and tempo.

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

### Endpoint: `/create_song`

**Method:**  `POST`
**Description:** Generates a song based on the provided genre, mood, and tempo by calling the Musicfy API.

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
The response will be a JSON object containing the generated song url from the Musicfy API.
```json
[
	{
		"file_url": “https:/example-url”,
		"type": "music"
	}
]
```


## Testing

Run the `pytest` testing framework:
```
$ pytest
```

  
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Creators
- [**Shelby Willis**](#https://www.linkedin.com/in/shelby-willis-57004a234/)
- [**Sunny Muniz**](#https://www.linkedin.com/in/sunny-muniz-4838b8235/)
- [**Kit Sutliff**](#https://www.linkedin.com/in/kit-sutliff/)
- [**Anika Stephen Wilbur**](#https://www.linkedin.com/in/anika-stephen-wilbur/)