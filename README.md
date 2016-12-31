
Raven communications solutions.

### raven versions
(v0.0.1) Current development version.

Version specified in README, CHANGELOG, commit tag and raven_config.py




### Overview

#-> Data structure serialisation uses json.decode json.loads. This is slow.



### Installation
1. Git clone or download archive and extract.

2.

	$ make install


3. Run with a shell.

	$ raven_com



### Requirements:

Raven_com depends on many other packages and software.

And of course runs on Python 3.5


#### Python packages
git@github.com:weleoka/gmail_sender
git@github.com:weleoka/gmail_reciever
git@github.com:weleoka/latlon
 -> pyproj for some operations.
#git@github.com:weleoka/ravencore
https://weleoka@bitbucket.org/weleoka/ravencore.git
git@github.com:weleoka/raveneye

sudo apt-get install python3-pip
sudo pip3 install setuptools
sudo pip3 install redis
sudo pip3 install apscheduler


#### Redis database
Debian PPA makes the Redis systemd service and is easier than wget for setting up redis as a service:
sudo add-apt-repository ppa:chris-lea/redis-server
sudo apt-get update
sudo apt-get install redis-server
#sudo apt-get install redis-tools # This is done by default with this PPA.

$ wget http://download.redis.io/releases/redis-3.2.6.tar.gz
$ tar xzf redis-3.2.6.tar.gz
$ cd redis-3.2.6
$ make


### Usage

Raven_com writes to syslog.


### Current Features:

The service front end to run Raven_com. The goodies are in ravencore, raveneye etc.



### Bugs, known Issues and missing Features:

Please report an issue if one is found.

Functionality:
Specs and options:
Security:
Code, style and performance:



### Contributing

If you'd like to contribute to raven's development, start by forking the GitHub repo:

https://github.com/weleoka/raven.git

Have a look at the known issues and missing features and take a pick or find something else that needs doing.

You can search for need-doing tags "#->" in the source code.

The best way to get your changes merged is as follows:

1. Clone your fork
2. Hack away
3. If you are adding significant new functionality, document it in the README
4. Do not change the version number, I will do that on my end
5. Push the repo up to GitHub
6. Send a pull request to [weleoka/raven](https://github.com/weleoka/raven)



### Licence

GNU GENERAL PUBLIC LICENSE, Version 3


LICENSE for details.

Copyright (c) 2017 A.K. Weeks



### Sources, inspiration and notes



