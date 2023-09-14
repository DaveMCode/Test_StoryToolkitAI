import copy
import os
import codecs
import json
import hashlib
import shutil
import time
from datetime import datetime
import re
from threading import Timer

from timecode import Timecode

from storytoolkitai.core.logger import logger


class Story:
    
    _instances = {}
    
    def __new__(cls, *args, **kwargs):
        """
        This checks if the current story file path isn't already loaded in an instance
        and returns that instance if it is.
        """

        # we use the story file path as the id for the instance
        story_path_id = cls.get_story_path_id(*args, **kwargs)

        # if the story file path is already loaded in an instance, we return that instance
        if story_path_id in cls._instances:

            return cls._instances[story_path_id]

        # otherwise we create a new instance
        instance = super().__new__(cls)

        # and we store it in the instances dict
        cls._instances[story_path_id] = instance

        # then we return the instance
        return instance
    
    def __init__(self, story_file_path):

        # prevent initializing the instance more than once if it was found in the instances dict
        if hasattr(self, '_initialized') and self._initialized:
            return

        self._story_path_id = None
        self.__story_file_path = None

        # this is used to check if the file has changed
        # it will be updated only when the file is loaded and saved
        self._last_hash = None

        self._name = None

        self._lines = []
        self._text = ''

        # timecode data variables
        self._timeline_fps = None
        self._timeline_start_tc = None

        # the main language of the story
        self._language = None

        # this is set to false if the file wasn't found
        self._exists = False

        # for a file to qualify as a story file,
        # it needs to have lines or a lines attribute
        self._is_story_file = False

        # this is set to true if the story file has lines (len > 0)
        self._has_lines = False

        # here we store all the other data that is not part of the known attributes
        # but was found in the story file
        self._other_data = {}

        # where we store the story data from the file
        # this will be empty once the data is loaded into attributes
        self._data = None

        # use the passed story file path
        self.load_from_file(file_path=story_file_path)

        # we use this to keep track if we updated, deleted, added, or changed anything
        self._dirty = False

        # this is used to keep track of the last time the story was saved
        self._last_save_time = None

        # with this we can set a timer to save the story after a certain amount of time
        # this way, we don't create another timer if one is already running and the save_soon method is called again
        self._save_timer = None

        # if we're saving very often, we can throttle the save timer
        # the throttle is a ratio used to multiply the save timer interval
        # the more often we save, the longer the interval between saves
        # but then this is reset to 1 when we're not saving often
        self._save_timer_throttle = 1

        # add this to know that we already initialized this instance
        self._initialized = True

    def __del__(self):
        """
        Make sure we remove this from the instances dict when it's deleted
        """

        # if we're deleting the instance that is stored in the instances dict
        # we remove it from the dict, so we don't have a reference to a deleted object
        if self.__class__._instances[self.story_path_id] == self:
            del self.__class__._instances[self.story_path_id]

    @property
    def language(self):
        return self._language

    @property
    def story_file_path(self):
        return self.__story_file_path

    @property
    def has_lines(self):
        return self._has_lines

    @property
    def is_story_file(self):
        return self._is_story_file

    @property
    def story_path_id(self):
        return self._story_path_id

    @property
    def lines(self):
        return self._lines

    @property
    def name(self):
        return self._name

    @property
    def text(self):
        return self._text

#    def __str__(self):
#        return self.text

    def __dict__(self):
        return self.to_dict()

    @property
    def exists(self):
        return self._exists

    @exists.setter
    def exists(self, value):
        self._exists = value

    @property
    def timeline_fps(self):
        return self._timeline_fps

    @property
    def timeline_start_tc(self):
        return self._timeline_start_tc
        
    @property
    def other_data(self):
        return self._other_data
    
    @property
    def dirty(self):
        return self._dirty

    def is_dirty(self):
        return self._dirty

    def set_dirty(self, value=True):
        self._dirty = value

    def set(self, key: str or dict, value=None):
        """
        We use this to set some of the attributes of the story.
        If the attribute was changed, we set the dirty flag to true.
        """

        # everything that is "known"
        allowed_attributes = copy.deepcopy(self.__known_attributes)

        # but without the lines attribute
        allowed_attributes.remove('lines')

        # if we're setting a dictionary of attributes
        if isinstance(key, dict):

            # we iterate through the dictionary
            for k, v in key.items():

                # and set each attribute
                self.set(k, v)

            return True

        # if the key is a string and is allowed, do this:
        if key in allowed_attributes:

            # if the attribute is different than the current value,
            if getattr(self, '_' + key) != value:

                # set the attribute
                setattr(self, '_' + key, value)

                # set the dirty flag
                self.set_dirty()

            return True

        # throw an error if the key is not valid
        else:
            raise AttributeError('Cannot set the attribute {} for Story, '
                                 'only {} can be set.'.format(key, allowed_attributes))
        
    def reload_from_file(self, save_first=False):
        """
        This reloads the story file from disk and sets the attributes
        :param save_first: if True, we save the story first and then reload it
        """

        # if there's a save timer running, we save the story first
        if save_first and self._save_timer is not None:

            # cancel timer
            self._save_timer.cancel()

            # save story now
            self._save()

        # load the story file from disk
        self.load_from_file(file_path=self.__story_file_path)

    def load_from_file(self, file_path):
        """
        This changes the story_file_path
        and loads the story file from disk and sets the attributes
        """
        self.__story_file_path = file_path

        # when we set the story file_path, we also check if the file exists
        # but only if the file_path is a string
        self._exists = os.path.isfile(self.__story_file_path) if isinstance(file_path, str) else False

        # load the json found in the file into attributes
        self._load_json_into_attributes()

    __known_attributes = [
        'name', 'lines',
        'language',
        'timeline_fps', 'timeline_start_tc'
    ]

    @staticmethod
    def get_story_path_id(story_file_path: str = None):
        return hashlib.md5(story_file_path.encode('utf-8')).hexdigest()
    
    def _load_json_into_attributes(self):

        # calculate the new path id
        self._story_path_id = self.get_story_path_id(self.__story_file_path) \
            if self.__story_file_path else None

        if self._exists:
            # get the contents of the story file
            try:

                logger.debug("Loading story file {}".format(self.__story_file_path))

                with codecs.open(self.__story_file_path, 'r', 'utf-8-sig') as json_file:
                    self._data = json.load(json_file)

                    # let's make a deep copy of the data
                    # so that we can manipulate it without changing the original data
                    self._data = copy.deepcopy(self._data)

            # in case we get JSONDecodeError, we assume that the file is not a valid JSON file
            except json.decoder.JSONDecodeError:
                self._data = {}

            # if we have a file that is not a valid JSON file, we assume that it is not a story file
            except:
                logger.error("story file {} is invalid".format(self.__story_file_path, exc_info=True))
                self._data = {}

        else:
            self._data = {}

        # set the attributes
        for attribute in self.__known_attributes:

            # if the known attribute is in the json, set the attribute
            if attribute in self._data:

                # process the value for the attribute
                attribute_value = self._process_attribute(attribute, copy.deepcopy(self._data[attribute]))

                # if there's nothing left to set, continue
                if attribute_value is None:
                    continue

                # set the attribute, but also process it
                setattr(self, '_'+attribute, attribute_value)

                # and remove it from the data
                del self._data[attribute]

            # if the known attribute is not in the json,
            # set the attribute to None so we can still access it
            else:
                setattr(self, '_'+attribute, None)

        # other data is everything else
        self._other_data = {k: v for k, v in self._data.items() if k not in self.__known_attributes}

        # calculate the hash of the story data
        self._get_story_hash()

        # check if this is a valid story
        self._is_valid_story_data()

    def to_dict(self):
        """
        This returns the story data as a dict.
        It doesn't include all the attributes, only the known ones and the other data.
        """

        # create a copy of the data
        story_dict = dict()

        # add the known attributes to the data
        for attribute in self.__known_attributes:

            # if the attribute is set, add it to the dict
            if hasattr(self, '_'+attribute) and getattr(self, '_'+attribute) is not None:

                # if the attribute is lines, we need to convert the lines to dicts too
                if attribute == 'lines':
                    story_dict[attribute] = [line.to_dict() for line in getattr(self, '_'+attribute)]

                # otherwise, we just add the attribute
                else:
                    story_dict[attribute] = getattr(self, '_'+attribute)

        # merge the other data with the story data
        story_dict.update(self._other_data)

        return story_dict

    def _is_valid_story_data(self):
        """
        This checks if the story is valid by looking at the lines in the data
        """

        # for story data to be valid
        # it needs to have lines which are a list
        # and either the list needs to be empty or the first item in the list needs to be a valid line
        if (isinstance(self._lines, list) \
                and (len(self._lines) == 0
                     or (isinstance(self._lines[0], StoryLine) and self._lines[0].is_valid)
                     or StoryLine(self._lines[0]).is_valid)):
            self._is_story_file = True
        else:
            self._is_story_file = False

    def _process_attribute(self, attribute_name, value):
        """
        This processes the attributes of the story file
        """

        if attribute_name == 'name':

            # if there is no name, we use the file name without the extension
            if not value or value == '':
                value = os.path.splitext(os.path.basename(self.__story_file_path))[0]

        # the lines
        elif attribute_name == 'lines':

            # set the lines
            self._set_lines(lines=value)

            # return None since we already set the attributes in the method
            return None

        return value

    def _set_lines(self, lines: list = None):
        """
        This method sets the _lines attribute (if lines is not None),
        checks if all the lines are StoryLines
        then re-calculates the _has_lines
        """

        # if lines were passed, set them
        if lines is not None:
            self._lines = lines

        # if we have lines, make sure that they're all objects
        for index, line in enumerate(self._lines):

            # if the line is not an object, make it an object
            if not isinstance(line, StoryLine):

                # turn this into a line object
                self._lines[index] = StoryLine(line, parent_story=self)

            # take the text from all the lines and put it in the story ._text attribute
            self._text = (self._text + self._lines[index].text) \
                if isinstance(self._text, str) else self._lines[index].text

        # sort all the lines by their start time
        # self._lines = sorted(self._lines, key=lambda x: x.start)

        # re-calculate the self._has_lines attribute
        self._has_lines = len(self._lines) > 0

        # re-generate the self._line_ids attribute
        # self._line_ids = {i: line.id for i, line in enumerate(self._lines)}

        # re-calculate if it's valid
        self._is_valid_story_data()

    def get_lines(self):
        """
        This returns the lines in the story
        """

        # if we have lines, return them
        return self._lines if self._has_lines else self._lines
    
    def get_line(self, line_index: int = None):
        """
        This returns a specific line object by its index in the lines list
        :param line_index: the index of the line in the lines list
        """

        if line_index is None:
            logger.error('Cannot get line index "{}".'.format(line_index))
            return None

        # if we have lines
        if self._has_lines:

            # if we know the index
            if line_index is not None:

                # if the index is valid
                if 0 <= line_index < len(self._lines):

                    # if the line is not a StoryLine object, make it one
                    if not isinstance(self._lines[line_index], StoryLine):
                        self._lines[line_index] = StoryLine(self._lines[line_index])

                    return self._lines[line_index]
                else:
                    logger.error('Cannot get line with index "{}".'.format(line_index))
                    return None

    def get_num_lines(self):
        """
        This returns the total number of lines in the story
        """

        # if we have lines, return the number of lines
        if self._has_lines:
            return len(self._lines)

        # otherwise return 0
        return 0

    def __len__(self):
        """
        This returns the total number of lines in the story
        """
        return self.get_num_lines()

    def replace_all_lines(self, new_lines: list):
        """
        This deletes all the lines in the story and then replaces them with the new lines
        """
        # if we have lines
        if self._has_lines:

            # delete all the lines
            self._lines = []

        # add the new lines
        self.add_lines(new_lines)

        # set the dirty flag anyway
        self.set_dirty()

    def delete_line(self, line_index: int, reset_lines: bool = True):
        """
        This removes a line from the story and then re-sets the lines
        """

        # if the index is valid
        if line_index is not None and 0 <= line_index < len(self._lines):

            # remove the line
            self._lines.pop(line_index)

            # reset the lines if not mentioned otherwise
            if reset_lines:
                self._set_lines()

        # set the dirty flag anyway
        self.set_dirty()

    def add_lines(self, lines: list):
        """
        This adds a list of lines to the story and then re-sets the lines
        """

        for line in lines:
            self.add_line(line, skip_reset=True)

        # reset the lines if not mentioned otherwise
        self._set_lines()

    def add_line(self, line: dict or object, line_index: int = None, skip_reset=False):
        """
        This adds a line to the story and then re-sets the lines.
        If a line_index is passed, the line will be added at that index, and the rest of the lines will be
        shifted to the right. If no line_index is passed, the line will be added to the end of the lines list.
        """

        # make sure we have a lines list
        if not self._has_lines:
            self._lines = []

        # if the line_data is a dict, turn it into a StoryLine object
        line = StoryLine(line, parent_story=self) if isinstance(line, dict) else line

        # if the line doesn't contain a type, we assume it's a text line
        if not line.type:
            line._type = 'text'

        if not isinstance(line, StoryLine):
            logger.error('Cannot add line "{}" to story - must be dict or StoryLine object.'.format(line))
            return False

        # if we're adding a line at a specific index
        # and the index is valid
        if line_index is not None and 0 <= line_index < len(self._lines):

            # add the line at the index
            self._lines.insert(line_index, line)
            self._has_lines = True

        # otherwise, add the line to the end of the list
        else:
            self._lines.append(line)
            self._has_lines = True

        # reset the lines
        if not skip_reset:
            self._set_lines()

        # set the dirty flag
        self.set_dirty()
        
    def save_soon(self, force=False, backup: bool or float = False, sec=1, **kwargs):
        """
        This saves the story to the file,
        but keeping track of the last time it was saved, and only saving
        if it's been a while since the last save
        :param force: bool, whether to force save the story even if it's not dirty
        :param backup: bool, whether to backup the story file before saving, if an integer is passed,
                             it will be used to determine the time in hours between backups
        :param sec: int, how soon in seconds to save the story, if 0, save immediately
        """

        # if the story is not dirty
        # or if this is not a forced save
        # don't save it
        if not self.is_dirty() and not force:
            logger.debug("Story is unchanged. Not saving.")
            return False

        # if there's no waiting time set, save immediately
        if sec == 0:

            # but first cancel the save timer if it's running
            if self._save_timer is not None:
                self._save_timer.cancel()
                self._save_timer = None

            return self._save(backup=backup, **kwargs)

        # if we're calling this function again before the last save was done
        # it means that we're calling this function more often so many changes might follow in our Transcript,
        # so throttle the save timer for the next time to increase the time between saves
        # also, because the last save didn't executed, we don't have to start another save timer
        # since all changes will be saved when the existing save timer executes
        if self._save_timer is not None:
            # only increase the throttle if it's not already at the max
            if self._save_timer_throttle < 3:
                self._save_timer_throttle *= 1.05
            return
        else:
            self._save_timer_throttle = 1

        # calculate the throttled time
        throttled_sec = sec * self._save_timer_throttle

        kwargs = {**{'backup': backup}, **kwargs}

        self._save_timer = Timer(throttled_sec, self._save, kwargs=kwargs)
        self._save_timer.start()

    def _save(self, backup: bool or float = False,
              if_successful: callable = None, if_failed: callable = None, if_none: callable = None, **kwargs):
        """
        This saves the story to the file
        :param backup: bool, whether to backup the story file before saving, if an integer is passed,
                                it will be used to determine the time in hours between backups
        :param auxiliaries: bool, whether to save the auxiliaries
        :param if_successful: callable, a function to call if the story was saved successfully
        :param if_failed: callable, a function to call if the story failed to save
        :param if_none: callable, a function to call if the story was not saved because it was not dirty
        """

        # create the story data dict
        story_data = self.to_dict()

        # add 'modified' to the story json
        story_data['last_modified'] = str(time.time()).split('.')[0]

        # use the story utils function to write the story to the file
        save_result = StoryUtils.write_to_story_file(
            story_data=story_data,
            story_file_path=self.__story_file_path,
            backup=backup
        )

        # set the exists flag to True
        self._exists = True

        if save_result:
            # set the last save time
            self._last_save_time = time.time()

            # recalculate story hash
            self._get_story_hash()

            # reset the save timer
            self._save_timer = None

            # reset the dirty flag back to False
            self.set_dirty(False)

        # if we're supposed to call a function when the story is saved
        if save_result and if_successful is not None:

            # call the function
            if_successful()

        # if we're supposed to call a function when the save failed
        elif not save_result and if_failed is not None:
            if_failed()

        return save_result

    def _get_story_hash(self):
        """
        This calculates the hash of a dict version of the story
        (the actual things that are written to the file)
        and then calculates the hash.
        """

        # get the dict version of the story
        story_dict = self.to_dict()

        # calculate the hash (also sort the keys to make sure the hash is consistent)
        self._last_hash = hashlib.md5(json.dumps(story_dict, sort_keys=True).encode('utf-8')).hexdigest()

        return self._last_hash

    def get_timecode_data(self):
        """
        Returns the timeline_fps and timeline_start_tc attribute values
        """

        # if both values exist return them in a tuple
        if self._timeline_fps is not None and self._timeline_start_tc is not None:
            return self._timeline_fps, self._timeline_start_tc

        # otherwise return False
        return False

    def set_timecode_data(self, timeline_fps, timeline_start_tc):
        """
        Sets the timeline_fps and timeline_start_tc attribute values
        Then it also sets the dirty flag and saves the story
        """
        self._timeline_fps = timeline_fps
        self._timeline_start_tc = timeline_start_tc

        self._dirty = True
        self.save_soon(sec=0, auxiliaries=False)


class StoryLine:
    """
    This is a class for a line in a story.
    """

    def __init__(self, line_data: dict, parent_story: Story = None):

        # for the line to be valid,
        # it needs to have start and end times
        self._is_valid = False

        self._type = None
        self._text = None
        self._source_start = None
        self._source_end = None
        self._transcription_file_path = None
        self._source_file_path = None
        self._source_fps = None
        self._source_start_tc = None

        self._other_data = {}

        # use this in case we need to communicate with the parent
        self._parent_story = parent_story

        self._load_dict_into_attributes(line_data)

    @property
    def is_valid(self):
        return self._is_valid

    @property
    def parent_story(self):
        return self._parent_story

    @parent_story.setter
    def parent_story(self, value):
        self._parent_story = value

    @property
    def type(self):
        return self._type

    @property
    def text(self):
        return self._text

    @property
    def source_start(self):
        return self._source_start

    @property
    def source_end(self):
        return self._source_end

    @property
    def transcription_file_path(self):
        return self._transcription_file_path

    @property
    def source_file_path(self):
        return self._source_file_path

    @property
    def source_fps(self):
        return self._source_fps

    @property
    def source_start_tc(self):
        return self._source_start_tc

    def __str__(self):
        return self.text

    @property
    def other_data(self):
        return self._other_data

    def set(self, key: str, value):
        """
        We use this to set some of the attributes of the line.
        If the line has a parent, it flags it as dirty.
        """

        allowed_attributes = ['text']

        if key in allowed_attributes:
            setattr(self, '_'+key, value)

            # if the line has a parent, flag it as dirty
            if self.parent_story:
                self.parent_story.set_dirty()

            return True

        # throw an error if the key is not valid
        else:
            raise AttributeError('Cannot set the attribute {} for StoryLine, '
                                 'only {} can be set.'.format(key, allowed_attributes))

    def update(self, line_data: dict or object):
        """
        This updates the line with new line_data
        """

        self._load_dict_into_attributes(line_data)

    # set the known attributes
    __known_attributes = ['text', 'type', 'source_start', 'source_end', 'transcription_file_path',
                          'source_file_path', 'source_fps', 'source_start_tc']

    def _load_dict_into_attributes(self, line_dict):

        # we need to make a copy of the line data
        # to make sure that we don't change the original data
        line_dict = copy.deepcopy(line_dict)

        # if the line is not a dictionary, it is not valid
        if not isinstance(line_dict, dict):
            self._is_valid = False

        # set the attributes
        for attribute in self.__known_attributes:

            # if the known attribute is in the json, set the attribute
            if isinstance(line_dict, dict) and attribute in line_dict:

                # convert the start and end times to floats
                if attribute == 'start' or attribute == 'end':
                    line_dict[attribute] = float(line_dict[attribute])

                setattr(self, '_'+attribute, line_dict[attribute])

            # if the known attribute is not in the json,
            # set the attribute to None so we can still access it
            else:
                setattr(self, '_'+attribute, None)

        # other data is everything else
        if line_dict:
            self._other_data = {k: v for k, v in line_dict.items() if k not in self.__known_attributes}
        else:
            self._other_data = {}

        # for a line to be valid,
        # it needs to have text and type
        if self._text is None or self._type is None:
            self._is_valid = False
        else:
            self._is_valid = True

    def to_dict(self):
        """
        This returns the line data as a dict, but it only converts the attributes that are __known_attributes
        """

        # create a copy of the data
        line_dict = dict()

        # add the known attributes to the data
        for attribute in self.__known_attributes:

            if hasattr(self, '_'+attribute) and getattr(self, '_'+attribute) is not None:
                line_dict[attribute] = getattr(self, '_'+attribute)

        # merge the other data with the story data
        line_dict.update(self._other_data)

        return line_dict
    
    def get_index(self):
        """
        This returns the index of the line in the parent story
        """

        # if the line has a parent, return its index
        if self.parent_story:

            # try to see if the line is in the parent's lines list
            try:
                line_index = self.parent_story.lines.index(self)

            # it might be that the object was already cleared from the parent's lines list
            except ValueError:
                line_index = None

            return line_index

        # if the line does not have a parent, return None
        else:
            return None

    def __del__(self):
        """
        This deletes the line from the parent story, if it has one, otherwise it just deletes the line
        """

        # if the line has a parent, remove it from the parent
        if self.parent_story:

            # get the index of the line from the parent's lines list
            line_index = self.get_index()

            # delete the line from the parent
            # (if it still exists in the parent's lines list)
            if line_index is not None:
                self.parent_story.delete_line(line_index)

        # if the line does not have a parent, just delete it
        else:
            del self


class StoryUtils:

    @staticmethod
    def write_to_story_file(story_data, story_file_path, backup=False):

        # if no full path was passed
        if story_file_path is None:
            logger.error('Cannot save story to path "{}".'.format(story_file_path))
            return False

        # if the story file path is a directory
        if os.path.isdir(story_file_path):
            logger.error(
                'Cannot save story - path "{}" is a directory.'.format(story_file_path))
            return False

        # if the directory of the story file path doesn't exist
        if not os.path.exists(os.path.dirname(story_file_path)):
            # create the directory
            logger.debug("Creating directory for story file path: {}")
            try:
                os.makedirs(os.path.dirname(story_file_path))
            except OSError:
                logger.error("Cannot create directory for story file path.", exc_info=True)
                return False
            except:
                logger.error("Cannot create directory for story file path.", exc_info=True)
                return False

        # if backup_original is enabled, it will save a copy of the story file to
        # .backups/[filename].backup.sts, but if backup is an integer, it will only save a backup after [backup] hours
        if backup and os.path.exists(story_file_path):

            # get the backups directory
            backups_dir = os.path.join(os.path.dirname(story_file_path), '.backups')

            # if the backups directory doesn't exist, create it
            if not os.path.exists(backups_dir):
                os.mkdir(backups_dir)

            # format the name of the backup file
            backup_story_file_path = os.path.basename(story_file_path) + '.backup.sts'

            # if another backup file with the same name already exists, add a consecutive number to the end
            backup_n = 0
            while os.path.exists(os.path.join(backups_dir, backup_story_file_path)):

                # get the modified time of the existing backup file
                backup_file_modified_time = os.path.getmtime(
                    os.path.join(backups_dir, backup_story_file_path))

                # if the backup file was modified les than [backup] hours ago, we don't need to save another backup
                if (isinstance(backup, float) or isinstance(backup, int)) \
                        and time.time() - backup_file_modified_time < backup * 60 * 60:
                    backup = False
                    break

                backup_n += 1
                backup_story_file_path = \
                    os.path.basename(story_file_path) + '.backup.{}.sts'.format(backup_n)

            # if the backup setting is still not negative, we should save a backup
            if backup:
                # copy the existing file to the backup
                shutil \
                    .copyfile(story_file_path, os.path.join(backups_dir, backup_story_file_path))

                logger.debug('Copied story file to backup: {}'.format(backup_story_file_path))

        # encode the story json (do this before writing to the file, to make sure it's valid)
        story_json_encoded = json.dumps(story_data, indent=4)

        # write the story json to the file
        with open(story_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(story_json_encoded)

        logger.debug('Saved story to file: {}'.format(story_file_path))

        return story_file_path

    @staticmethod
    def add_count_to_story_path(story_file_path, target_dir=None):
        """
        This adds a count to the story file path, so that the story file path is unique
        ending either in a file with no number (filename.sts) or a number (filename_2.sts)
        """

        # remove .sts from the end of the path, but don't use replace, it needs to be at the end
        if story_file_path.endswith(".sts"):
            story_file_path_base = story_file_path[:-len(".sts")]
        # otherwise, remove the extension after the last dot using os splitext
        else:
            story_file_path_base = os.path.splitext(story_file_path)[0]

        # if the story_file_path_base contains "_{digits}", remove it
        story_file_path_base = re.sub(r"_[0-9]+$", "", story_file_path_base)

        # use target_dir or don't...
        full_story_file_path = os.path.join(target_dir, story_file_path_base) \
            if target_dir else story_file_path_base

        # add the .sts extension
        full_story_file_path += ".sts"

        count = 2
        while os.path.exists(full_story_file_path):
            # add the count to the story file path
            full_story_file_path = f"{story_file_path_base}_{count}.sts"

            # increment the count
            count += 1

        return full_story_file_path

    @staticmethod
    def write_txt(story_lines: list, txt_file_path: str):
        """
        Write the story lines to a file in TXT format.
        Each segment is written on a new line.
        """

        if not story_lines:
            return

        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            for line in story_lines:
                # write txt lines
                print(
                    line.text.rstrip('\n'),
                    file=txt_file,
                    flush=True,
                )

    @staticmethod
    def write_edl(story_lines: list, edl_file_path: str):
        """
        Write the story lines to a file in EDL format.
        """

        ###
        # This is an example of an EDL file:
        # TITLE: AT 04 Workshop Conversation
        # FCM: NON-DROP FRAME
        #
        # 001  AX       V     C        11:40:39:07 12:04:09:00 01:00:00:00 01:23:29:17
        # * FROM CLIP NAME: C001_08241140_C001.braw
        #
        # 002  AX       A     C        11:40:39:07 12:04:09:00 01:00:00:00 01:23:29:17
        # * FROM CLIP NAME: C001_08241140_C001.braw
        #
        # Segment 1:
        # - Video source identified as "AX"
        # - Type of source is "Video"
        # - Type of transition is "Cut"
        # - The source clip starts at "11:40:39:07" and ends at "12:04:09:00"
        # - In the edited sequence, it will appear starting at "01:00:00:00" and ending at "01:23:29:17"
        # - The name of the video clip being used is "C001_08241140_C001.braw"
        #
        # Segment 2:
        # - Audio source identified as "AX"
        # - The same details for source start time, end time, and the time frame in the final sequence apply.
        # - The same video clip "C001_08241140_C001.braw" is used for audio as well.
        #
        #
        # In simple terms, it's detailing that the video and audio from clip "C001_08241140_C001.braw"
        # starting from "11:40:39:07" to "12:04:09:00"
        # will be used in the final video sequence from "01:00:00:00" to "01:23:29:17".
        # The "V" indicates a video track and "A" indicates an audio track.
        # - these can also be V2, A2 etc. depending on which track they are on.
        # The "C" stands for "Cut," the type of transition between clips.

        if not story_lines:
            return

        with open(edl_file_path, "w", encoding="utf-8") as edl_file_path:
            for line in story_lines:

                if line.type == 'transcription_segment' or line.type == 'video_segment':

                    # todo we need to ask for timeline_fps and timeline_start_tc
                    #  if they're not set for the transcription

                    print(line.source_file_path)
                    print(line.source_start)
                    print(line.source_end)
                    print(line.to_dict())


                # if the file ends with .wav, .mp3 or .aac, it's an audio file - so we won't add the video part

