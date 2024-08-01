from conan import ConanFile
from conan.tools.files import get, copy

import re, os

required_conan_version = ">=2.0.0"


class HashicorpSerf(ConanFile):
    name = "hashicorp-serf"
    description = "Parses NMEA 0183 sentences into complete AIS messages."
    license = "Mozilla Public License, version 2.0"
    package_type = "application"
    url = "https://www.serf.io/"

    settings = "os", "arch"

    options = {}
    default_options = {}
            

    def source(self):
        for data in self.conan_data["sources"][self.version]:
            url = data["url"]
            match = re.search(r'([^_]+)\.zip$', url)
            if match:
                arch_dir = match.group(1)
            else:
                arch_dir = "No match found"

            get(self, url, destination=arch_dir, keep_permissions=True)

    def package(self):
        if 'x86' in self.settings.arch:
            dir = 'amd64'
        elif 'arm' in self.settings.arch:
            dir = 'arm'

        copy(self, "serf", dst=os.path.join(self.package_folder, "bin"), src=dir, keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.frameworkdirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = []

        # TODO: Legacy, to be removed on Conan 2.0
        bin_dir = os.path.join(self.package_folder, "bin")
        self.env_info.PATH.append(bin_dir)
