from pydantic import (
    StrictBool,
    StrictInt,
    StrictStr,
    constr,
    validator,
)
from yt_shared.enums import DownMediaType
from yt_shared.schemas.base import RealBaseModel

_LANG_CODE_LEN = 2
_LANG_CODE_REGEX = rf'^[a-z]{{{_LANG_CODE_LEN}}}$'


class AnonymousUserSchema(RealBaseModel):
    id: StrictInt

    @property
    def is_anonymous_user(self) -> bool:
        return True


class VideoCaptionSchema(RealBaseModel):
    include_title: StrictBool
    include_filename: StrictBool
    include_link: StrictBool
    include_size: StrictBool


class UploadSchema(RealBaseModel):
    upload_video_file: StrictBool
    upload_video_max_file_size: StrictInt
    forward_to_group: StrictBool
    forward_group_id: StrictInt | None
    silent: StrictBool
    video_caption: VideoCaptionSchema


class UserSchema(AnonymousUserSchema):
    send_startup_message: StrictBool
    download_media_type: DownMediaType
    save_to_storage: StrictBool
    use_url_regex_match: StrictBool
    upload: UploadSchema

    @property
    def is_anonymous_user(self) -> bool:
        return False


def _change_type(values: list[int]) -> list[AnonymousUserSchema]:
    return [AnonymousUserSchema(id=id_) for id_ in values]


class ApiSchema(RealBaseModel):
    upload_video_file: StrictBool
    upload_video_max_file_size: StrictInt
    upload_to_chat_ids: list[AnonymousUserSchema]
    silent: StrictBool
    video_caption: VideoCaptionSchema

    _transform_chat_ids = validator('upload_to_chat_ids', pre=True)(_change_type)


class TelegramSchema(RealBaseModel):
    api_id: StrictInt
    api_hash: StrictStr
    token: StrictStr
    lang_code: constr(regex=_LANG_CODE_REGEX, to_lower=True)
    max_upload_tasks: StrictInt
    url_validation_regexes: list[str]
    allowed_users: list[UserSchema]
    api: ApiSchema


class YtdlpSchema(RealBaseModel):
    version_check_enabled: StrictBool
    version_check_interval: StrictInt
    notify_users_on_new_version: StrictBool


class ConfigSchema(RealBaseModel):
    telegram: TelegramSchema
    ytdlp: YtdlpSchema
