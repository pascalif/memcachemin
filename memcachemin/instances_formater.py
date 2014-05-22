__author__ = 'pascalif'

import time
from config import Config


class ConsoleFormater():
    def __init__(self):
        pass

    def dump_clusters(self, clusters):
        limiters = 70
        print('')
        print('Clusters usage :')
        print('='*limiters)
        print('| Owner      | Usage           | Cu | NbSlots | SlotSize | TotalSize |')
        print('='*limiters)
        for hashkey in sorted(clusters.iterkeys()):
            sc = clusters[hashkey]
            size_class = sc['size_class']
            subcluster_size = len(sc['instances']) * Config.get_size_for_class(size_class)
            print('| {owner:10s} | {usage:15s} | {culture:2s} | {nbslots:7d} | {slotsize:5.1f} Gb | '
                  '{totsize:6.1f} Gb |'.format(
                  owner=sc['owner'],
                  usage=sc['usage'],
                  culture=sc['culture'],
                  nbslots=len(sc['instances']),
                  slotsize=Config.get_size_for_class(size_class),
                  totsize=subcluster_size
                  ))

    def dump_instances(self, clusters):
        limiters = 185
        print('')
        print('Instances details :')
        print('='*limiters)
        print('| ## | Owner      | Usage           | Cu | Ip              | Port  || StartTime           | Con | TotlCon '
              '| Memory used                    | NbGet      | NbSet      | HitR | Evictions |')
        print('='*limiters)
        ix = 1
        for hashkey in sorted(clusters.iterkeys()):
            sc = clusters[hashkey]
            for instance_desc in sc['instances']:
                stats = instance_desc['_stats']

                # [(u'10.208.160.128:11211 (1)', {'auth_cmds': '0', 'reclaimed': '0', 'pid': '1005', 'cas_hits': '0',
                # 'uptime': '6048', 'delete_misses': '0', 'listen_disabled_num': '0', 'cas_misses': '0',
                # 'decr_hits': '0', 'incr_hits': '0', 'version': '1.4.5', 'limit_maxbytes': '1205862400',
                # 'bytes_written': '0', 'incr_misses': '0', 'accepting_conns': '1', 'rusage_system': '0.000000',
                # 'total_items': '0', 'cmd_get': '0', 'curr_connections': '10', 'threads': '4',
                # 'total_connections': '11', 'cmd_set': '0', 'curr_items': '0', 'conn_yields': '0',
                # 'get_misses': '0', 'bytes_read': '7', 'cas_badval': '0', 'cmd_flush': '0', 'evictions': '0',
                # 'bytes': '0', 'connection_structures': '11', 'auth_errors': '0', 'rusage_user': '0.192012',
                # 'time': '1393429933', 'delete_hits': '0', 'pointer_size': '64', 'decr_misses': '0', 'get_hits': '0'})]
                # Rem : time is date of the stats, not the start time !

                static_data = '| {index:02d} | {owner:10s} | {usage:15s} | {culture:2s} | {ip:15s} | {port:5d} |'.\
                    format(
                        index=ix,
                        owner=instance_desc['owner'],
                        usage=instance_desc['usage'],
                        culture=instance_desc['culture'],
                        ip=instance_desc['ip'],
                        port=instance_desc['port']
                    )
                dynamic_data = ' N/A'

                hit_ratio = 0
                if stats:
                    start_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                               time.localtime(int(stats['time'])-int(stats['uptime'])))
                    available_size = int(stats['limit_maxbytes'])
                    used_size = int(stats['bytes'])
                    used_size_percent = int(100*used_size/available_size)
                    evictions = int(stats['evictions'])
                    current_connections = int(stats['curr_connections'])
                    total_connections = int(stats['total_connections'])
                    nb_set = int(stats['cmd_set'])
                    nb_get = int(stats['cmd_get'])
                    if int(stats['get_hits'])+int(stats['get_misses']) > 0:
                        hit_ratio = int(100*int(stats['get_hits']) / (int(stats['get_hits'])+int(stats['get_misses'])))

                    dynamic_data = '| {time:19s} | {cc:3d} | {tc:7d} | {us:10d} / {av_size:10d} : {usp:02d} % | ' \
                                   '{ng:10d} | {ns:10d} | {hr:02d} % | {ev:9d} |'.\
                        format(
                            time=start_time,
                            cc=current_connections,
                            tc=total_connections,
                            us=used_size,
                            av_size=available_size,
                            usp=used_size_percent,
                            ng=nb_get,
                            ns=nb_set,
                            hr=hit_ratio,
                            ev=evictions
                        )

                print('%s%s' % (static_data, dynamic_data))
                ix += 1


class TwikiFormater():
    def __init__(self):
        pass

    def dump_clusters(self, clusters):
        raise Exception('Not implemented')

    def dump_instances(self, clusters):
        raise Exception('Not implemented')


class HtmlFormater():
    def __init__(self):
        pass

    def dump_clusters(self, clusters):
        raise Exception('Not implemented')

    def dump_instances(self, clusters):
        raise Exception('Not implemented')
