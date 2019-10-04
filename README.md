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
Performs dryrun and checks the connections issues if any and logs slow queries currently running
```
python pt-kill.py -c server1 -d
```

Terminates all slow queries currently running that meet the threshold criteria
```
python pt-kill.py -c server1
```

## TODO
- [ ] Add option to only log and not kill the queries
- [ ] Add the kill statement to kill the queries
