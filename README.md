# Lemmy_API_test
A test tool for the Lemmy API written in Python

https://github.com/dessalines/lemmy

As of right now this tool only runs expected behavior tests that require no auth. As further test sets are built this README will be updated.

To run:

1. Update conf.conf file with the API address under the "server" field,
2. create unique username and admin_username (and passwords if you prever) in conf.conf
3. run test.py

Logs are saved in raw_log.txt, each line corresponds to a request and response in the format of timestamp;request;response additionally an error line is logged for easy searching of errors. This is a rough logging method and will be improved in the future.

Other options in the configuration file do not currently work, but will work soon.

