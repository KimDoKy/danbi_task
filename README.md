# 단비교육 백엔드

## Run Dev Server

```bash
# 1. run docker
$ docker-compose -f docker-compose-dev.yml up -d

# 2. exec container
$ docker exec -it backend_service bash

# 3. migrate
$ python3 manage.py migrate
```

## Run Test

```bash
$ python3 manage.py test
```
