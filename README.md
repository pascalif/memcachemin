memcachemin
===========

## About

memcachemin is a mini CLI tools to administrate a memcache instances cluster.
It does not replace more powerful web interfaces but gives you an easy CLI way to :

* check on your console the usage of a cluster of several memcache instances, helping you to decide to upgrade or downgrade its size,
* flush all or a subset of those instances.

Through attributes, several instances can be regrouped into sub-clusters depending on their clients, usage, host...
The global cluster can be statically described through a JSON description file or dynamically loaded from a Chef databag.


## Requirements

* ```memcache```
* ```json```
* and optionally ```chef``` which is lazily imported if needed


## Get started
    git clone https://github.com/pascalif/memcachemin
    cd memcachemin
    pip install -r requirements-light.txt
    python -m memcachemin.mcm --help

Assuming you'll want to quickly try this project with your single local memcached instance listening to port 11211,
 a forged instances description file named ```instances-sample-localhost.json``` is provided to fake a cluster of
 several instances (several entries are pointing to the same physical instance which is only interesting for
 demo purpose). Test memcachemin with it like this :

    python -m memcachemin.mcm --instances-file instances-sample-localhost.json


Finally, ```mcm``` is an alias to bootstrap the call to the script, aka containing
```python -m memcachemin.mcm --verbose --instances-file instances.json $*```.
You can use it to simply your calls if using an instances description file.


## Examples

### Get statistics
This action connect to each instance and display some usefull intel.

    python -m memcachemin.mc --instances-file instances.json --action stats

Remark : the parameter ```--action``` is not needed for ```stats``` action.

Some statistics can be reset by the memcached protocol. Do it with :

    python -m memcachemin.mc --instances-file instances.json --action stats --stats-reset


### Flushing memcache data
This action will flag every object of the instance(s) as removeable.

    python -m memcachemin.mc --instances-file instances.json --action flush-data

To limit overhead on client side, you can pace the rate of flush so that all selected instances won't be invalided
at the same time. By default, the value is ```10``` seconds between each instance flush.

    python -m memcachemin.mc --instances-file instances.json --action flush-data --fhush-sleep 60


### Configuration

So far, you have two different location to describe the memcache cluster. The format must be the same.

### Local file

This must be a JSON file containing a list of structures respecting the following example :

```json
[
{"ip": "192.169.0.10", "culture": "en", "owner": "frontend", "usage": "objects", "port": 11211, "size_class": "small"},
{"ip": "192.169.0.10", "culture": "fr", "owner": "frontend", "usage": "objects", "port": 11212, "size_class": "small"},
...
{"ip": "192.169.0.99", "culture": "ww", "owner": "frontend", "usage": "sessions", "port": 11214, "size_class": "small"},
{"ip": "192.169.0.99", "culture": "en", "owner": "frontend", "usage": "views", "port": 11215, "size_class": "small"}
]
```

The values of attributes ```culture```, ```owner``` and ```usage``` is free.

By default, ```memcachemin``` will try to locate a file name ```instances.json``` in the current directory.
You can override the location and name by using the parameter ```--instances-file```.


### Chef

If you use Chef for provisioning, you can get dynamic cluster information from it.

You could create a Chef recipe to do whatever is needed on your admin host, plus the creation of the previous file.
Either through a `chef-client` or a `knife ssh`, you would be able to update the description file.

But, if you want to be sure your data is always up to date
(and not be affected by a `chef-client` run frequency)
memcachemin can directly load the instances description from a Chef server's databag.

Use the parameter ```--chef-env``` on CLI. Databag name and item id are configurable on config.py
(note : to be improved in next release)

The databag content must respect following syntax :

```json
{
  "id": "your-databag-item-id",
  "instances": [
    {
      "size_class": "small",
      "culture": "ww",
      "ip": "10.208.160.159",
      "usage": "objects",
      "owner": "frontend",
      "port": 11211
    },
    ...
  ]
}
```

### Filtering instances
By default, actions are applied to all instances. You can filter them on several perpendicular dimensions
represented by attributes attached to each instances.

There are two mandatory attributes :

* `ip`
* `port`

Optional attributes are :

* ```owner``` : the client of this instance
* ```usage``` : which specific usage is done on this instances (eg : views, rawdata, objects, sessions, ...)
* ```culture``` : the culture of the data (eg : any, en, fr, ...)

You can give any values to thoses attributes

    python -m memcachemin.mc --instances-file instances.json --owner frontend
    python -m memcachemin.mc --instances-file instances.json --usage sessions
    python -m memcachemin.mc --instances-file instances.json --ip 10.0.20.11


All together :

    python -m memcachemin.mc --instances-file instances.json --ip 10.0.20.11 --port 11211
    python -m memcachemin.mc --instances-file instances.json --owner frontend --usage sessions --ip 10.0.20.11

    python -m memcachemin.mc --instances-file instances.json --owner frontend --usage sessions --action flush-data



## Contribute

Many things could be added or improved. You can probably help !

## See also

* [Memcache telnet interface](http://lzone.de/articles/memcached.htm)
* [A powerful web interface written in PHP](http://code.google.com/p/phpmemcacheadmin/)
* [A simpler web interface also in PHP](http://livebookmark.net/journal/2008/05/21/memcachephp-stats-like-apcphp/)
