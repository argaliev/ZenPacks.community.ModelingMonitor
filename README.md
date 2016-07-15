======================================
ZenPacks.community.ModelingMonitor
======================================


Description
===========

This ZenPack provides datasource ModelingMonitorDataSource to get information about modeling status.
Zenpack check last modelling time of device and number of component classes, that must be presented in device.
How it can be usefull:
 - When you applied several modeler on device, and some of them wasn't create expected component classes, this will trigger an event.
   I my case, there was snmp plugin, that returns no data and failed events, until special vendor drivers was installed.
 - When, for some reason, modelling was performing later than given time ago(in days)

Requirements & Dependencies
===========================

    * Zenoss Versions Supported: > 4.0
    * External Dependencies:
    * ZenPack Dependencies:
    * Installation Notes: zenhub and zopectl restart after installing this ZenPack.
    * Configuration:

Installation
============
Normal Installation (packaged egg)
----------------------------------
Copy the downloaded .egg to your Zenoss server and run the following commands as the zenoss
user::

   * zenpack --install <package.egg>
   * zenhub restart
   * zopectl restart

Developer Installation (link mode)
----------------------------------
If you wish to further develop and possibly contribute back to this
ZenPack you should clone the git repository, then install the ZenPack in
developer mode::

   * zenpack --link --install <package>
   * zenhub restart
   * zopectl restart

Configuration
=============

Tested with Zenoss 4.2.5

zProperties
-----------
- **zCompClassCount** - number of class components that expected to appear in device
- **zExpiryDaysPast** - number of days when last modeling time become outdated
- **zModelingMonitorInterval** - time interval to perform monitor
 
Monitoring Templates
-----------
- **/Devices/Server/rrdTemplates/ModelingMonitor**

Event Classes
-----------
- **/Status/Modeling**
- **/Status/Modeling/ComponentMismatch**
- **/Status/Modeling/ModelTimeExpired**

Screenshots
===========
* |ModelingMonitorEdit|
* |ModelingMonitorEvent|