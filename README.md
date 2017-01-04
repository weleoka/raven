
Raven communications solutions.



### raven versions

v0.1beta Current development version.

Version specified in README, CHANGELOG, commit tag and raven_config.py




### Overview

This is the front end for ravencore where all the guts of the application are. ravencore is currently a private repo.

What whe have here are general information concerning Raven_com and its functinality.






### Installation
Make sure all the requirements are satisfied. See requirements header below. Here there is further talk of installing for production or development environments. We begin:

The sys.path can be appended with a relative or absolute path to the "vendor" folder.
This is currently done in ./raven_com but is really only for development purposes.

However, if raven_com is run as a service (systemd/ init.d or other) then the home folder 
will not necessarily have been mounted. The safer way is to install the dependencies in 

/usr/local/lib/python3.5/dist-packages or /usr/lib/python3/dist-packages

First of all the dependencies which can't be installed with a standard installer are best fetched by cloning the relevant repositories. Easy is simply go to the raven/vendor folder and clone the whole bunch of dependencies into there. The ./raven_com executable has some commented lines which will append a relative or absolute path to python's sys.path (where it looks for packages) - like this it's just to get cracking on the development. 

The cloned repositories in raven/vendor can be manually copied to 

    /usr/local/lib/python3.5/dist-packages or /usr/lib/python3/dist-packages

Alternatively 
    
    $ make cpdeps

Should run through and copy the relevant repositories to the above paths.! Not super neat but easy.


To summarise:

1. Git clone or download archive and extract.

3. Go to vendor folder and git clone the dependencies listed under the requirements header.

2. Look in the Makefile for details.

    $ make install
    $ make cpdeps


3. Run with a shell, or if set in makefile it will be a system service.

    $ raven_com
    $ systemctl status raven_com

4. Monitor log files if running as a system service:

systemd journal is now the standard logging device for most distros.

    $ journalctl -e -u raven_com

(-u selects raven_com unit. -e Jumps to the end.)


### Requirements:

Raven_com depends on some other software.

It does require Python 3.5 for example. 

Some requirements are easily satisfied with a package manager like pip and apt-get. Unfortunately not all the dependencies can. Some require manual downloading and installing. See below for further details.




#### Python packages as repos
These packages are needed but do not have installers.

They will manually have to be installed to the correct dependency directory (raven/vendor).


    git clone https://github.com/weleoka/raven.git
    git clone https://github.com/weleoka/raveneye.git
    git clone https://github.com/weleoka/gmail_sender.git
    git clone https://github.com/weleoka/gmail_reciever.git
    git clone https://github.com/weleoka/latlon.git
    git clone https://github.com/weleoka/ravencore.git # Private repo moved to bitbucket

    # latlon uses pyproj (python projection) for some functions.
    # (sudo pip3 install pyproj) However currently pyproj is not installing,
    
    git clone from https://github.com/jswhit/pyproj


#### Python packages on PIP3
These are well maintained and install without troubles:
    $ apt-get install python3-pip (if you don't have it already)
    $ pip3 install setuptools
    $ pip3 install redis
    $ pip3 install apscheduler

#### Redis database
Debian PPA makes the Redis systemd service and is easier than wget for setting up redis as a service:
    $ add-apt-repository ppa:chris-lea/redis-server
    $ apt-get update
    $ apt-get install redis-server
    #apt-get install redis-tools # This is done by default with this PPA.

If you still prefer to wget and manually write a redis-server.service file then:
    $ wget http://download.redis.io/releases/redis-3.2.6.tar.gz
    $ tar xzf redis-3.2.6.tar.gz
    $ cd redis-3.2.6
    $ make



### Usage

Start up and hope syslog isn't flooded with problems!

The service can be stopped and restarted and jobs will not be lost, or doubled up.

To modify the log output change debug flags and basic_log settings in ravencore.main.config

Some modules are 'noisy' and can have custom loging levels set.

Be carful with the resetdb parameter in config! =)





### Current Features:

This is the service front end to raven_com. The goodies are in ravencore, raveneye etc.



### Bugs, known Issues and missing Features:

Please report an issue if one is found.

Functionality:
Specs and options:
Security:
Code, style and performance:



#### DO LIST

Anywhere in the code where the job tag (#->) is found =)


Here are some of the low-priority jobs. These will mostly be found in ravencore modules,
but this is a useful overview for jobs that affect the raven_com service.

-> Data structure serialisation uses json.decode json.loads. This is slow.
-> Job.merge_dicts should be able to omit certain dict keys which are trivial. The raven job does not need to know the underlying service parameters.
-> Make system users (user1) parameters global to save on db reads.
-> Forward an email with attachment without downloading attachment.
-> Job_router. Newsletter. Find the raven_user_service_id.
-> Litemail identification in Mail_router assumes all to be for user2.
-> Newsletter Mail_out() objects should be a different dbitem. so that the system does not accidentally send a load of blog mail.
-> The Job_router() and Mail_router() in ravencore/coms/router.py both have alot of logic in __init__(). The usage is flawed and should be moved out to methods.




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



