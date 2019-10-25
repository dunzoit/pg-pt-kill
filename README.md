# pg-pt-kill

Long running query killer for PostgreSQL DB

**Inspration:** https://www.percona.com/doc/percona-toolkit/LATEST/pt-kill.html

## Setup 
```
git clone git@github.com:dunzoit/pg-pt-kill.git
cd pg-pt-kill
pip3 install virtualenv
virtualenv venv
. venv/bin/activate
pip install -r requirements.lock
cp settings.py.sample settings.py
```

Modify `settings.py` to update the connection credentials for your database

## Usage
Performs a dry run. Connects to the database and logs all the queries that met threshold criteria.
```
pt-kill.py -c dbserver
```
```
pt-kill.py -c dbserver -r dryrun
```

Terminates all slow queries currently running that meet the threshold criteria
```
pt-kill.py -c dbserver -r kill
```

If the db config is not provided, it uses `default` config
```
pt-kill.py -r kill
```