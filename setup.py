from setuptools import setup, find_packages

setup(
    name="fear_greed_engine",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.23.0",
        "pandas>=1.5.0",
        "scikit-learn>=1.2.0",
        "nltk>=3.8.0",
        "tweepy>=4.14.0",
        "praw>=7.7.0",
        "newsapi-python>=0.2.7",
        "yfinance>=0.2.18",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "textblob>=0.17.0",
        "vaderSentiment>=3.3.0",
        "tqdm>=4.65.0",
        "requests>=2.28.0"
    ],
    entry_points={
        'console_scripts': [
            'fear_greed=main:main',
        ],
    },
    author="GoQuant Developer",
    author_email="dev@goquant.io",
    description="Fear & Greed Sentiment Engine for market analysis",
    keywords="sentiment, trading, finance, crypto, stocks",
    python_requires=">=3.8",
)