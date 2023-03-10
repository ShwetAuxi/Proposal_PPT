Important: make sure to put in your openai key when testing!

To run this application:

```
venv\Script\activate
flask --debug run
```

To run in container:

```
docker build -t [image_name] .
docker run -p [localhost_port]:5000 [image_name]
```

Example:
```
docker build -t my_image .
docker run -p 5000:5000 my_image
```
Then visit localhost:5000/ to access the webapp.

TODO:
- Figure out how to run on Azure
- Figure out how to shut down webapp when running in container
