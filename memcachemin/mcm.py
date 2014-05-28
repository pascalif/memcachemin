#!/usr/bin/python

import argparse
import traceback
from memcachemin.instances_loader import MemcacheConfigurationLoader
from memcachemin.instances_filter import MemcacheInstancesFilter
from memcachemin.memcache_manager import MemcacheClusterManager

ACTION_STATS_DUMP = 'stats'
ACTION_STATS_RESET = 'reset'
ACTION_DATA_FLUSH = 'flush-data'


def parse_args():
    desc = 'View & manage memcache instances'

    parser = argparse.ArgumentParser(description=desc, add_help=True,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    #parser.add_argument('--format', dest="format", required=False, action='store', default='console',
    #                    help='Format of output', choices=['console', 'twiki', 'html'])
    parser.add_argument('--instances-file', dest="instances_file", required=False,
                        help="Configuration file describing memcache instances")
    parser.add_argument('--culture', required=False, help='Filter instances by culture')
    parser.add_argument('--owner', required=False, help='Filter instances by owner')
    parser.add_argument('--ip', required=False, help='Filter instances by IP')
    parser.add_argument('--port', required=False, help='Filter instances by memcache port')
    parser.add_argument('--usage', required=False, help='Filter instances by usage')
    parser.add_argument('-v', '--verbose', required=False, action='store_true', help='More stuff on teh screen')
    parser.add_argument('-a', '--action', required=False, default=ACTION_STATS_DUMP, help='Action to do',
                        choices=[ACTION_STATS_DUMP, ACTION_DATA_FLUSH])
    parser.add_argument('--stats-reset', required=False, default=False, action='store_true',
                        help='Reset some stats on remote servers before getting statuses or after flushing data')
    parser.add_argument('--stats-inject', required=False, default=False, action='store_true',
                        help='Inject some limited useless data to activate stats')
    parser.add_argument('--flush-sleep', default=10, required=False,
                        help='Sleep delay in seconds between two instances flush')
    parser.add_argument('--chef-env', dest="chef_env", required=False,
                        help="Chef environment where to retrieve memcache instances. "
                             "If specified, this parameter overrides --instances-file")
    parser.add_argument('--chef-databag', dest="chef_databag_name", required=False,
                        help="Chef databag filename containing memcache instances description."
                             "If specified, this parameter overrides both --instances-file and --chef-env")
    parser.add_argument('--chef-item', dest="chef_databag_item_id", required=False,
                        help="Chef databag item id containing memcache instances description."
                             "If specified, this parameter overrides both --instances-file and --chef-env")

    args = parser.parse_args()
    args.format = 'console'
    return args


def main():
    args = parse_args()
    if args.chef_env is not None:
        all_instances = MemcacheConfigurationLoader().load_from_chef_env(args.chef_env)
    elif args.chef_databag_name is not None:
        if args.chef_databag_item_id is None:
            raise Exception('Please provide both a Chef databag name and item id.')
        all_instances = MemcacheConfigurationLoader().load_from_chef_databag(args.chef_databag_name,
                                                                             args.chef_databag_item_id)
    elif args.instances_file is None:
        raise Exception('Please provide a path to the file describing memcache instances or '
                        'specify a Chef environment for real-time loading.')
    else:
        all_instances = MemcacheConfigurationLoader().load_from_file(args.instances_file)

    instances = MemcacheInstancesFilter().filter(instances=all_instances,
                                                 culture=args.culture,
                                                 owner=args.owner,
                                                 ip=args.ip,
                                                 port=args.port,
                                                 usage=args.usage)
    if len(instances) == 0:
        raise Exception('No memcache instances were selected')

    mc = MemcacheClusterManager(instances, verbose=args.verbose)

    if args.action == ACTION_STATS_DUMP:
        if args.stats_reset:
            mc.reset_stats()
        if args.stats_inject:
            mc.inject_traffic()
        mc.dump_clusters(args.format)
        mc.dump_instances(args.format)

    elif args.action == ACTION_DATA_FLUSH:
        mc.flush_all_data(int(args.flush_sleep))
        if args.stats_reset:
            mc.reset_stats()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('============================')
        print('FATAL: ')
        traceback.print_exc()
        print('============================')

