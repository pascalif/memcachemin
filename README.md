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

* `memcache`
* and optionally `chef` which is lazily imported if needed


## Get started
    git clone https://github.com/pascalif/memcachemin
    cd memcachemin
    pip install -r requirements-min.txt
    python -m memcachemin.mcm --help

Assuming you'll want to quickly try this project with your single local memcached instance listening to port 11211,
 a forged instances description file named ```instances-sample-localhost.json``` is provided to fake a cluster of
 several instances (several entries are pointing to the same physical instance which is only interesting for
 demo purpose). Test memcachemin with it like this :

    python -m memcachemin.mcm --instances-file instances-sample-localhost.json


Finally, the bash script `mcm` is an alias to bootstrap the call to the script, aka containing
`python -m memcachemin.mcm --verbose --instances-file instances.json $*`.
You can use it to simply your calls.


## Actions

### Get statistics
This action connect to each instance and displays some usefull data.

    python -m memcachemin.mc --instances-file instances.json --action stats

Remark : the parameter `--action` is not needed for `stats` action.

Some statistics (total connections, get/set/evictions numbers) can be reset by the memcached protocol. Do it with :

    python -m memcachemin.mc --instances-file instances.json --action stats --stats-reset

If for some reason you want to be sure your memcache instances are running as expected, you
can inject some fake temporary data in it :

    python -m memcachemin.mc --instances-file instances.json --action stats --stats-inject


The stats action will display something like this :
```
Clusters usage :
======================================================================
| Owner      | Usage           | Cu | NbSlots | SlotSize | TotalSize |
======================================================================
| backend    | rawdata         | ww |       2 |   1.5 Gb |    3.0 Gb |
| frontend   | objects         | ww |       4 |   1.5 Gb |    6.0 Gb |
| frontend   | sessions        | ww |       9 |   4.3 Gb |   38.7 Gb |
| frontend   | views           | it |       3 |   1.5 Gb |    4.5 Gb |
| frontend   | views           | en |      10 |   4.3 Gb |   43.0 Gb |
| frontend   | views           | fr |       6 |   4.3 Gb |   25.8 Gb |

Instances details :
=========================================================================================================================================================================================
| ## | Owner      | Usage           | Cu | Ip              | Port  || StartTime           | Con | TotlCon | Memory used                    | NbGet      | NbSet      | HitR | Evictions |
=========================================================================================================================================================================================
| 01 | backend    | rawdata         | ww |   10.0.201.103  | 11211 || 2014-04-15 15:26:28 | 206 |  176408 |  407978375 / 1205862400 : 33 % |  590640607 |   99714007 | 92 % |    290497 |
| 02 | backend    | rawdata         | ww |   10.0.202.177  | 11211 || 2014-04-15 15:26:34 | 206 |   98313 |  391344171 / 1205862400 : 32 % |  384535102 |   71031328 | 98 % |    292258 |
| 03 | frontend   | objects         | ww |   10.0.200.120  | 14212 || 2014-04-15 15:26:48 | 678 |  133428 |  112406355 / 4508876800 : 02 % |   65510782 |   93175764 | 56 % |         0 |
| 04 | frontend   | objects         | ww |   10.0.200.121  | 14212 || 2014-04-15 15:26:39 | 678 |  133388 |   77155927 / 4508876800 : 01 % |  221258559 |   61437195 | 91 % |         0 |
| 05 | frontend   | objects         | ww |   10.0.200.120  | 11211 || 2014-04-15 15:26:47 | 680 |  401923 |  297694766 / 1205862400 : 24 % |  558149640 |    3912925 | 99 % |         0 |
| 06 | frontend   | objects         | ww |   10.0.200.121  | 11211 || 2014-04-15 15:26:39 | 660 |  133088 |  249276012 / 1205862400 : 20 % |   57338265 |    3139996 | 98 % |         0 |
| 07 | frontend   | sessions        | ww |   10.0.200.120  | 14211 || 2014-04-15 15:26:47 | 680 |  164433 | 3200585496 / 4508876800 : 70 % |   27606513 |   49760484 | 97 % |         0 |
| 08 | frontend   | sessions        | ww |   10.0.200.121  | 14211 || 2014-04-15 15:26:39 | 680 |  171442 | 3330730583 / 4508876800 : 73 % |  186155725 |  207909714 | 99 % |         0 |
| 09 | frontend   | sessions        | ww |   10.0.200.119  | 14211 || 2014-04-15 15:27:11 | 679 |  176974 | 3890506121 / 4508876800 : 86 % |   41778558 |   73233158 | 97 % |       238 |
| 10 | frontend   | sessions        | ww |   10.0.201.104  | 14211 || 2014-04-15 15:26:30 | 680 |  178175 | 3895255292 / 4508876800 : 86 % |   39825874 |   76097736 | 97 % |       388 |
| 11 | frontend   | sessions        | ww |   10.0.201.102  | 14211 || 2014-04-15 15:26:30 | 679 |  175077 | 3885870941 / 4508876800 : 86 % |   32932101 |   59919542 | 97 % |       220 |
| 12 | frontend   | sessions        | ww |   10.0.201.103  | 14211 || 2014-04-15 15:26:28 | 676 |  175063 | 3891481351 / 4508876800 : 86 % |   38254153 |   72061277 | 97 % |       177 |
| 13 | frontend   | sessions        | ww |   10.0.202.177  | 14211 || 2014-04-15 15:26:34 | 678 |  159294 | 2712230457 / 4508876800 : 60 % |   27086565 |   42163306 | 97 % |         0 |
| 14 | frontend   | sessions        | ww |   10.0.202.176  | 14211 || 2014-04-15 15:26:39 | 679 |  181573 | 3892418585 / 4508876800 : 86 % |   51455138 |   84243098 | 98 % |       828 |
| 15 | frontend   | sessions        | ww |   10.0.202.175  | 14211 || 2014-04-15 15:26:35 | 680 |  167998 | 3572792447 / 4508876800 : 79 % |   33647817 |   54494136 | 98 % |         0 |
| 16 | frontend   | views           | it |   10.0.200.119  | 11211 || 2014-04-15 15:27:11 | 100 |   25500 | 1017856851 / 1205862400 : 84 % |  190771912 |  148532201 | 31 % |   2389311 |
| 17 | frontend   | views           | it |   10.0.201.104  | 11211 || 2014-04-15 15:26:30 | 100 |   25432 |  889177993 / 1205862400 : 73 % |  113435528 |   92127405 | 23 % |     17481 |
| 18 | frontend   | views           | it |   10.0.201.102  | 11211 || 2014-04-15 15:26:30 | 100 |   25490 |  909339207 / 1205862400 : 75 % |  168814744 |  126301460 | 37 % |    177433 |
| 19 | frontend   | views           | en |   10.0.200.119  | 14212 || 2014-04-15 15:27:12 | 589 |  129557 | 4028372234 / 4508876800 : 89 % |  203730090 |  149601531 | 26 % |   2690752 |
| 20 | frontend   | views           | en |   10.0.201.104  | 14212 || 2014-04-15 15:26:30 | 590 |  130008 | 4035458492 / 4508876800 : 89 % |  287906892 |  200709407 | 41 % |   9626612 |
| 21 | frontend   | views           | en |   10.0.201.102  | 14212 || 2014-04-15 15:26:30 | 589 |  129587 | 4024683447 / 4508876800 : 89 % |  235132339 |  164787934 | 32 % |   1499066 |
| 22 | frontend   | views           | en |   10.0.201.103  | 14212 || 2014-04-15 15:26:28 | 589 |  129892 | 4026502875 / 4508876800 : 89 % |  254937851 |  163563259 | 36 % |   3255352 |
| 23 | frontend   | views           | en |   10.0.202.177  | 14212 || 2014-04-15 15:26:35 | 589 |  128514 | 4022221757 / 4508876800 : 89 % |  194794943 |  133807074 | 31 % |    699929 |
| 24 | frontend   | views           | en |   10.0.202.176  | 14212 || 2014-04-15 15:26:39 | 590 |  127288 | 3987377028 / 4508876800 : 88 % |  167084776 |  108986379 | 34 % |    175790 |
| 25 | frontend   | views           | en |   10.0.202.175  | 14212 || 2014-04-15 15:26:35 | 589 |  128544 | 3989101429 / 4508876800 : 88 % |  215067809 |  142475378 | 36 % |    338114 |
| 26 | frontend   | views           | en |   10.0.200.120  | 14213 || 2014-04-15 15:26:48 | 589 |  129932 | 4029063563 / 4508876800 : 89 % |  274193381 |  208611939 | 41 % |   3081339 |
| 27 | frontend   | views           | en |   10.0.200.121  | 14213 || 2014-04-15 15:26:40 | 590 |  126768 | 3986164108 / 4508876800 : 88 % |  163936690 |  118873537 | 36 % |    153673 |
| 28 | frontend   | views           | en |   10.0.200.119  | 14213 || 2014-04-15 15:27:12 | 590 |  125666 | 3973423008 / 4508876800 : 88 % |  132495121 |   96660657 | 27 % |     91481 |
| 29 | frontend   | views           | fr |   10.0.201.104  | 14213 || 2014-04-15 15:26:30 | 589 |  109335 | 3424468152 / 4508876800 : 75 % |  110744398 |   85701968 | 22 % |         0 |
| 30 | frontend   | views           | fr |   10.0.201.102  | 14213 || 2014-04-15 15:26:30 | 589 |  109468 | 3474834801 / 4508876800 : 77 % |  128718063 |  103870503 | 31 % |         0 |
| 31 | frontend   | views           | fr |   10.0.201.103  | 14213 || 2014-04-15 15:26:29 | 589 |  109467 | 3752845709 / 4508876800 : 83 % |  146892781 |  108757076 | 32 % |      9904 |
| 32 | frontend   | views           | fr |   10.0.202.177  | 14213 || 2014-04-15 15:26:35 | 589 |  109528 | 3721765658 / 4508876800 : 82 % |  164767343 |  111543615 | 32 % |     34712 |
| 33 | frontend   | views           | fr |   10.0.202.176  | 14213 || 2014-04-15 15:26:40 | 589 |  109314 | 2559984986 / 4508876800 : 56 % |   89896725 |   64980667 | 28 % |         0 |
| 34 | frontend   | views           | fr |   10.0.202.175  | 14213 || 2014-04-15 15:26:35 | 589 |  109540 | 3750676917 / 4508876800 : 83 % |  157283113 |  115948829 | 32 % |     16392 |
```

### Flushing memcache data
This action will invalidate every object of the instances.

    python -m memcachemin.mc --instances-file instances.json --action flush-data

You can add the optional parameter `--stats-reset` to reset statistics on each flushed instance (cf stats command).

To limit the potential impact/overhead on client side, you can pace the rate of flush so that all selected instances won't be invalided
at the same time. By default, the value is `10` seconds between each instance flush.

    python -m memcachemin.mc --instances-file instances.json --action flush-data --flush-sleep 60


## Configuration

So far, you have two possible ways to describe your memcache cluster.

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

Use either on CLI :
- the parameter `--chef-env`. Databag name and item id are computed (code can be changed) in Config.py from the Chef environment value.
- or the parameters `--chef-databag` and `--chef-item`.

The databag content must respect the following syntax :

```json
{
  "id": "your-databag-item-id",
  "instances": [
    {
      "size_class": "small",
      "culture": "ww",
      "ip": "  10.0.200.159",
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
    python -m memcachemin.mc --instances-file instances.json --ip  10.0.20.11


All together :

    python -m memcachemin.mc --instances-file instances.json --ip  10.0.20.11 --port 11211
    python -m memcachemin.mc --instances-file instances.json --owner frontend --usage sessions --ip  10.0.20.11

    python -m memcachemin.mc --instances-file instances.json --owner frontend --usage sessions --action flush-data



## Contribute

Many things could be added or improved. You can probably help !

## See also

* [Memcache telnet interface](http://lzone.de/articles/memcached.htm)
* [A powerful web interface written in PHP](http://code.google.com/p/phpmemcacheadmin/)
* [A simpler web interface also in PHP](http://livebookmark.net/journal/2008/05/21/memcachephp-stats-like-apcphp/)
