from conan import ConanFile, tools
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout
from conan.tools.files import copy
from conan.tools.scm import Git
import os

required_conan_version = ">=2.0.0"

class OrtoolsConan(ConanFile):
    name = "ortools"
    url = "https://github.com/google/or-tools"
    description = "Google's software suite for combinatorial optimization."

    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "USE_SCIP": [True, False],
        "USE_COINOR": [True, False],
        "USE_GLPK": [True, False],
        "USE_CPLEX": [True, False],
        "USE_XPRESS": [True, False],
    }
    default_options = {
        # ShieldAI change - default to shared lib due to issue
        # on arm described here https://statics.gov.teams.microsoft.us/evergreen-assets/safelinks/1/atp-safelinks.html
        "shared": True,
        "fPIC": True,
        "USE_SCIP": False, #NOTE: SCIP license is not for commercial use
        "USE_COINOR": False,
        "USE_GLPK": False,
        "USE_CPLEX": False,
        "USE_XPRESS": False
    }

    def requirements(self):
        self.requires("abseil/20200923.3", transitive_headers=True)
        self.requires("zlib/1.3.1")
        self.requires("protobuf/3.21.9", transitive_headers=True)
        self.requires("glog/0.4.0")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def export_sources(self):
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["BUILD_DEPS"] = False
        tc.variables["BUILD_SAMPLES"] = False
        tc.variables["BUILD_EXAMPLES"] = False
        tc.variables["USE_SCIP"] = self.options.USE_SCIP
        tc.variables["USE_COINOR"] = self.options.USE_COINOR
        tc.variables["USE_GLPK"] = self.options.USE_GLPK
        tc.variables["USE_CPLEX"] = self.options.USE_CPLEX
        tc.variables["USE_XPRESS"] = self.options.USE_XPRESS

        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        git = Git(self)
        git.clone(url=self.conan_data["sources"][self.version]["url"], target="source_subfolder")
        git.folder = "source_subfolder"     
        git.checkout(self.conan_data["sources"][self.version]["tag"])

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = CMake(self)
        cmake.install()
        tools.files.rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "ortools"
        self.cpp_info.set_property("cmake_file_name", "ortools")
        self.cpp_info.set_property("cmake_target_name", "ortools::ortools")
        self.cpp_info.set_property("pkg_config_name", "ortools")
        self.cpp_info.libs = ["ortools"]
        self.cpp_info.cxxflags = ["-DUSE_BOP", "-DUSE_GLOP"]
        self.cpp_info.system_libs = ["dl", "pthread"]
