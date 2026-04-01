class OnePasswordConnectSDKError(RuntimeError):
    pass


class EnvironmentTokenNotSetException(OnePasswordConnectSDKError, TypeError):
    pass


class EnvironmentHostNotSetException(OnePasswordConnectSDKError, TypeError):
    pass


class FailedToRetrieveItemException(OnePasswordConnectSDKError):
    def __init__(self, message, *, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class FailedToRetrieveVaultException(OnePasswordConnectSDKError):
    pass


class FailedToDeserializeException(OnePasswordConnectSDKError, TypeError):
    pass
