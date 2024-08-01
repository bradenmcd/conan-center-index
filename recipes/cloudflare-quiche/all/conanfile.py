import os

from conan import ConanFile
from conan.tools.files import copy, chdir
from conan.tools.system.package_manager import Apt
from conan.tools.scm import Git

class QUICHE(ConanFile):
    name="cloudflare-quiche"
    url="https://github.com/conan-io/conan-center-index"
    homepage="https://github.com/cloudflare/quiche"
    description="quiche is an implementation of the QUIC transport protocol and HTTP/3 as specified by the IETF"
    topics = ("cpp14", "cpp17", "quic", "udp")
    license="BSD-2"

    settings = "os", "build_type", "arch"
    no_copy_source = True

    exports_sources = "apps/*", "octets/*", "qlog/*", "quiche/*", "target/*", "Cargo.toml", "COPYING", "README.md", "quiche.svg"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def source(self):
        git = Git(self)
        git.clone(
            url=self.conan_data["sources"][self.version]["url"], 
            target=self._source_subfolder,
            args=["--recurse-submodules"]
            )
        git.folder = self._source_subfolder   
        git.checkout(self.conan_data["sources"][self.version]["tag"])

    def set_version(self):
        if not self.version:
            # This version comes from the quiche library
            self.version = "0.20.1"

    def build(self):
        build_dir = os.path.join(self.build_folder, self._build_subfolder)
        with chdir(self, os.path.join(self.source_folder, self._source_subfolder)):
            # "--features ffi" is needed since it enables the  "Foreign Function Interface",
            # which is a mechanism provided by Rust to interact with code written in other
            # languages, typically C or C++.
            self.run(f"cargo build --release --features ffi --target-dir {build_dir}")

    def package(self):
        src_dir = os.path.join(self.source_folder, self._source_subfolder)
        include_dir = os.path.join(src_dir, "quiche", "include")
        cargo_build_dir = os.path.join(self.build_folder, self._build_subfolder, "release")
        copy(self, "COPYING", src=src_dir, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "quiche.h", src=include_dir, dst=os.path.join(self.package_folder, "include"))
        copy(self, "*.so", src=cargo_build_dir, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.dylib", src=cargo_build_dir, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.a", src=cargo_build_dir, dst=os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "cloudflare-quiche"
        self.cpp_info.names["cmake_find_package_multi"] = "cloudflare-quiche"
        self.cpp_info.set_property("cmake_file_name", "cloudflare-quiche")

        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.libs = ["quiche"]
        self.cpp_info.includedirs = ["include"]
