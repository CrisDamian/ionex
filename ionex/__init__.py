from .ionex_file import IonexV1, NullContext
from .exceptions import IONEXError
from .exceptions import IONEXUnexpectedEnd

__all__ = ['reader']


def _get_version_type(line):
    return float(line[:8]), line[20]


def reader(file):
    """Returns the file reader in IONEX format.
     The reader is an iterable object, at each iteration it returns an instance
     
     `` ionex_map.IonexMap`` next map read from file.
     : type file: str | file-object
     
     : param file: Path to the IONEX file or file object.
 
     : raises IONEXError:
        If the type or version of the uploaded file is unknown.
     
     : raises IONEXUnexpectedEnd:
         Incomplete file.
     
     : raises IONEXMapError:
         If there are errors while processing the card.
    """
    readers = {
        1.0: IonexV1,
    }

    if isinstance(file, str):
        context_manager = open(file)
    else:
        context_manager = NullContext(file)

    with context_manager as file_object:
        try:
            file_ver, file_type = _get_version_type(next(file_object))
        except StopIteration:
            raise IONEXUnexpectedEnd(file_object)

        if file_type != 'I':
            raise IONEXError('Unknown file type.')
        if file_ver not in readers:
            raise IONEXError('Unsupported version: {}'.format(file_ver))

        reader_class = readers[file_ver]
        return reader_class(file)
