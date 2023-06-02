from fastapi_jsonrpc import BaseError


class UserExistsError(BaseError):
    CODE = -32001
    MESSAGE = 'User already exists'


class NoUserError(BaseError):
    CODE = -32002
    MESSAGE = 'User does not exists'


class AuthError(BaseError):
    CODE = -32003
    MESSAGE = 'Unauthorized'


class NoVideoError(BaseError):
    CODE = -32004
    MESSAGE = 'No video'


class WrongDataError(BaseError):
    CODE = -32005
    MESSAGE = 'Enter correct data'


class UploadError(BaseError):
    CODE = -32006
    MESSAGE = 'Error while loading an object'


class NoCommentError(BaseError):
    CODE = -32007
    MESSAGE = 'No Comment'


class NoAdminError(BaseError):
    CODE = -32008
    MESSAGE = 'User is not admin'



