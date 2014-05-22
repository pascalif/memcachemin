
class Config():
    # If you want to download your instances from a Chef databag, set correct value for this variable
    CHEF_CONFIGURATION_PATH = '/home/ubuntu/.chef'

    SIZE_CLASS_LABEL_BIG = 'big'
    SIZE_CLASS_LABEL_SMALL = 'small'

    @staticmethod
    def get_size_for_class(class_name):
        sizes = {Config.SIZE_CLASS_LABEL_SMALL: 1.5, Config.SIZE_CLASS_LABEL_BIG: 4.3}
        return sizes[class_name]

    @staticmethod
    def get_chef_databag_name(chef_env):
        return 'memcache'

    @staticmethod
    def get_chef_databag_item_id(chef_env):
        # TODO changer avant de commiter
        return '{chef_env:s}-frontend'.format(chef_env=chef_env)

    def __init__(self):
        pass
