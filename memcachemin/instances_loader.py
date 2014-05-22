import json
import os
# Remark : importing chef module is done lazily in the code if needed

from config import Config

__author__ = 'pascalif'


class MemcacheConfigurationLoader():
    def __init__(self):
        pass

    def load_from_chef(self, chef_env):
        import chef
        chef_api = chef.autoconfigure(Config.CHEF_CONFIGURATION_PATH)

        databag_name = Config.get_chef_databag_name(chef_env)
        databag_item_id = Config.get_chef_databag_item_id(chef_env)
        print(('Loading data bag item [{:s}:{:s}]'.format(databag_name, databag_item_id)))
        databag_item = chef.DataBagItem(databag_name, databag_item_id, api=chef_api)

        if 'instances' not in databag_item:
            raise Exception('Empty data bag item')
        return databag_item['instances']

    def load_from_file(self, description_file_name):
        if not os.path.exists(description_file_name):
            raise Exception('Unable to find memcache instances description file [{:s}]. Aborting.'.format(description_file_name))

        with open(description_file_name, 'r') as fh:
            try:
                instances = json.load(fh)
            except ValueError as ve:
                raise Exception('Failed to parse a valid JSON content in file [%s]' % description_file_name)
                # Python 3 :
                #raise Exception('Failed to parse a valid JSON content in file [%s]' % configuration_file_name) from ve
        return instances

