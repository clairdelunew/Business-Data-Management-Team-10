from setuptools import setup, find_packages

setup(
    name="my_spider",  # 项目名称
    version="1.0.0",  # 版本号
    packages=find_packages(),  # 自动发现 Python 包
    install_requires=[line.strip() for line in open("requirements.txt").readlines()],  # 自动读取 requirements.txt
    entry_points={
        "console_scripts": [
            "my_spider=my_spider.scrape:main"  # 让 my_spider 命令运行 scrape.py 里的 main() 函数
        ]
    },
    author="group10",
    author_email="your_email@example.com",
    description="A web crawler to scrape Panerai watch data.",
    python_requires=">=3.10.14",
)
