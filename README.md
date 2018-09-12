# djangoconus2018-drf-talk

[![Build Status](https://travis-ci.org/drewbrew/djangoconus2018-drf-talk.svg?branch=master)](https://travis-ci.org/drewbrew/djangoconus2018-drf-talk)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Example code for my DRF talk at DjangoCon US 2018. Check out the project's [documentation](http://drewbrew.github.io/djangoconus2018-drf-talk/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)
- [Travis CLI](http://blog.travis-ci.com/2013-01-14-new-client/)

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```
