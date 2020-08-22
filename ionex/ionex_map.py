from collections import namedtuple

from .exceptions import IONEXMapError

Grid = namedtuple('Grid', ['latitude', 'longitude'])
Latitude = namedtuple('Latitude', ['lat1', 'lat2', 'dlat'])
Longitude = namedtuple('Longitude', ['lon1', 'lon2', 'dlon'])


class IonexMap:
    """IONEX card class. Contains map and meta data.
    
    Attributes:
    
    : type grid: namedtuple
    
    : param grid: a grid definition for the map, contains two
        `` namedtupla``:
    
    - `` grid.latittude`` =
          `` namedtuple ('Latitude', ['lat1', 'lat2', 'dlat']) 'definition
          latitude grids from `` lat1 '' to `` lat2 '' with step `` dlat '';
    
    - `` grid.longitude`` =
          `` namedtuple ('Longitude', ['lon1', 'lon2', 'dlon']) ''
          longitude grid definition from `` lon1 '' to `` lon2 '' with a step
          `` dlon``.
    
    : type tec: list
    
    : param tec: PES data; one-dimensional list, is
        a set of latitudinal "slices" with TEC values.
        The beginning of each slice corresponds to the latitude of `` grid.latitude.lat1 '', the end
        - `` grid.latitude.lat2``, with a step equal to
        `` grid.latitude.dlat``.
        The longitude of the first slice corresponds to `` grid.longitude.lon1 '', longitude
        the latter is `` grid.longitude.lon2 '', with a step equal to
        `` grid.longitude.dlon``.
    
    : type height: float
    
    : param height: The height with which the map data is associated.
    
    : type epoch: datetime
    
    : param epoch: date and time of the PES map.
    """

    def __init__(self, *,
                 exponent,
                 epoch,
                 longitude,
                 latitude,
                 height,
                 tec,
                 rms=None,
                 none_value=None):
        """
       param exponent:
            `` int``, value 'EXPONENT' from file IONEX; power,
            into which the TEC values will be raised.

        : param epoch:
            `` datetime.datetime``, the date and time of the current card.

        : param longitude:
            `` tuple``, latitude grid definition, (lon1, lon2, dlon),
            values are assumed to be the same as header values
            'LON1 / LON2 / DLON' from IONEX file.

        : param latitude:
           `` tuple``, latitude grid definition, (lat1, lat2, dlat),
           values are assumed to be the same as header values
           'LAT1 / LAT2 / DLAT' from IONEX file.

        : param height:
            float, the height of the current map.

        : param tec:
            `` list``, a list of PES values from the IONEX.

        : param rms:
            `` list``, a list of RMS values from the IONEX file.

        : param none_value:
            `` int``, values in the map equal to `` none_value`` will be replaced with
            `` None``. By default, none_value == None, in which case
            no replacement will be made.
        """
        self.epoch = epoch
        self.height = height
        self.grid = Grid(
            latitude=Latitude(*latitude),
            longitude=Longitude(*longitude),
        )

        self._exponent = exponent
        self._none_value = none_value

        self._tec = tec.copy()
        self._rms = rms.copy() if rms is not None else None

        if not self._grid_match_data():
            err_msg = 'The grid definition does ' \
                      'not match the map; epoch {}.'.format(self.epoch)
            raise IONEXMapError(err_msg)

    @property
    def tec(self):
        """Вернуть ПЭС с учётом степени."""
        tec = [v * 10 ** self._exponent for v in self._tec]
        if self._none_value is None:
            return tec

        none_value = self._none_value * 10 ** self._exponent
        while True:
            try:
                i = tec.index(none_value)
                tec[i] = None
            except ValueError:
                break
        return tec

    @property
    def rms(self):
        raise NotImplementedError

    def _grid_match_data(self):
        def cells(start, stop, step):
            return (abs(start) + abs(stop)) / abs(step) + 1

        lat_cells = cells(*self.grid.latitude)
        lon_cells = cells(*self.grid.longitude)
        return lon_cells * lat_cells == len(self._tec)
