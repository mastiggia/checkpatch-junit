import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="checkpatch-junit",
    version="0.0.1",
    description="Provide JUnit output to Linux checkpatch.pl script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mastiggia/checkpatch-junit",
    license="GPLv3",
    license_file="LICENSE",
    author="Mastiggia",
    author_email="mastiggia@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Testing :: Unit",
    ],
    keywords="checkpatch, ci, junit",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6, <4",
    install_requires=["junit-xml>=1.9"],
    entry_points={
        "console_scripts": [
            "checkpatch-junit=checkpatch_junit.__init__:main",
        ],
    },
)
