#!/usr/bin/env bash
dokku postgres:unlink tb-database tb-admin
dokku postgres:stop tb-database
dokku postgres:destroy tb-database --force
dokku postgres:create tb-database
dokku postgres:link tb-database tb-admin
dokku run tb-admin python manage.py migrate
dokku run tb-admin make
