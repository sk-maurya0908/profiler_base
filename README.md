# Profiler_base
An automated resume generator that creates resume of IIT Bombay format as a pdf file.

## Setting the `postgresql`
### Installation
`sudo apt update`
`sudo apt install postgresql postgresql-contrib`

### Initialize the Database Cluster:
`sudo pg_createcluster <version> main`
replace `<version>` with the current version of `sql`.

### Start and Enable PostgreSQL:
`sudo systemctl start postgresql`
`sudo systemctl enable postgresql`

### Set a Password for the PostgreSQL Superuser:
`sudo -i -u postgres`
`psql`
`ALTER USER postgres PASSWORD 'your_password';`

### Access the postgresql via command line 
`sudo -u postgres psql`

### Creating new users
`CREATE USER <username> WITH PASSWORD <password>;`
`ALTER ROLE <username> SET client_encoding TO 'utf8';`
`ALTER ROLE <username> SET default_transaction_isolation TO 'read committed';`
`ALTER ROLE <username> SET timezone TO 'UTC';`

### Create and configure Database 
`createdb <database name>;`

`\c <database name>;`

`GRANT ALL PRIVILEGES ON DATABASE <database name> TO <username>;`

### Create and configure table
`CREATE TABLE <table name> (<column name> <type> <etc>,<other column names>);`

`GRANT SELECT, INSERT ON TABLE <table name> TO <username>;`

`GRANT USAGE, SELECT ON SEQUENCE <sequence_name> TO <username>;`
