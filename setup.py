from setuptools import setup, find_packages

setup(
    name="chigutiro",
    version="0.1.0",
    description="A high-performance pipeline for neurofunk audio analysis for identification and classification of track VIPs (Variation in Production) and Dubplates",
    author="Kundai Sachikonye",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "librosa",
        "madmom",
        "networkx",
        "matplotlib",
        "fastdtw",
        "scipy",
    ],
    python_requires=">=3.8",
)
