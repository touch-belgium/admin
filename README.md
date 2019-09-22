# Touch Belgium Admin

## Usage

```
$ pipenv install
$ npm i
$ npm start &
$ pipenv shell
$ python manage.py migrate website
$ python manage.py runserver
```

Environment variables required in `settings.py` have to be set
somehow, in the `activate` script, .env file, etc.

The folder `MEDIA_ROOT` (also an env variable) has to be created in
the local filesystem. FileBrowser will not create it.

**On macOS:**

`pipenv install` might fail because `psycopg2` can't be compiled
without the SSL library (which can't be found inside the virtual
env). Therefore, the command should be:

```bash
$ LDFLAGS="-L/usr/local/opt/openssl/lib" pipenv install
```

## On Dokku

### Media serving

Nginx has to be configured manually to serve user uploaded files. See
folder `nginx.conf.d`.

Use `dokku storage:mount` to provide a folder to the application. The
convention is for this folder to be
`/var/lib/dokku/data/storage/<app_name>` and the exposed dir name HAS
to be the same as `MEDIA_ROOT`. Something like:

```
dokku storage:mount touch-belgium /var/lib/dokku/data/storage/touch-belgium:/storage
```

and

```
dokku config:set touch-belgium MEDIA_ROOT=/storage
```

### Buildpack order

The `heroku-buildpack-nodejs` should be used first in order to install
all dependencies specified in `package.json`.

The assets are generated after the buildpack has finished building the
Node.js part of the application as specified in the `heroku-postbuild`
script in `package.json`. There is no need for something like
`heroku-buildpack-run` to execute some arbitrary code in between
buildpacks.

Once these assets are available, Django can collect and serve them
(WhiteNoise).

If the order of the buildpacks is switched, `heroku-buildpack-python`
is not able to collect the static assets.

## On Heroku

Heroku uses an ephemeral file system so media cannot be saved.

Nginx is also harder to configure.
