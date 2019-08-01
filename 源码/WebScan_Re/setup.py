from setuptools import setup, find_packages

setup(
 name = "WebScan",
 version = "1.2",

 packages = find_packages(),
 include_package_data = True,
 install_requires = ["requests"],

 scripts = ["WebScan.py"],
package_data={'': ['*.json'],}
)
