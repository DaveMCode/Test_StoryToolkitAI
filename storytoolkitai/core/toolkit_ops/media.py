import os
import cv2
from moviepy.editor import VideoFileClip, AudioFileClip

from storytoolkitai.core.toolkit_ops.videoanalysis import ClipIndex
from storytoolkitai.core.logger import logger


class MediaItem:
    """
    This handles all the audio/video items that are used in the toolkit.
    """

    def __init__(self, path: str):

        # the path of the media item
        self._path = path

        # the name of the media item is the basename of the path
        self._name = os.path.basename(path)

        self._type = None

        self._duration = None
        self._metadata = None

    @property
    def path(self):
        """
        Returns the path of the media item.
        """
        return self._path

    @property
    def name(self):
        """
        Returns the name of the media item.
        """
        return self._name

    @property
    def type(self):
        """
        Returns the type of the media item.
        """
        return self._type

    @property
    def duration(self):
        """
        Returns the duration of the media item.
        """
        return self._duration

    @property
    def metadata(self):
        """
        Returns the metadata of the media item.
        """
        return self._metadata

    def get_duration(self):
        """
        Returns the duration of the media item.
        """
        pass

    def get_metadata(self):
        """
        Returns the metadata of the media item.
        """
        pass

    def get_transcription(self):
        """
        Returns the transcription of the media item.
        """
        pass

    @staticmethod
    def has_audio(file_path):
        """
        Checks if the file has audio and returns True if it does, otherwise returns False.
        """

        try:
            audio_clip = AudioFileClip(file_path)
            audio_present = audio_clip.duration > 0
        except Exception:
            audio_present = False

        return audio_present

    @staticmethod
    def has_video(file_path):
        """
        Checks if the file has video and returns True if it does, otherwise returns False.
        """

        try:
            clip = VideoFileClip(file_path)
            video_present = clip.reader.nframes > 0
        except Exception:
            video_present = False

        return video_present

class AudioItem(MediaItem):
    """
    This handles all the audio items that are used in the toolkit.
    """

    def __init__(self, path: str):
        super().__init__(path=path)

        self._type = 'audio'

class VideoItem(MediaItem, ClipIndex):
    """
    This handles all the video items that are used in the toolkit.
    """

    def __init__(self, path: str):

        MediaItem.__init__(self, path=path)
        ClipIndex.__init__(self)

        self._type = 'video'

        self.source_path = self.path

        self._timecode_data = None

    def get_timecode_data(self):
        """
        Returns the timecode data of the video item.
        """
        return self._timecode_data

    def extract_timecode_data(self):
        """
        Extracts the timecode data from the file
        """

        # look into the file's metadata and extract the timecode data

    def get_video_frame(self, frame_index: int):
        """
        Returns the video frame at the given frame index.
        """

        cap = cv2.VideoCapture(self.source_path)

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index - 1)
        ret, frame = cap.read()

        # Return the frame if it was read correctly, otherwise return None
        return frame if ret else None

    ClipIndex = ClipIndex

