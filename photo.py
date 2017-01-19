import matplotlib.image as mpimg
import os


class Photo:

    LEFT = 0
    RIGHT = 1

    def __init__(self, filename, score=1400.0, wins=0, matches=0):

        if not os.path.isfile(filename):
            raise ValueError("Could not find the file: %s" % filename)

        self._filename = filename
        self._score = score
        self._wins = wins
        self._matches = matches

        self._read_and_downsample()

    def data(self):
        return self._data

    def filename(self):
        return self._filename

    def matches(self):
        return self._matches

    def score(self, s=None, is_winner=None):

        if s is None:
            return self._score

        assert is_winner is not None

        self._score = s

        self._matches += 1

        if is_winner:
            self._wins += 1

    def win_percentage(self):
        return 100.0 * float(self._wins) / float(self._matches)

    def __eq__(self, rhs):
        return self._filename == rhs._filename

    def to_dict(self):

        return {
            'filename': self._filename,
            'score': self._score,
            'matches': self._matches,
            'wins': self._wins,
        }

    def _read_and_downsample(self):
        """
        Reads the image, performs rotation, and downsamples.
        """

        # read image

        f = self._filename

        data = mpimg.imread(f)

        # downsample

        # the point of downsampling is so the images can be redrawn by the
        # display as fast as possible, this is so one can iterate though the
        # image set as quickly as possible.  No one want's to wait around for
        # the fat images to be loaded over and over.

        # dump downsample, just discard columns-n-rows

        # M, N = data.shape[0:2]

        # MN = max([M,N])

        # step = int(MN / 800)
        # if step == 0: m_step = 1

        # data = data[ 0:M:step, 0:N:step, :]

        # #----------------------------------------------------------------------
        # # rotate

        # # read orientation with exifread
        # with open(f, 'rb') as fd:
        #     tags = exifread.process_file(fd)

        # print (tags)

        # #r = str(tags['Image Orientation'])

        # # rotate as necessary

        # if r == 'Horizontal (normal)':
        #     pass

        # elif r == 'Rotated 90 CW':

        #     data = np.rot90(data, 3)

        # elif r == 'Rotated 90 CCW':

        #     data = np.rot90(data, 1)

        # elif r == 'Rotated 180':

        #     data = np.rot90(data, 2)

        # else:
        #     raise RuntimeError('Unhandled rotation "%s"' % r)

        self._data = data