#!/bin/bash
../../py34/bin/python make_icons.py cobl2/static/icons/
dropdb cobl2
createdb cobl2
time python cobl2/scripts/initializedb.py development.ini

