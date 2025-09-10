"""
Setup script for Facebook Messenger Bot
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="facebook-messenger-bot",
    version="1.0.0",
    author="Smart Chat Bot Team",
    author_email="",
    description="Browser automation chatbot for Facebook Messenger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Will100001/Smart-chat-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    keywords="facebook messenger bot automation selenium chatbot",
    project_urls={
        "Bug Reports": "https://github.com/Will100001/Smart-chat-bot/issues",
        "Source": "https://github.com/Will100001/Smart-chat-bot",
    },
)