from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource \
    import PythonDataSource, PythonDataSourcePlugin

import datetime
from dateutil import parser
from twisted.internet import defer

import logging
log = logging.getLogger('zen.ModelingMonitor')

class ModelingMonitorDataSource(PythonDataSource):
    """ Monitoring of modeling status """

    ZENPACKID = 'ZenPacks.community.ModelingMonitor'

    # Friendly name for your data source type in the drop-down selection.
    sourcetypes = ('ModelingMonitor',)
    sourcetype = sourcetypes[0]

    component = '${here/id}'
    eventClass = '/Status/Modeling'
    cycletime = '${dev/zModelingMonitorInterval}'

    # Custom fields in the datasource
    CompClassCount = '${dev/zCompClassCount}'
    ExpiryDaysPast = '${dev/zExpiryDaysPast}'

    _properties = PythonDataSource._properties + (
        {'id': 'CompClassCount', 'type': 'string', 'mode': 'w'},
        {'id': 'ExpiryDaysPast', 'type': 'string', 'mode': 'w'},
    )

    # Collection plugin for this type.
    plugin_classname = ZENPACKID + '.datasources.ModelingMonitorDataSource.ModelingMonitorPlugin'

class ModelingMonitorPlugin(PythonDataSourcePlugin):

    proxy_attributes = (
        'zCompClassCount',
        'zExpiryDaysPast',
        )

    @classmethod
    def config_key(cls, datasource, context):
        return (
            context.device().id,
            datasource.getCycleTime(context),
            datasource.rrdTemplate().id,
            datasource.id,
            datasource.plugin_classname,
            )

    @classmethod
    def params(cls, datasource, context):
        params = {}
        params['lastModelingDate'] = parser.parse(str(context.getSnmpLastCollection().Date()))

        comp_classes=set()
        for comp in context.getDeviceComponents():
            comp_classes.add(comp.meta_type)
        params['componentClassCount'] = len(comp_classes)

        log.debug(' params is %s \n' % (params))
        return params

    def collect(self, config):
        ds0 = config.datasources[0]
        data = self.new_data()

        if datetime.datetime.now() - datetime.timedelta(days=ds0.zExpiryDaysPast) > ds0.params['lastModelingDate']:
            data['events'].append({
                        'device': config.id,
                        'summary': "Monitoring data are outdated: last device component collection was performed later than {0} day ago".format(ds0.zExpiryDaysPast),
                        'severity': ds0.severity,
                        'eventClass' : '/Status/Modeling/ModelTimeExpired',
                        'eventKey': 'last_model_time_status',
                        })
        else:
            data['events'].append({
                        'device': config.id,
                        'summary': "Monitoring data are actual",
                        'severity': 0,
                        'eventClass' : '/Status/Modeling/ModelTimeExpired',
                        'eventKey': 'last_model_time_status',
                        })

        if ds0.params['componentClassCount'] < ds0.zCompClassCount:
            data['events'].append({
                        'device': config.id,
                        'summary': "Monitoring data lost: {0} of {1} component classes presented".format(ds0.params['componentClassCount'], ds0.zCompClassCount),
                        'severity': ds0.severity,
                        'eventClass' : '/Status/Modeling/ComponentMismatch',
                        'eventKey': 'component_model_status',
                        })
        else:
            data['events'].append({
                        'device': config.id,
                        'summary': "Monitoring class components fully presented",
                        'severity': 0,
                        'eventClass' : '/Status/Modeling/ComponentMismatch',
                        'eventKey': 'component_model_status',
                        })
        dd = defer.Deferred()
        dd.callback(data)
        log.debug( 'data is %s ' % (data))
        return dd