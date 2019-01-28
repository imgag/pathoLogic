metabiom
--------

This repo contains all the files for `metabiom`.

The [swagger definition](http://swagger.io/) can be found [here as well](./swagger.yaml).
Vuetify is used with `vue-cli`. See more in the [frontend folder](./frontend/README.md).

### Mocking REST API

You can use [prism](https://github.com/stoplightio/prism) like this
```
docker run -v $PWD:/code/ -p 4010:4010 -it stoplight/prism mock --spec /code/swagger.yaml
```
