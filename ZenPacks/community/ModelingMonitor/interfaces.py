__doc__="""interfaces.py

Interface that creates the web form for ModelingMonitorDataSource.

"""

from Products.Zuul.interfaces import IRRDDataSourceInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t

class IModelingMonitorDataSourceInfo(IRRDDataSourceInfo):

    CompClassCount = schema.TextLine(title=_t(u'Required Component Class Count'),)
    ExpiryDaysPast = schema.TextLine(title=_t(u'Number of days when outdated'),)

    cycletime = schema.TextLine(title=_t(u'Cycle Time (seconds)'))
