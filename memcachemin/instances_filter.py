__author__ = 'pascalif'


class MemcacheInstancesFilter():
    def __init__(self):
        pass

    def filter(self, instances, culture=None, owner=None, usage=None, ip=None, port=None):
        filtered_instances = instances
        if culture is not None:
            filtered_instances = self.filter_by_culture(filtered_instances, culture)
        if owner is not None:
            filtered_instances = self.filter_by_owner(filtered_instances, owner)
        if usage is not None:
            filtered_instances = self.filter_by_usage(filtered_instances, usage)
        if ip is not None:
            filtered_instances = self.filter_by_ip(filtered_instances, ip)
        if port is not None:
            filtered_instances = self.filter_by_port(filtered_instances, port)
        return filtered_instances

    def filter_by_culture(self, instances_desc, culture):
        return self._filter_by_field(instances_desc, 'culture', culture)

    def filter_by_ip(self, instances_desc, ip):
        return self._filter_by_field(instances_desc, 'ip', ip)

    def filter_by_port(self, instances_desc, port):
        return self._filter_by_field(instances_desc, 'port', port)

    def filter_by_usage(self, instances_desc, usage):
        return self._filter_by_field(instances_desc, 'usage', usage)

    def filter_by_owner(self, instances_desc, owner):
        return self._filter_by_field(instances_desc, 'owner', owner)

    def _filter_by_field(self, instances_desc, field_name, field_value):
        filtered_instances = []
        for instance_desc in instances_desc:
            if instance_desc[field_name] == field_value:
                filtered_instances.append(instance_desc)
        return filtered_instances
