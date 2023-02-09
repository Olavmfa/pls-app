# Personal number Lookup System

The Personal number Lookup System (pls) is a simple service to access a fake personal number register and access information concerning specific personal numbers.
The system runs as a REST-API with multiple endpoints.
Follow the set up steps below to run the application using docker

## Set up
- Pull the image using ***docker pull olavfp/pls-rest-api***.
- Run the api using ***docker run -d -p 8000:5000 --name pls-rest-server olavfp/pls-rest-api*** (Notice the optional --name for the container to run the image)
- Either
 - - Open a terminal in the container using ***docker exec -it pls-rest-server bash*** (Replace container name if you chose a different name)
- - Start using the cli typing ***pls -h***
- Or
- - Open a terminal running locally on your computer (requires python and python's requests module installed)
- - Start using the cli typing ***python cli.py -h***

## Testing
To run a test script testing the different endpoints, simply type ***docker exec olavfp/pls-rest-server python testing.py*** in a local shell, or ***python testing.py*** in an interactive shell within the container.

## Finishing
- After using the api, stop the container typing ***docker stop pls-rest-server***
