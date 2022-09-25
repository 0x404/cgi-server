"""setting"""
import os
from cgiserver.utils import AttrDict, html_file_loader
from cgiserver.logging import get_logger


LOGGER = get_logger()


class Setting(AttrDict):
    """Setting class to restore all backend settings"""

    def check_setting(self, key):
        """check whether key is in setting and make default key setting"""
        if key not in self:
            super().__setattr__(key, Setting.default_setting(key))
            warning_msg = (
                f"setting {key} is not set by user, default to '{self[key]}'."
                f"If you want to modify this setting, use `GLOBAL_SETTING.{key} = yoursetting`."
            )
            LOGGER.warning(warning_msg)
        elif os.path.isfile(self[key]):
            super().__setattr__(key, html_file_loader(self[key]))
            info_msg = f"detecting GLOBAL_SETTING.{key} is a template path, automatically load."
            LOGGER.info(info_msg)

    @staticmethod
    def default_setting(key):
        """default settings"""
        default = {
            "template_400": "Bad request syntax or unsupported method",
            "template_403": "Request forbidden",
            "template_404": "Nothing matches the given URI",
        }
        return default[key]
