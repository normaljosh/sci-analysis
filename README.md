# sci-analysis
An easy to use python based data exploration and analysis tool by Chris Morrow

## Current Version:
1.4 --- Released August 19, 2016

### What is sci-analysis?
sci-analysis is a python package for performing quickly performing statistical data analysis. It provides a graphical representation of the supplied data as well as the statistical analysis. sci-analysis is smart enough to determine the correct analysis and tests to perform based on the shape of the data you provide, as well as how the data is distributed.

Currently, sci-analysis can only be used for analyzing numeric data. Categorical data analysis is planned for a future version. The three types of analysis that can be performed are histograms of single vectors, correlation between two vectors and one-way ANOVA.

### What's new in sci-analysis version 1.4?

In version 1.4, sci-analysis was re-written to be more pythonic and to support python 3. A ton of new graphing options have been added histograms, scatter plots and oneway plots. Histograms can now display an accompanying cumulative distribution plot and fit lines to a specified distribution can be displayed on both the histogram and cumulative distribution plot. Scatter plots can now overlay density contour lines and display boxplot borders. Boxplots have been revamped and are now overlayed on top of a kernel density estimation, which provides a much better representation of distribution density. New tests have been added for comparing two distributions -- Student's T Test for normally distributed data, the Mann Whitney U Test for non-parametric data and the two-sample Kolmogorov-Smirnov Test for small non-parametric samples. The Kolmogorov-Smirnov Test has been added for determining goodness-of-fit to a specified distribution as well. 

### Getting started with sci-analysis
The documentation on how to install and use sci-analysis can be found here:

http://sci-analysis.readthedocs.io/en/latest/

