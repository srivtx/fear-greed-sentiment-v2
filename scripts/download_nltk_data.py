#!/usr/bin/env python3
"""
Download required NLTK data for the Fear & Greed Sentiment Engine
"""

import nltk
import ssl
import sys

def download_nltk_data():
    """Download required NLTK data packages"""
    
    # Fix SSL certificate issues
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    print("🚀 Downloading NLTK data packages...")
    
    packages = ['vader_lexicon', 'punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
    
    for package in packages:
        try:
            print(f"📦 Downloading {package}...")
            result = nltk.download(package, quiet=False)
            if result:
                print(f"✅ {package} downloaded successfully")
            else:
                print(f"ℹ️  {package} already exists or download failed")
        except Exception as e:
            print(f"❌ Error downloading {package}: {e}")
    
    print("🎉 NLTK data download completed!")
    
    # Test VADER initialization
    try:
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
        print("✅ VADER sentiment analyzer initialized successfully!")
        
        # Test with a sample text
        test_text = "Bitcoin is going to the moon! This is very bullish!"
        scores = analyzer.polarity_scores(test_text)
        print(f"🧪 Test sentiment analysis: {scores}")
        
    except Exception as e:
        print(f"❌ Error initializing VADER: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = download_nltk_data()
    sys.exit(0 if success else 1)
