from setuptools import setup

setup(
    name='xaquan',
    version='1.0.0',
    description='安全教育平台api & 爬虫',
    url="https://github.com/lanmiemie/xaquan",
    author="Archerfish1114",
    author_email="archerfish1114@163.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="API sdk spider",
    install_requires=["requests", "lxml", "fake_useragent"],
    packages=["xaq"],
    project_urls={
        "Bug Reports": "https://github.com/lanmiemie/xaquan/issues",
        "Source": "https://github.com/lanmiemie/xaquan",
    },
)
