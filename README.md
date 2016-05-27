# voiceclass-server
Service for detecting sex and age category in recorded voice. [The Android client can be found here](https://github.com/habbes/voiceclass-android)

## Installation

Install and run the server in a Docker container.
- First make sure to [download and setup docker](https://docs.docker.com)
- Clone this repo: `$ git clone https://github.com/habbes/voiceclass-server`
- Navigate to project directory: `$ cd voiceclass-server`
- Create docker image: `$ docker build -t voiceclass .`

### Running the server
- Create a directory in your somewhere under your user directory where server's data files will be saved: `$ cd /Users/name/some/path && mkdir voiceclass-data`
- Run the container: `$ docker run -d -p 5000:80 -v /Users/path/to/voiceclass-data:/data voiceclass`
- The above line forwards port `5000` of the docker host to port `80` in the container. Replace `5000` with any free port on your docker host you prefer to user.

### Testing the server on Linux
- From your browser/curl visit `http://localhost:5000`
- If it works, you will get the resonse `OK`

### On Windows or Mac
- Find the IP of your docker host: `$ docker-machine ip`
- Test using the docker host IP: `http://192.168.99.100:5000`

## API
The server exposes an API for classifying voice recordings as well training the classifier. It uses **JSON** for both request and response bodies.

### Available Classes

- FemaleChild
- FemaleTeen
- FemaleAdult
- FemaleSenior
- MaleChild
- MaleTeen
- MaleAdult
- MaleSenior


### `/api/classify`
Use this to get a classification of a voice recording's.

#### Request

##### audio
- Type: **object**
- Description: Object containing the audio data and metadata used to properly decode it

##### audio.format

- Type: **string**
- Description: Audio format: currently only `pcm` is supported

###### audio.data

- Type: **string**
- Description: Base-64 encoding of the raw **PCM** data of the audio recording

###### audio.channelCount

- Type: **number**
- Description: Number of channels in the audio recording

###### audio.sampleRate

- Type: **number**
- Description: Sample rate of the recording in **Hz**

###### audio.sampleSize

- Type: **number**
- Description: Sample size in **bytes**

#### Response

##### id
- Type: **string**
- Description: Identifier for this classification. Used as a reference when providing feedback.

##### class
- Type: **string**
- Description: The class name for the identified sex and age category

### `/api/feedback`

### `/api/train`

TODO: Complete docs...


