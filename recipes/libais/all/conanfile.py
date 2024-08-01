from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, copy

import os

required_conan_version = ">=1.43.0"


class LibAisConan(ConanFile):
    name = "libais"
    description = "Parses NMEA 0183 sentences into complete AIS messages."
    license = "Apache2.0"
    url = "https://github.com/schwehr/libais"
    exports_sources = "CMakeLists.txt"

    settings = "os", "arch", "compiler", "build_type"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def validate(self):
        # Check stdlib ABI compatibility
        if self.settings.compiler.libcxx != "libstdc++11":
            raise ConanInvalidConfiguration(f'Using {self.ref} requires "compiler.libcxx=libstdc++11"')
        
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
    
    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", dst=os.path.join(self.package_folder,"share"), src= self.source_folder, keep_path=False)
        copy(self, "**/ais.h", dst=os.path.join(self.package_folder, "include/libais"), src= self.source_folder, keep_path=False)
        copy(self, "**/vdm.h", dst=os.path.join(self.package_folder,"include/libais"), src= self.source_folder, keep_path=False)
        copy(self, "**/libais.a", dst=os.path.join(self.package_folder,"lib"), src=self.build_folder, keep_path=False)

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "libais")
        self.cpp_info.set_property("cmake_target_name", "libais::libais")
        self.cpp_info.libs = ["ais"]
