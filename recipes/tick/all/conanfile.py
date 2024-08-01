from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import copy

import os


required_conan_version = ">=1.43.0"


class TickConan(ConanFile):
    name = "tick"
    license = "BSD 3-Clause 'New' or 'Revised'"
    url = "https://devops.shield.ai/ShieldAI/ThirdParty/_git/tick"
    homepage = "https://devops.shield.ai/ShieldAI/ThirdParty/_git/tick"
    description = "Trait introspection and concept creator for C++11."
    topics = ("C++11")
    settings = "os", "compiler", "build_type", "arch"

    exports_sources = ["CMakeLists.txt"]

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def source(self):
        git = Git(self, "tick")
        git.clone(url=self.conan_data["sources"][self.version]["url"], target=".")
        git.checkout(self.conan_data["sources"][self.version]["commit"])

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", dst="licenses", src=os.path.join(self.source_folder, "tick"))
        cmake = CMake(self)
        cmake.install()


    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "tick")
        self.cpp_info.set_property("cmake_target_name", "tick::tick")
        self.cpp_info.set_property("pkg_config_name", "tick")
