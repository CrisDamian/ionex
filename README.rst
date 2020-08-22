=====
ionex
=====

IONEX card reader.


*************
Using
*************

Short
-------

::

    import ionex

    with open ('igsg0010.00i') as file:
        inx = ionex.reader (file)
        for ionex_map in inx:
            print (ionex_map.epoch)
            print (ionex_map.tec)


Module content
------------------


~~~~~~~~~~~~~~~~~~~~
`ionex.reader (file)`
~~~~~~~~~~~~~~~~~~~~

Returns the file reader in IONEX format. The reader is an iterable object that
at each iteration, returns an instance of `IonexMap` of the next map read
from file.

**Parameters**

- `file`:` str` | `file`, the path to an IONEX file, or a file object.

** Exceptions **

- `IONEXError`, unknown type or version of file transferred.
- `IONEXUnexpectedEnd` incomplete file.
- `IONEXMapError`, errors while processing the map.


~~~~~~~~~~~~~~~~~~~~~~~
`class ionex.IonexMap`
~~~~~~~~~~~~~~~~~~~~~~~

Map class IONEX, contains a map of TEC values ​​and metadata.

** Attributes **


- `grid`:` namedtuple`, a grid definition for the map, contains two `namedtupla`:

  - `grid.latittude` =` namedtuple ('Latitude', ['lat1', 'lat2', 'dlat']) `
    defining latitude grid from `lat1` to` lat2` with step `dlat`;

  - `grid.longitude` =` namedtuple ('Longitude', ['lon1', 'lon2', 'dlon']) `
    defining a grid in longitude from `lon1` to` lon2` with a step `dlon`.

- `tec`:` list`, PES data; one-dimensional list, is
  a set of latitudinal "slices" with TEC values.

  The beginning of each slice corresponds to the latitude of `grid.latitude.lat1`, the end -
  `grid.latitude.lat2`, with a step equal to` grid.latitude.dlat`.

  The longitude of the first slice corresponds to `grid.longitude.lon1`, longitude
  the latter is `grid.longitude.lon2`, with a step equal to` grid.longitude.dlon`.

- `height`:` float`, the height with which the map data is associated.

- `epoch`:` datetime`, date and time of the PES map.

*********
Installation
*********

Now it's better to set to editable-mode ::

    $ pip install -e git + https: //github.com/gnss-lab/ionex.git#egg=ionex


******
Errors
******

Bugs should be filed at `issues <https://github.com/gnss-lab/ionex/issues>` _.

How to file an error:

- describe how it can be reproduced;
- attach the IONEX files, during the processing of which the
  error or provide a link to these files.

********
License
********

Distributed under the terms of the
`MIT <https://github.com/gnss-lab/gnss-tec/blob/master/LICENSE.txt>` _
license, gnss-tec is free and open source software.

Copyright Ilya Zhivetiev, 2018.
