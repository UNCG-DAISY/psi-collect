import hashlib
import math
import os
import re
import time
from datetime import datetime
from typing import Union, List, Dict, Set, Pattern

import numpy as np
import pandas as pd

from psicollect.common import h, s

flag_unsaved_changes = False  # Keep track of if files have been committed to the disk


class Cataloging:

    @staticmethod
    def parse_catalog_path(scope_path: str = None) -> str:
        """
        Attempts to find the catalog file given a current path. It does this by first checking to see if there is a
        local copy of the catalog in the scope specified. If there isn't, the search then goes to the project data
        directory to get the possible global copy.

        :param scope_path: The root path of the scope to search for the catalog.csv in or None to default to the
        global, storm non-specific file if one exists ('default.csv')
        :return: The path to the catalog file, including the filename and extension
        :except CatalogNotFoundException: If a suitable catalog file cannot be found in the scope or project dir
        """

        storm_id: str or None = Cataloging._get_storm_from_path(scope_path=scope_path)
        catalog_path: str = h.validate_and_expand_path(Cataloging.get_catalog_path(storm_id=storm_id))
        alt_catalog_path: str = h.validate_and_expand_path(os.path.join(scope_path, s.CATALOG_FILE_DEFAULT))

        if os.path.exists(catalog_path) and os.path.isfile(catalog_path):
            # The catalog exists somewhere in the global catalog directory
            return h.validate_and_expand_path(catalog_path)

        elif os.path.exists(alt_catalog_path) and os.path.isfile(alt_catalog_path):
            # The catalog was found as catalog.csv in the scope path
            return h.validate_and_expand_path(os.path.join(scope_path, s.CATALOG_FILE_DEFAULT))

        else:
            raise CatalogNotFoundException

    @staticmethod
    def get_catalog_path(storm_id: str = None) -> str:
        """
        Get the catalog path as specified in s.py. This will return the absolute path on the local machine including
        the file name and extension (e.g. '/home/psic_user/Poststorm_Imagery/data/catalogs/v1/florence.csv').

        :param storm_id: The id of the storm (usually the name of the storm, lower-cased with '_' instead of spaces)
        :return: The absolute path of where the catalog should be (may not actually exist) including the filename and
        extension
        """

        if storm_id is None:
            return h.validate_and_expand_path(os.path.join(s.CATALOG_DATA_PATH, s.CATALOG_FILE_DEFAULT))

        else:
            return h.validate_and_expand_path(
                os.path.join(s.CATALOG_DATA_PATH, s.CATALOG_FILE.replace('${storm_id}', storm_id)))

    @staticmethod
    def generate_index_from_scope(scope_path: Union[str, bytes] = s.DATA_PATH,
                                  fields_needed: Set = s.DEFAULT_FIELDS.copy(),
                                  save_interval: int = 1000,
                                  require_geom: bool = False,
                                  override_catalog_path: Union[bytes, str, None] = None,
                                  debug: bool = s.DEFAULT_DEBUG,
                                  verbosity: int = s.DEFAULT_VERBOSITY,
                                  **kwargs) -> None:
        """
        A function to generate an index of all the data in the scope specified. Does not generate statistics, but
        instead allows for listing the data details based off of each file's attributes. Returns a Generator (an
        iterable object) that can be looped through with a for-loop or similar.

        :param scope_path: The root path to start indexing files from
        :param fields_needed: The fields to include in the catalog (gathered from the local file system)
        :param save_interval: The interval in which to save the data to the disk when accessing the .geom files,
        measured in file access operations. (0 = never save, 1000 = save after every 1,000 files read, etc.)
        :param require_geom: Whether (True) or not (False) to require a .geom file present in search for valid files
        :param override_catalog_path: If set, the program will not search for a catalog, and instead use the path to
        the catalog provided as a string.
        :param debug: Whether (True) or not (False) to override default debug flag and output additional statements
        :param verbosity: The frequency of debug statement output (1 = LOW, 2 = MEDIUM, 3 = HIGH)
        """

        global flag_unsaved_changes  # Include the global variable defined at top of this script

        print('Parsing out current path to determine catalog variables to use ... ', end='')

        scope_path = h.validate_and_expand_path(path=scope_path)
        storm_id: str or None = Cataloging._get_storm_from_path(scope_path=scope_path, debug=debug)

        if override_catalog_path is None:  # pragma: no cover
            try:
                catalog_path = Cataloging.parse_catalog_path(scope_path=scope_path)
            except CatalogNotFoundException:
                catalog_path = Cataloging.get_catalog_path(storm_id=storm_id)

        else:
            # A catalog path is provided, so no need to search (used for testing)
            catalog_path = override_catalog_path

        print('DONE')

        ##########################################
        # Collect matching files from filesystem #
        ##########################################

        print('Getting a list of all valid images ... ', end='')

        # Get a list of all files starting at the path specified
        files: List[str] = h.all_files_recursively(scope_path, unix_sep=True, require_geom=require_geom,
                                                   debug=debug, verbosity=verbosity, **kwargs)

        all_files = files.copy()
        for file_path in all_files:
            if os.path.split(file_path)[0].endswith('bak'):

                # Remove all files that are in 'bak' dirs (backup files)
                files.remove(file_path)

        if len(files) == 0:
            raise CatalogNoEntriesException(curr_dir=scope_path)

        if debug and verbosity >= 2:

            if verbosity < 3 and len(files) > 10:
                # Print only the first five and last five elements (similar to pandas's DataFrames)
                for i in (list(range(1, 6)) + list(range(len(files) - 4, len(files) + 1))):

                    # Right-align the file numbers, because why not
                    print(('{:>' + str(len(str(len(files) + 1))) + '}').format(i) + '  ' + files[i - 1])
                    if i == 5:
                        print(('{:>' + str(len(str(len(files) + 1))) + '}').format('...'))

            else:
                file_list_number = 1

                # Print all elements if there are 10 or less
                for f in files:

                    # Right-align the file numbers, because why not
                    print(('{:>' + str(len(str(len(files) + 1))) + '}').format(file_list_number) + '  ' + f)
                    file_list_number += 1

        print('DONE')

        ####################################################################
        # Load / generate the table (DataFrame) if it doesn't exist        #
        # and populate with file path, file size, and date image was taken #
        ####################################################################

        current_fields_needed: Set = fields_needed.copy()
        flag_unsaved_changes = False

        catalog: pd.DataFrame

        if os.path.exists(catalog_path) is False:
            # If the catalog file doesn't exist, create a new one

            print('Parsing out information about images from their paths ... ', end='')

            entries: List[Dict[str, str or int]] = list()

            for i in range(len(files)):
                entry: dict = dict()
                entry['file'] = files[i]
                entry['storm_id'] = Cataloging._get_storm_from_path(os.path.join(scope_path, files[i])).lower()
                entry['archive'] = Cataloging._get_archive_from_path(scope_path=os.path.join(scope_path, files[i]),
                                                                     storm_id=entry['storm_id']).lower()
                entry['image'] = Cataloging._get_image_from_path(os.path.join(scope_path, files[i]))
                entries.append(entry)

            catalog: pd.DataFrame = pd.DataFrame(entries)

            # DataFrame is populated with these fields, so remove them from the needed list
            current_fields_needed -= {'file', 'storm_id', 'archive', 'image'}

            print('DONE')

            if 'size' in current_fields_needed:
                sizes: List[int] = list()

                for i in range(len(files)):

                    print(f'\rGetting size of file {i + 1} of {len(files)} ({round((i / len(files)) * 100, 2)}%) ' +
                          '.' * (math.floor(((i + 1) % 9) / 3) + 1), end=' ')
                    sizes.append(os.path.getsize(os.path.join(scope_path, files[i])))

                catalog['size'] = sizes
                flag_unsaved_changes = True
                current_fields_needed.remove('size')

            if 'date' in current_fields_needed:
                dates: List[str] = list()

                stat_count_missing_date: int = 0

                for i in range(len(files)):

                    print(f'\rGetting date taken from file {i + 1} of {len(files)} ({round((i / len(files)) * 100, 2)}%) ' +
                          '.' * (math.floor(((i + 1) % 9) / 3) + 1), end=' ')

                    best_date: str or None = Cataloging._get_best_date(os.path.join(scope_path, files[i]))

                    if best_date is None:
                        # If no date can be found, leave the entry blank
                        dates.append(np.nan)
                        stat_count_missing_date += 1
                    else:
                        dates.append(Cataloging._get_best_date(os.path.join(scope_path, files[i])))

                if stat_count_missing_date > 0:
                    print(str(stat_count_missing_date) + ' images had unknown dates!')
                else:
                    print('DONE')

                catalog['date'] = dates
                flag_unsaved_changes = True
                current_fields_needed.remove('date')

            # Create the file in the scope directory
            Cataloging._force_save_catalog(catalog=catalog, scope_path=scope_path)

        else:

            print('Reading in existing catalog to try and fill in any missing values ... ', end='')

            catalog = pd.read_csv(catalog_path, usecols=lambda col_label: col_label in current_fields_needed)

            if catalog.shape[0] < len(files):
                # If there are fewer images found than listed in current catalog
                h.print_error(f'Found {catalog.shape[0]} entries in the existing catalog and {len(files)} files in the '
                              f'scope directory. Files are most likely missing or misplaced! ')
                exit(1)

            elif catalog.shape[0] > len(files):
                # The number of images in the directory exceed the amount listed in the current catalog
                h.print_error('The catalog seems to be missing some entries! Deleting old one and trying again ... ')
                os.remove(catalog_path)
                Cataloging.generate_index_from_scope(scope_path=scope_path,
                                                     fields_needed=fields_needed,
                                                     save_interval=save_interval,
                                                     require_geom=require_geom,
                                                     override_catalog_path=override_catalog_path,
                                                     debug=debug,
                                                     verbosity=verbosity,
                                                     **kwargs)
                exit(0)

            # Remove basic info as it should already exist in the CSV file
            current_fields_needed -= {'file', 'storm_id', 'archive', 'image', 'date', 'size'}

            print('DONE')

        ##########################################################################################
        # Collect information from the .geom files about latitude and longitude of image corners #
        ##########################################################################################

        if debug and verbosity >= 1:
            print('Basic data is complete! Moving on to .geom specific data ... ')

        for field in current_fields_needed:

            # If a column for each field does not exist, create one for each field with all the values as empty strings
            if field not in catalog:
                catalog[field] = ''
                flag_unsaved_changes = True

        stat_files_accessed: int = 0
        stat_count_missing_geom: int = 0

        # For any remaining fields needed (i.e. ll_lat), look for them in the .geom files
        for i, row in catalog.iterrows():

            dots = math.floor(((i + 1) % 9) / 3) + 1

            print(f'\rProcessing .geom attributes of file {i + 1} of {len(files)} '
                  f'({round((i / len(files)) * 100, 2)}%) ' +
                  '.' * dots + ' ' * (3 - dots), end=' ')

            row_fields_needed = current_fields_needed.copy()
            row_fields_existing = set()

            # Remove redundant queries to .geom file if the data is already present in the catalog
            for field in current_fields_needed:
                if (type(row[field]) is str and len(row[field]) > 0) \
                        or (type(row[field]) is not str and str(row[field]).lower() != "nan"):
                    row_fields_existing.add(field)
                    row_fields_needed.remove(field)

            ending: str
            if debug and verbosity >= 3:
                ending = '\n'
            else:
                ending = '\r'

            if len(row_fields_existing) > 0:
                print(f'Found existing data for {row_fields_existing} ... skipping these fields!', end=ending)

            # Only query the .geom file if there are fields still unfilled
            if len(row_fields_needed) > 0:

                # Look up the fields that are needed and still missing data
                geom_data: Dict[str, str] or None = Cataloging._get_geom_fields(
                    field_id_set=row_fields_needed, file_path=os.path.join(
                        scope_path, os.path.normpath(row['file'])), debug=debug, verbosity=verbosity)
                stat_files_accessed += 1

                if geom_data is None:
                    # The geom file does not exist

                    geom_data = dict()

                    for field_id in row_fields_needed:
                        # Since no .geom file was found, fill with nan values
                        geom_data[field_id] = np.nan

                    stat_count_missing_geom += 1

                else:
                    # Store the values in the catalog's respective column by field name, in memory
                    for key, value in geom_data.items():
                        try:
                            catalog.at[i, key] = value
                        except ValueError as e:
                            h.print_error('The catalog seems to be corrupted or out of date! Deleting old one and '
                                          f'trying again ... \nError: {e}')
                            os.remove(catalog_path)
                            Cataloging.generate_index_from_scope(scope_path=scope_path,
                                                                 fields_needed=fields_needed,
                                                                 save_interval=save_interval,
                                                                 require_geom=require_geom,
                                                                 override_catalog_path=override_catalog_path,
                                                                 debug=debug,
                                                                 verbosity=verbosity,
                                                                 **kwargs)
                            exit(0)

                        flag_unsaved_changes = True

            if save_interval > 0 and stat_files_accessed != 0 and stat_files_accessed % save_interval == 0:

                print('\rSaving catalog to disk (' + str(stat_files_accessed) +
                      ' .geom files accessed) ... ', end='')
                Cataloging._force_save_catalog(catalog=catalog, scope_path=scope_path)

        if stat_count_missing_geom > 0:
            print(str(stat_count_missing_geom) + ' images were missing a .geom file!')
        else:
            print('DONE')

        if debug:
            print('\r')

            if verbosity >= 1:
                print()
                print(catalog)

        # Do a final save of the file
        Cataloging._force_save_catalog(catalog=catalog, scope_path=scope_path)

        print('Saved all existing data successfully!\n')

    #####################################
    # Catalog-Specific Helper Functions #
    #####################################

    @staticmethod
    def _get_best_date(file_path: Union[bytes, str],
                       debug: bool = s.DEFAULT_DEBUG,
                       verbosity: int = s.DEFAULT_VERBOSITY) -> str or None:

        # Assume years can only be 2000 to 2099 (current unix time ends at 2038 anyways)
        pattern: Pattern = re.compile('[\\D]*(20\\d{2})(\\d{2})(\\d{2})\\D')

        # Search the entire path for a matching date format, take the last occurrence
        if re.search(pattern, file_path):
            year, month, day = re.search(pattern, file_path).groups()

            if debug and verbosity >= 1:
                # In-line progress (no spam when verbosity is 1)
                print('\rFound year: %s, month: %s, day: %s in PATH: %s' % (year, month, day, file_path), end='')

                if verbosity >= 2:
                    # Multi-line output of progress (may be quite verbose)
                    print()

            return year + '/' + month + '/' + day

        # If no date can be parsed from file path or file name, then leave blank
        else:
            if debug:
                h.print_error('Could not find any date in ' + file_path + ' ... leaving it blank!')
            return None

    @staticmethod
    def _timestamp_to_utc(timestamp: str or int) -> str:
        timestamp = datetime.utcfromtimestamp(timestamp)
        return timestamp.strftime("%Y/%m/%d")

    @staticmethod
    def _get_image_from_path(scope_path: Union[bytes, str] = None) -> str or None:

        scope_path = h.validate_and_expand_path(scope_path)

        image_file: str = os.path.split(scope_path)[1]

        if '.jpg' in image_file:
            return image_file
        else:
            return None

    @staticmethod
    def _get_storm_from_path(scope_path: Union[bytes, str] = None, debug: bool = s.DEFAULT_DEBUG,
                             recurse_count: int = 0) -> str or None:

        if debug:
            print('Looking for storm in path: ' + str(scope_path))

        scope_path = h.validate_and_expand_path(scope_path)

        path_head, path_tail = os.path.split(scope_path)

        if path_head == os.path.splitdrive(scope_path)[1] and path_tail == '':
            # If the filesystem root directory is reached, a storm-specific catalog cannot be found

            raise PathParsingException(objective='the storm name')

        if recurse_count > 10:
            raise RecursionError('Could not find storm in path after 10 iterations!')

        if path_tail[0].islower() or re.match('.*([._]).*', path_tail) or scope_path == s.DATA_PATH:
            # If the first character of the directory's name is lower-cased (storms should have capitals)
            # or the directory is actually a file or archive or is the data path

            # Keep recursively checking each directory to match the pattern (traverse back through path)
            return Cataloging._get_storm_from_path(scope_path=os.path.split(scope_path)[0],
                                                   recurse_count=(recurse_count + 1))

        else:
            if debug:
                print('Found storm name (' + str(path_tail) + ') in path: ' + str(scope_path))

            return path_tail

    @staticmethod
    def _get_archive_from_path(scope_path: Union[bytes, str], storm_id: str) -> str:

        scope_path = h.validate_and_expand_path(scope_path)

        path_head, path_tail = os.path.split(scope_path)

        if path_tail == '':
            # If the filesystem root directory is reached, a storm-specific catalog cannot be found

            raise PathParsingException(objective='the archive name')

        if os.path.split(path_head)[1].lower() == storm_id:
            # If the parent directory is the storm directory

            return path_tail

        else:
            # Keep recursively checking each directory to match the pattern (traverse back through path)
            return Cataloging._get_archive_from_path(scope_path=os.path.split(scope_path)[0], storm_id=storm_id)

    @staticmethod
    def _force_save_catalog(catalog: pd.DataFrame, scope_path: Union[bytes, str]):
        global flag_unsaved_changes  # Include the global variable defined at top of this script

        if flag_unsaved_changes is False:
            return

        flag_save_incomplete = True

        while flag_save_incomplete:
            try:
                storm_id: str = Cataloging._get_storm_from_path(scope_path=scope_path)
                catalog_path: str = Cataloging.get_catalog_path(storm_id=storm_id)

                if os.path.exists(os.path.split(catalog_path)[0]) is False:
                    # Create the necessary directories if they do not exist
                    os.makedirs(os.path.split(catalog_path)[0])

                # Periodically save the file based on the save_interval parameter
                catalog.to_csv(Cataloging.get_catalog_path(storm_id=storm_id))
                flag_unsaved_changes = False
                flag_save_incomplete = False

            except PermissionError as e:  # pragma: no cover
                h.print_error(str(e) + '\nTry closing the file if it is open in another program!\nWill attempt '
                                       'to save again in 10 seconds ... \n')
                time.sleep(10)

        print('Saved catalog to disk! ', end='')
        flag_unsaved_changes = False

    @staticmethod
    def _get_geom_fields(field_id_set: Set[str] or str, file_path: Union[bytes, str],
                         debug: bool = s.DEFAULT_DEBUG, verbosity: int = s.DEFAULT_VERBOSITY) \
            -> Union[Dict[str, str], str, None]:

        is_single_input = False

        # If only one id is entered (a single string), convert to a set of 1 element
        if type(field_id_set) is str:
            field_id_set: Set[str] = {field_id_set}
            is_single_input = True

        # Get the .geom file that corresponds to this file (substitute existing extension for ".geom")
        geom_path = h.validate_and_expand_path(re.sub(pattern='\\.[^.]*$', repl='.geom', string=str(file_path)))

        result: Dict[str] = dict()

        if os.path.exists(geom_path) is False:
            if debug:
                h.print_error('Could not find .geom file for "' + file_path + '": "' + geom_path + '"')
            return None

        if os.path.getsize(geom_path) == 0:
            h.print_error('\n\nThe .geom file for "' + file_path + '": "' + geom_path + '" is 0 KiBs.\n'
                          'Bad file access may have caused this, so check the archive to see if the image and '
                          'the .geom files in the archive are the same as the unzipped versions!\n')
            for field_id in field_id_set:
                # Since no .geom file was found, fill with nan values
                result[field_id] = np.nan

            return result

        # Generate a new hash object to store the hash data
        hashing: hashlib.md5 = hashlib.md5()

        with open(geom_path, 'rb') as f:
            # Use the geom file's bytes to generate a checksum

            if 'geom_checksum' in field_id_set:
                # Generate a md5 hash to help ensure the correct data is being referenced if compared elsewhere
                hashing.update(f.read())
                result['geom_checksum'] = hashing.hexdigest()
                field_id_set.remove('geom_checksum')

        with open(geom_path, 'r') as f:

            for line in f.readlines():

                # If there are no more fields to find, close the file and return the resulting dictionary or string
                if len(field_id_set) == 0:
                    f.close()

                    if debug and verbosity >= 2:
                        print('\rFound ' + str(len(result)) + ' value(s) in ' + geom_path, end='')

                        if verbosity >= 3:
                            print()  # RIP your console if you get here

                    if is_single_input and len(result) == 1:
                        # Return the first (and only value) as a single string
                        return str(list(result.values())[0])

                    return result

                field_id_set_full = field_id_set.copy()
                for field_id in field_id_set_full:
                    value = re.findall(field_id + ':\\s+(.*)', line)
                    if len(value) == 1:
                        result[field_id] = str(value[0])
                        field_id_set.remove(field_id)

            f.close()
            h.print_error('\nCould not find any values for fields ' + str(field_id_set) + ' in ' + geom_path)
            for field_id in field_id_set:
                # Fill missing fields with nan values
                result[field_id] = np.nan

            return result


class CatalogNoEntriesException(IOError):
    def __init__(self, curr_dir: str):
        IOError.__init__(self, 'There were no images found in any sub-directories in ' + curr_dir)


class CatalogNotFoundException(IOError):
    def __init__(self):
        IOError.__init__(self, 'The catalog file was not found!')


class PathParsingException(IOError):
    def __init__(self, objective: str):
        IOError.__init__(self, 'Could not parse ' + objective + ' from the current path.')
