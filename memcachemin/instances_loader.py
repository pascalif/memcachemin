import json
import os
# Remark : importing chef module is done lazily in the code if needed

from config import Config

__author__ = 'pascalif'


class MemcacheConfigurationLoader():
    def __init__(self):
        pass

    def load_from_chef_env(self, chef_env):
        databag_name = Config.build_chef_databag_name(chef_env)
        databag_item_id = Config.build_chef_databag_item_id(chef_env)
        return self._load_chef_databag(databag_name, databag_item_id)

    def load_from_chef_databag(self, databag_name, databag_item_id):
        return self._load_chef_databag(databag_name, databag_item_id)

    def _load_chef_databag(self, databag_name, databag_item_id):
        import chef
        # TODO : check file existence
        chef_api = chef.autoconfigure(Config.CHEF_CONFIGURATION_PATH)

        print(('Loading databag item [{:s}:{:s}]'.format(databag_name, databag_item_id)))
        databag_item = chef.DataBagItem(databag_name, databag_item_id, api=chef_api)

        if not databag_item.exists:
            raise Exception('Databag item not found')
        if 'instances' not in databag_item:
            raise Exception('Empty databag item')
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

