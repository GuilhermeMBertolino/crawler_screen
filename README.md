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

## Code conventions for project

* Every selector used for filtering html pages must be made with xpath
* Every message sent by the spider must be sent using the logging library
* Each spider class must be in CamelCase
* Everything else must be snake_case