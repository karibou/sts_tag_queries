# STS query scripts

# Introduction

This is a set of scripts that facilitate the query of cases that need to be
followed by STS. They are :

* sponsor_backlog.py : List the cases that have the sts-sponsor tag
* sts_sru.py         : List the cases that have the sts-sru tag

# Organisation

Both scripts rely on the BugTasks.py module. This is where all the work
happens.

The library loops through all the active series since Trusty and collects
tasks for each bug that has the selected tag. They are then grouped together
by Bug ID.

The first letter of each serie is printed when one task is found for a bug.
The output looks like this :

>tttxxxxyyyy

# Scripts


## sponsor_backlog.py

The script's options are :

>usage: sponsor_backlog.py [-h] [-l]
>
>optional arguments:
>  -h, --help  show this help message and exit
>  -l, --long  Display series and owners

This script produces a synthetic list of cases that have the sts-sponsor tag
attached to it :

$ ./sponsor_backlog.py
>tttxxxxyyyy
>LP: #1590799 - (nfs-utils) nfs-kernel-server does not start because of dependency failure
>LP: #1645324 - (ebtables) ebtables: Lock file should be moved from /var/lib/ebtables to /run
>LP: #1668639 - (rsyslog) Add a trigger to reload rsyslog when a new configuration file is dropped in /etc/rsyslog.d

The --long output would look like this :
$ ./sponsor_backlog.py -l
tttxxxxyyyy
LP: #1590799 - (nfs-utils) nfs-kernel-server does not start because of dependency failure
  - Series to SRU : xenial yakkety
  - Owners : Rafael David Tinoco

LP: #1645324 - (ebtables) ebtables: Lock file should be moved from /var/lib/ebtables to /run
  - Series to SRU : trusty
  - Owners : Dragan S.

LP: #1668639 - (rsyslog) Add a trigger to reload rsyslog when a new configuration file is dropped in /etc/rsyslog.d
  - Series to SRU : xenial yakkety trusty
  - Owners : None

## sts_sru.py

The script's options are :

>usage: sts_sru.py [-h] [-l]
>
>optional arguments:
>  -h, --help  show this help message and exit
>  -l, --long  Display series and owners

This script produces a synthetic list of cases that have the sts-sru tag
attached to it :

$ ./sts_sru.py
ttttttttttxxxxxxxyyyyyy
>LP: #1356211 - (sosreport) cannot collect rotated syslog.1
>LP: #1515278 - (oslo.messaging) [SRU] rabbit queues should expire when unused
>LP: #1566508 - (sssd) autofs races with sssd on startup
>LP: #1590799 - (nfs-utils) nfs-kernel-server does not start because of dependency failure

The --long output would look like this :
$ ./sts_sru.py -l
>ttttttttttxxxxxxxyyyyyy
>LP: #1356211 - (sosreport) cannot collect rotated syslog.1
>  - Series to SRU : trusty
>  - Owners : Louis Bouchard
>
>LP: #1515278 - (oslo.messaging) [SRU] rabbit queues should expire when unused
>  - Series to SRU : trusty
>  - Verification : verification-done verification-liberty-done
>  - Owners : Jorge Niedbalski
>
>LP: #1566508 - (sssd) autofs races with sssd on startup
>  - Series to SRU : xenial trusty yakkety
>  - Verification : verification-needed
>  - Owners : Victor Tapia
>
>LP: #1590799 - (nfs-utils) nfs-kernel-server does not start because of dependency failure
>  - Series to SRU : xenial yakkety
>  - Owners : Rafael David Tinoco
>
>#info SRU are pending for : oslo.messaging, nfs-utils, sssd, sosreport

The line starting with #info is used for the Server Engineering and will only appear
when --long is used.
