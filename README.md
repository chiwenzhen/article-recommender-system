# article-recommender-system
A python news classification system: collect articles and classifies articles

# Depenpendies
* [Anaconda](https://www.continuum.io/downloads#_windows) I choose Anaconda2-4.1.1-Windows-x86_64.exe (python 2.7)
* [MySQL-python](http://www.codegood.com/download/11/) I choose MySQL-python-1.2.3.win-amd64-py2.7.exe 
* gensim
* scikit-learn
* flask

# Main
1. crawlers to collect documents from web
2. perform word segment on these documents
3. train a text classifier on segmented documents
4. use flask to set up a website to demonstrate
