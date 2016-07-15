__doc__="""info.py

Adapter between IModelingMonitorDataSourceInfo and ModelingMonitorDataSource.

"""
from zope.component import adapts
from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import RRDDataSourceInfo

from ZenPacks.community.ModelingMonitor import interfaces
from ZenPacks.community.ModelingMonitor.datasources import ModelingMonitorDataSource

class ModelingMonitorDataSourceInfo(RRDDataSourceInfo):

    implements(interfaces.IModelingMonitorDataSourceInfo)
    adapts(ModelingMonitorDataSource)

    CompClassCount = ProxyProperty('CompClassCount')
    ExpiryDaysPast = ProxyProperty('ExpiryDaysPast')

    cycletime = ProxyProperty('cycletime')

    testable = False

