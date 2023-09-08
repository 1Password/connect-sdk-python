class OnePasswordConnectSDKError(RuntimeError):
    pass


class EnvironmentTokenNotSetException(OnePasswordConnectSDKError, TypeError):
    pass


class EnvironmentHostNotSetException(OnePasswordConnectSDKError, TypeError):
    pass


class FailedToRetrieveItemException(OnePasswordConnectSDKError):
    pass


class FailedToRetrieveVaultException(OnePasswordConnectSDKError):
    pass


class FailedToDeserializeException(OnePasswordConnectSDKError, TypeError):
    pass
