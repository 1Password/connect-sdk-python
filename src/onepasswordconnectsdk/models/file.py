import pprint


class File:
    openapi_types = {
        'id': 'str',
        'name': 'str',
        'size': 'int',
        'content_path': 'str',
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'size': 'size',
        'content_path': 'content_path',
    }

    def __init__(self, id=None, name=None, size=None, content_path=None):  # noqa: E501
        self._id = None
        self._name = None
        self._size = None
        self._content_path = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if size is not None:
            self.size = size
        if content_path is not None:
            self.content_path = content_path

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def content_path(self):
        return self._content_path

    @content_path.setter
    def content_path(self, content_path):

        self._content_path = content_path

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr in self.openapi_types.keys():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, File):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, File):
            return True

        return self.to_dict() != other.to_dict()
