from .. import *
from ..build.plat import *
from .utils import *


class MockPlatform(Platform):
    resources  = []
    connectors = []

    required_tools = []

    def toolchain_prepare(self, fragment, name, **kwargs):
        raise NotImplementedError


class PlatformTestCase(FHDLTestCase):
    def setUp(self):
        self.platform = MockPlatform()

    def test_add_file_str(self):
        self.platform.add_file("x.txt", "foo")
        self.assertEqual(self.platform.extra_files["x.txt"], "foo")

    def test_add_file_bytes(self):
        self.platform.add_file("x.txt", b"foo")
        self.assertEqual(self.platform.extra_files["x.txt"], b"foo")

    def test_add_file_exact_duplicate(self):
        self.platform.add_file("x.txt", b"foo")
        self.platform.add_file("x.txt", b"foo")

    def test_add_file_io(self):
        with open(__file__) as f:
            self.platform.add_file("x.txt", f)
        with open(__file__) as f:
            self.assertEqual(self.platform.extra_files["x.txt"], f.read())

    def test_add_file_wrong_filename(self):
        with self.assertRaises(TypeError,
                msg="File name must be a string, not 1"):
            self.platform.add_file(1, "")

    def test_add_file_wrong_contents(self):
        with self.assertRaises(TypeError,
                msg="File contents must be str, bytes, or a file-like object, not 1"):
            self.platform.add_file("foo", 1)

    def test_add_file_wrong_duplicate(self):
        self.platform.add_file("foo", "")
        with self.assertRaises(ValueError,
                msg="File 'foo' already exists"):
            self.platform.add_file("foo", "bar")
