# Web crawler for screen project

To install all dependencies of the project, run the following command:

```
    pip install requirements.txt
```

To run the crawler for all vendor websites, run the crawl bash script

```
    ./crawl.sh
```

If you want to run only a specific crawler, try to run the script with a parameter, just like the example below:

```
    ./crawl.sh dlink
```

# Run crawler on Docker container

If you are not using linux, you will probably need to run the crawler in a docker container, to do so, you must have Docker and docker-compose installed in your machine, you can get them from the [official website](https://www.docker.com/get-started/). Once you have docker installed you can build the image running the following code from the crawler folder:

```
    docker-compose build
```

To run the image, just run:

```
    docker-compose --rm up
```

Once you are done, the container will be deleted.

## Code conventions for project

* Every selector used for filtering html pages must be made with xpath
* Every message sent by the spider must be sent using the logging library
* Each spider class must be in CamelCase
* Everything else must be snake_case