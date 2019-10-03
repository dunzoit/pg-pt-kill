# pg-pt-kill

Long running query killer for PostgreSQL DB

**Inspration:** https://www.percona.com/doc/percona-toolkit/LATEST/pt-kill.html

# Setup 
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

# Usage
```
python pt-kill.py -d server1
```
**NOTE:** Currently does not kill any queries. Only logs the long running queries to a log file

## TODO
- [ ] Add option to perform dryruns
- [ ] Add option to only log and not kill the queries
- [ ] Add the kill statement to kill the queries
