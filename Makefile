# Installation parameters
# See comments in Makefile for available settings to change.

# Where to install
INSTDIR = /usr/local/bin
PROGRAM = raven_com

# Config file
CONFIGDIR = /etc
CONFIGFILE = raven_com.conf

# SYSTEMD configuring to autorun.
LOADERDIR = /etc/systemd/system
LOADERCONFIG = raven_com.service

# LOGGING


install:	$(PROGRAM)
		@if [ -d $(INSTDIR) ]; \
			then \
			cp $(PROGRAM) $(INSTDIR);\
			chmod a+x $(INSTDIR)/$(PROGRAM);\
			chmod og-w $(INSTDIR)/$(PROGRAM);\
			echo "Copied $(PROGRAM) to $(INSTDIR) ";\
		else \
			echo "Sorry, $(INSTDIR) does not exist";\
		fi
		@if [ -d $(CONFIGDIR) ]; \
			then \
			cp $(CONFIGFILE) $(CONFIGDIR);\
			chmod a-x $(CONFIGDIR)/$(CONFIGFILE);\
			chmod og-w $(CONFIGDIR)/$(CONFIGFILE);\
			echo "Copied config file $(CONFIGFILE) to $(CONFIGDIR) ";\
		else \
			echo "Sorry, $(LOADERDIR) does not exist";\
		fi
		@if [ -d $(LOADERDIR) ]; \
			then \
			cd utils; \
			cp $(LOADERCONFIG) $(LOADERDIR);\
			chmod a-x $(LOADERDIR)/$(LOADERCONFIG);\
			chmod og-w $(LOADERDIR)/$(LOADERCONFIG);\
			echo "Copied systemd $(LOADERCONFIG) to $(LOADERDIR) ";\
			cd ..; \
		else \
			echo "Sorry, $(LOADERDIR) does not exist";\
		fi

		@echo "Reloading systemd.";
		@systemctl daemon-reload;
#systemctl enable raven_com # Set this to start raven_com on boot.

		#@echo "Creating logfile.";
		#@mkdir -p /var/log/raven_com;
		#@touch /var/log/raven_com/new_log;

		raven_com; # Start the program after make install build finished.
		# @systemctl start raven_com; # Start as service.

uninstall:
		# @systemctl stop raven_com; # Stop the service if running.
		rm $(INSTDIR)/$(PROGRAM);
		rm $(LOADERDIR)/$(LOADERCONFIG);
		rm $(CONFIGDIR)/$(CONFIGFILE);


wrapup:
	tar -cvzf $(PROGRAM).tar.gz *;


# Special macros and options for makefiles:
# $? List of prerequisites (files the target depends on) changed more recently than the current target
# $@ Name of the current target
# $< Name of the current prerequisite
# $* Name of the current prerequisite, without any suffix
# - tells make to ignore any errors. For example, if you wanted to make a directory but wished to
#   ignore any errors, perhaps because the directory might already exist, you just precede mkdir
#   with a minus sign.
# @ tells make not to print the command to standard output before executing it. This character is
#   handy if you want to use echo to display some instructions.



