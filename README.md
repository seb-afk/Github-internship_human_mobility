# Where people stay - extracting destinations from GPS data
![](/images/readme_teaser.jpg)

This project contains a fast Python implementation of algorithms
proposed in [[1]](#hariharan2004) to extract so-called stop locations
from GPS data. The project also contains some sample data and a
detailed Jupyter notebook that showcases the work. You can explore the project in your browser by clicking on the "launch binder" button below and running the `Notebook for github latest edition.ipynb` Jupyter notebook.

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/sebastianbertoli/Github-internship_human_mobility/master)

## Prerequisites

What things you need to install. Also see `requirements.txt`.

```text
ipython                   5.1.0
joblib                    0.11
matplotlib                2.0.0
numpy                     1.11.3
pandas                    0.20.1
plotly                    2.2.2
scikit-learn              0.18.1
scipy                     0.18.1
```

## Authors

**Sebastian Bertoli** - [sebastianbertoli](https://github.com/sebastianbertoli)

## Acknowledgments

My thanks go to Marco de Nadai and Lorenzo Lucchini for their insights, guidance and code-fixes. 

## References

<a id='hariharan2004'></a> [1] Hariharan R., Toyama K. (2004) [Project Lachesis: Parsing and Modeling Location Histories.](https://link.springer.com/chapter/10.1007/978-3-540-30231-5_8#citeas) In: Egenhofer M.J., Freksa C., Miller H.J. (eds) Geographic Information Science. GIScience 2004. Lecture Notes in Computer Science, vol 3234. Springer, Berlin, Heidelberg

[2] Jing Yuan, Yu Zheng, Xing Xie, and Guangzhong Sun. Driving with knowledge from the physical world. In The 17th ACM SIGKDD international conference on Knowledge Discovery and Data mining, KDD’11, New York, NY, USA, 2011. ACM.

[3] Jing Yuan, Yu Zheng, Chengyang Zhang, Wenlei Xie, Xing Xie, Guangzhong Sun, and Yan Huang. T-drive: driving directions based on taxi trajectories. In Proceedings of the 18th SIGSPATIAL International Conference on Advances in Geographic Information Systems, GIS ’10, pages 99-108, New York, NY, USA,2010. ACM.
