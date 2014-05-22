import memcache
import time
from memcachemin.instances_formater import ConsoleFormater, TwikiFormater, HtmlFormater

__author__ = 'pascalif'


class MemcacheClusterManager():
    def __init__(self, instances, verbose=False):
        self.instances = instances
        self.connected = False
        self.verbose = verbose

        self._connect_to_memcache_instances()

    def _connect_to_memcache_instances(self):
        if self.verbose:
            print('Connecting to instances...')

        for instance_desc in self.instances:
            mc = memcache.Client([instance_desc['ip']+':'+str(instance_desc['port'])])
            instance_desc['_connection'] = mc
        self.connected = True

    def inject_traffic(self):
        if self.verbose:
            print('Injecting traffic...')

        base_prefix = '__injected_data_'
        for instance_desc in self.instances:
            mc = instance_desc['_connection']
            mc.set(base_prefix+'key1', 'a'*2500, 120)
            mc.get(base_prefix+'key1')
            mc.get(base_prefix+'key2')
            mc.get(base_prefix+'key3')

    @staticmethod
    def reorganize_by_cluster(instances):
        # Reorganize instances by usage
        clusters = {}
        for instance_desc in instances:
            hashkey = '%s%s%s' % (instance_desc['owner'], instance_desc['usage'], instance_desc['culture'])
            if hashkey not in clusters:
                clusters[hashkey] = {'instances': [],
                                     'owner': instance_desc['owner'],
                                     'usage': instance_desc['usage'],
                                     'culture': instance_desc['culture'],
                                     'size_class': instance_desc['size_class']
                                     }
            clusters[hashkey]['instances'].append(instance_desc)
        return clusters

    def dump_clusters(self, formatter_name='console'):
        clusters = self.reorganize_by_cluster(self.instances)

        formatters = {'console': ConsoleFormater, 'twiki': TwikiFormater, 'html': HtmlFormater}
        if formatter_name not in formatters:
            raise Exception('Unknown formatter [%s]' % formatter_name)

        formatters[formatter_name]().dump_clusters(clusters)

    def dump_instances(self, formatter_name='console'):
        clusters = self.reorganize_by_cluster(self.instances)

        formatters = {'console': ConsoleFormater, 'twiki': TwikiFormater}
        if formatter_name not in formatters:
            raise Exception('Unknown formatter [%s]' % formatter_name)

        for instance_desc in self.instances:
            mc = instance_desc['_connection']
            stats_container = mc.get_stats()
            try:
                mc_instance_endpoint, stats = stats_container[0]
                instance_desc['_stats'] = stats
            except IndexError:
                # Probably the lib couldn't connect to the endpoint
                instance_desc['_stats'] = None

        formatters[formatter_name]().dump_instances(clusters)

    def reset_stats(self):
        if self.verbose:
            print('Resetting partial instances stats...')

        for instance_desc in self.instances:
            try:
                instance_desc['_connection'].get_stats('reset')
            except IndexError:
                # The memcache library is buggggged
                pass

    def flush_all_data(self, sleep_duration=0):
        if self.verbose:
            print('Flushing data with an anti-flood sleep security of %ss...' % sleep_duration)

        for instance_desc in self.instances:
            instance_desc['_connection'].flush_all()
            if self.verbose:
                print('   - %s:%s done' % (instance_desc['ip'], instance_desc['port']))
            time.sleep(sleep_duration)

        if self.verbose:
            print('Flush done')
            print("Remark : results won't be visible in memory footprint when doing STATS.")
