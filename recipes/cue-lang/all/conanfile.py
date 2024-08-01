import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration, ConanException
from conan.tools.files import get, copy


required_conan_version = ">=1.52.0"


class CUELangConan(ConanFile):
    name = "cue-lang"
    description = "CUE is an open source language, with a rich set of APIs and tooling, for defining, generating, and validating all kinds of data: configuration, APIs, database schemas, code, … you name it."
    settings = "os", "arch"
    package_type = "application"

    _supported_arch = {
        "x86_64": "amd64", 
        "armv8": "arm64",
        "armv8.3": "arm64",
    }

    def validate(self):
        if self.info.settings.os != "Linux":
            raise ConanInvalidConfiguration("Cue is currently only pacakged for Linux.")
            
        if self.version not in self.conan_data["artifacts"] and self._supported_arch[str(self.info.settings.arch)] not in self.conan_data["artifacts"][self.version]:
            raise ConanInvalidConfiguration("Not artifacts for current version and arch.")

    def build(self):
        data = self.conan_data["artifacts"][self.version][self._supported_arch[str(self.info.settings.arch)]]

        get(self, **data, destination="cue_root", strip_root=False)

    def package(self):
        copy(self, "cue", os.path.join(self.build_folder, "cue_root"), os.path.join(self.package_folder, "bin"))
