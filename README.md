# IEEE-USJ
An interactive Web App for the Management of the IEEE Student Branch USJ

## To Install and Modify
1. Using PostgresSQL, create a database called `ieee` (no caps)
2. Copy the `config_default.cfg` file, and rename the copy to `config_dev.cfg`. It will be, by default, ignored by git.
3. Change the `SQLALCHEMY_DATABASE_URI` value by replacing `username:password` by your username and password for the database.

Continue working normally