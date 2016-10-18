Project name : stock_analysis

Description  : filter stocks with strategy, get real time stock data, estimate stock strategy

Code language: python

python lib   : pandas, matplotlib, url2lib

Author       : zhu haofeng 271481778@qq.com


1 Environment Requirement

  Python 2.7.11 |Anaconda 4.0.0 (64-bit)

  https://www.continuum.io/downloads

2 python lib materials

  numpy http://old.sebug.net/paper/books/scipydoc/numpy_intro.html

  pandas http://pandas.pydata.org/pandas-docs/stable/10min.html

        http://pandas.pydata.org/pandas-docs/version/0.16.2/api.html

3 prepare stock history data for analysis

  setup 通达信金融终端 software

  http://www.pc6.com/softview/SoftView_142489.html
  
  All stocks history data can be download from this software

4 how to generate rsa-key for git env

  ssh-keygen -t rsa

  cat ~/.ssh/id_rsa.pub

5 how to checkout code with code command

  git init

  git pull git@github.com:redblader/stock_analysis.git

6 commit code with code command

  git add --> git commit --> git push
  
7 download folder (scripts and stocks history data files)
  
  "get_stock_data_from_storage.py" script can read stocks' history data from csv files (stored in storage folder ) which export from tongxinda software
  
  "get_realtime_stock_data.py" script can get real time stocks data with sina stock interface

8 analysis folder (strategy script)
  
  "u_curve_filter.py" which is introduced with Venus strategy, filter all stocks with U shape for nearest 5 days k-line of stocks, generate plot figure for result.
  
  
