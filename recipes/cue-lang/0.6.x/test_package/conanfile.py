from conan import ConanFile
from conan.errors import ConanException
from conan.tools.layout import basic_layout
from conan.tools.build import cross_building


class CueTestConan(ConanFile):
    settings = "os", "arch"
    generators = "VirtualBuildEnv", "VirtualRunEnv"
    apply_env = True
    test_type = "explicit"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def layout(self):
        basic_layout(self)

    def build(self):
        self.run("cue -h", env="conanbuild")

    def test(self):
        if cross_building(self):
            # JUst check cue is still on the path.
            self.run("which cue", env="conanrun")
        else:
            self.run("cue -h", env="conanrun")

