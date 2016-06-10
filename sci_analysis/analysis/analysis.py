"""Module: analysis.py
Classes:
    Analysis - Generic analysis root class.
    Test - Generic statistical test class.
    GroupTest - Perform a test on multiple vectors that are passed as a tuple of arbitrary length.
    Comparison - Perform a test on two independent vectors of equal length.
    NormTest - Tests for whether data is normally distributed or not.
    GroupNormTest - Tests a group of data to see if they are normally distributed or not.
    TTest - Performs a T-Test on the two provided vectors.
    LinearRegression - Performs a linear regression between two vectors.
    Correlation - Performs a pearson or spearman correlation between two vectors.
    Anova - Performs a one-way ANOVA on a group of vectors.
    Kruskal - Performs a non-parametric Kruskal-Wallis test on a group of vectors.
    EqualVariance - Checks a group of vectors for equal variance.
    VectorStatistics - Reports basic summary stats for a provided vector.
    GroupStatistics - Reports basic summary stats for a group of vectors.
Functions:
    analyze - Magic method for performing quick data analysis.
"""
# Python3 compatability
from __future__ import absolute_import
from __future__ import print_function

# Scipy imports
from scipy.stats import linregress, shapiro, pearsonr, spearmanr, ttest_ind, \
    ttest_1samp, f_oneway, kruskal, bartlett, levene, skew, kurtosis, kstest, sem

# Numpy imports
from numpy import concatenate, mean, std, median, amin, amax, percentile

# Local imports
from ..data.vector import Vector
from ..operations.data_operations import is_dict, is_iterable, is_vector, is_group,\
    is_dict_group, drop_nan, drop_nan_intersect
from ..graphs.graph import GraphHisto, GraphScatter, GraphBoxplot


class Analysis(object):
    """Generic analysis root class.

    Members:
        _data - the data used for analysis.
        _display - flag for whether to display the analysis output.
        _results - A dict of the results of the test.

    Methods:
        logic - This method needs to run the analysis, set the results member, and display the output at bare minimum.
        run - This method should return the results of the specific analysis.
        output - This method shouldn't return a value and only produce a side-effect.
    """

    _name = "Analysis"

    def __init__(self, data, display=True):
        """Initialize the data and results members.

        Override this method to initialize additional members or perform
        checks on data.
        """
        self._data = data
        self._display = display
        self._results = {}

    @property
    def name(self):
        """The name of the test class"""
        return self._name

    @property
    def data(self):
        """The data used for analysis"""
        return self._data

    @property
    def results(self):
        """A dict of the results returned by the run method"""
        return self._results

    def data_prep(self, data):
        """Prepare the data for analysis"""
        pass

    def logic(self):
        """This method needs to run the analysis, set the results member, and
        display the output at bare minimum.

        Override this method to modify the execution sequence of the analysis.
        """
        if not self._data:
            pass
        self.run()
        if self._display:
            str(self)

    def run(self):
        """This method should perform the specific analysis and set the results dict.

        Override this method to perform a specific analysis or calculation.
        """
        pass

    def output(self):
        """This method shouldn't return a value and only produce a side-effect.

        Override this method to write the formatted output to std out.
        """
        print(str(self.__class__))
        pass

    def __str__(self):
        return self.output()

    def __repr__(self):
        return self.output()


class Test(Analysis):
    """Generic statistical test class.
    Members:
        _name - The name of the test.
        _h0 - Prints the null hypothesis.
        _ha - Prints the alternate hypothesis.
        _data - the data used for analysis.
        _display - flag for whether to display the analysis output.
        _alpha - the statistical significance of the test.
        _results - A dict of the results of the test.
    Methods:
        logic - If the result is greater than the significance, print the null hypothesis, otherwise,
            the alternate hypothesis.
        run - This method should return the results of the specific analysis.
        output - This method shouldn't return a value and only produce a side-effect.
    """

    _name = "Test"
    _statistic_name = "test"
    _h0 = "H0: "
    _ha = "HA: "
    _min_size = 2

    def __init__(self, *args, **kwargs):
        """Initialize the object"""

        self._alpha = kwargs['alpha'] if 'alpha' in kwargs else 0.05
        data = self.data_prep(args) if is_group(args) else self.data_prep(*args)
        if len(data) <= 1:
            try:
                data = data[0]
            except IndexError:
                pass

        # set the _data and _display members
        super(Test, self).__init__(data, display=(kwargs['display'] if 'display' in kwargs else True))

        # Run the test and display the results
        self.logic()

    @property
    def statistic(self):
        """The test statistic returned by the function called in the run method"""
        try:
            return self._results['statistic']
        except KeyError:
            return float("nan")

    @property
    def p_value(self):
        """The p-value returned by the function called in the run method"""
        try:
            return self._results['p_value']
        except KeyError:
            return float("nan")

    def data_prep(self, data):
        clean_list = list()
        for d in data:
            if not is_iterable(d):
                try:
                    clean_list.append(float(d))
                except (ValueError, TypeError):
                    continue
            else:
                v = drop_nan(d) if is_vector(d) else drop_nan(Vector(d))
                if v.is_empty() or len(v) <= self._min_size:
                    continue
                clean_list.append(v)
        return clean_list

    def output(self):
        """Print the results of the test in a user-friendly format"""
        return "\n".join((
            ' ',
            self._name,
            '-' * len(self._name),
            ' ',
            self._statistic_name + " = " + "{:.4f}".format(self.statistic),
            "p value = " + "{:.4f}".format(self.p_value),
            " ",
            # If the result is greater than the significance, print the null
            # hypothesis, otherwise, the alternate hypothesis
            self._h0 if self.p_value > self._alpha else self._ha,
            " "
        ))


class Comparison(Test):
    """Perform a test on two independent vectors of equal length."""

    def data_prep(self, data):
        """Prepare the data for analysis"""
        xdata = data[0] if is_vector(data[0]) else Vector(data[0])
        ydata = data[1] if is_vector(data[1]) else Vector(data[1])
        if len(xdata) != len(ydata):
            pass
        elif len(xdata) <= self._min_size or len(xdata) <= self._min_size:
            pass
        elif xdata.is_empty() or ydata.is_empty():
            pass
        else:
            xdata, ydata = drop_nan_intersect(xdata, ydata)
        return [xdata, ydata]

    @property
    def xdata(self):
        """The predictor vector for comparison tests"""
        return self.data[0]

    @property
    def ydata(self):
        """The response vector for comparison tests"""
        return self.data[1]

    @property
    def predictor(self):
        """The predictor vector for comparison tests"""
        return self.data[0]

    @property
    def response(self):
        """The response vector for comparison tests"""
        return self.data[1]


class NormTest(Test):
    """Tests for whether data is normally distributed or not."""

    _name = "Shapiro-Wilk test for normality"
    _statistic_name = "W value"
    _h0 = "H0: Data is normally distributed"
    _ha = "HA: Data is not normally distributed"

    def run(self):
        if not is_group(self._data):
            w_value, p_value = shapiro(self.data)
        else:
            w_value = list()
            p_value = list()
            for d in self._data:
                _w, _p = shapiro(d)
                w_value.append(_w)
                p_value.append(_p)
            min_p = min(p_value)
            w_value = w_value[p_value.index(min_p)]
            p_value = min_p
        self._results.update({'statistic': w_value, 'p_value': p_value})


class KSTest(Test):
    """Tests whether data comes from a specified distribution or not."""

    _name = "Kolmogorov-Smirnov Test"
    _statistic_name = 'D value'

    def __init__(self, data, distribution='norm', parms=(), alpha=0.05, display=True):
        self._distribution = distribution
        self._parms = parms
        self._h0 = "H0: Data is matched to the " + self.distribution + " distribution"
        self._ha = "HA: Data is not from the " + self.distribution + " distribution"
        super(KSTest, self).__init__(data, alpha=alpha, display=display)

    def run(self):
        args = [self._data, self._distribution]
        if self._parms:
            args.append(self._parms)
        d_value, p_value = kstest(*args)
        self._results.update({'statistic': d_value, 'p_value': p_value})

    @property
    def distribution(self):
        """Return the distribution that data is being compared against"""
        return self._distribution


class TTest(Test):
    """Performs a T-Test on the two provided vectors."""

    _name = {'1_sample': '1 Sample T Test', 't_test': 'T Test', 'welch_t': "Welch's T Test"}
    _statistic_name = 't value'
    _h0 = "H0: Means are matched"
    _ha = "HA: Means are significantly different"

    def __init__(self, xdata, ydata, alpha=0.05, display=True):
        self._mu = None
        if not is_iterable(ydata):
            self._mu = float(ydata)
            super(TTest, self).__init__(xdata, alpha=alpha, display=display)
        else:
            super(TTest, self).__init__(xdata, alpha=alpha, display=display)

    def run(self):
        if self._mu:
            t, p = ttest_1samp(self._data, self._mu)
            test = "1_sample"
        else:
            if EqualVariance(*self._data, display=False, alpha=self._alpha).p_value > self._alpha:
                t, p = ttest_ind(*self._data, equal_var=True)
                test = 't_test'
            else:
                t, p = ttest_ind(*self._data, equal_var=False)
                test = 'welch_t'
        self._results.update({'p_value': p, 't_value': t, 'test': test})

    def output(self):
        return "\n".join((
            ' ',
            self._name[self._results['test']],
            '-' * len(self._name[self._results['test']]),
            ' ',
            self._statistic_name[self._results['test']] + " = " + "{:.4f}".format(self._results['t_value']),
            "p value = " + "{:.4f}".format(self.p_value),
            " ",
            # If the result is greater than the significance, print the null
            # hypothesis, otherwise, the alternate hypothesis
            self._h0 if self.p_value > self._alpha else self._ha,
            " "
        ))


class LinearRegression(Comparison):
    """Performs a linear regression between two vectors."""

    _min_size = 3
    _name = "Linear Regression"
    _h0 = "H0: There is no significant relationship between predictor and response"
    _ha = "HA: There is a significant relationship between predictor and response"

    def run(self):
        slope, intercept, r2, p_value, std_err = linregress(self.xdata, self.xdata)
        count = len(self.xdata)
        self._results.update({'count': count,
                              'slope': slope,
                              'intercept': intercept,
                              'r2': r2,
                              'std_err': std_err,
                              'p_value': p_value})

    def output(self):
        return "\n".join((
            " ",
            self._name,
            "-" * len(self._name),
            " ",
            "count     = " + str(self.results['count']),
            "slope     = " + "{:.4f}".format(self.results['slope']),
            "intercept = " + "{:.4f}".format(self.results['intercept']),
            "R^2       = " + "{:.4f}".format(self.results['r2']),
            "std err   = " + "{:.4f}".format(self.results['std_err']),
            "p value   = " + "{:.4f}".format(self.results['p_value']),
            " ",
            self._h0 if self.p_value > self._alpha else self._ha,
            " "
        ))


class Correlation(Comparison):
    """Performs a pearson or spearman correlation between two vectors."""

    _min_size = 3
    _name = 'Correlation'
    _statistic_name = 'r value'
    _h0 = "H0: There is no significant relationship between predictor and response"
    _ha = "HA: There is a significant relationship between predictor and response"

    def run(self):
        if NormTest(concatenate([self.xdata, self.ydata]), display=False, alpha=self._alpha).p_value > self._alpha:
            r_value, p_value = pearsonr(self.xdata, self.ydata)
            r = "pearson"
        else:
            r_value, p_value = spearmanr(self.xdata, self.ydata)
            r = "spearman"
        self._results.update({'r_value': r_value, 'p_value': p_value, 'type': r})

    def output(self):
        return "\n".join((
            " ",
            self.name,
            "-" * len(self.name),
            " ",
            "Pearson Coeff: " if self.results['type'] == "pearson" else "Spearman Coeff: ",
            "r value = " + "{:.4f}".format(self.results['r_value']),
            "p value = " + "{:.4f}".format(self.results['p_value']),
            " ",
            self._h0 if self.p_value > self._alpha else self._ha,
            " "
        ))


class Anova(Test):
    """Performs a one-way ANOVA on a group of vectors."""

    _name = "Oneway ANOVA"
    _statistic_name = 'f value'
    _h0 = "H0: Group means are matched"
    _ha = "HA: Group means are not matched"

    def run(self):
        f_value, p_value = f_oneway(*self.data)
        self._results.update({'p_value': p_value, 'f_value': f_value})

    @property
    def f_value(self):
        """The f value returned by the ANOVA f test"""
        return self._results['f_value']


class Kruskal(Test):
    """Performs a non-parametric Kruskal-Wallis test on a group of vectors."""

    _name = "Kruskal-Wallis"
    _statistic_name = 'H value'
    _h0 = "H0: Group means are matched"
    _ha = "HA: Group means are not matched"

    def run(self):
        h_value, p_value = kruskal(*self.data)
        self._results.update({'p_value': p_value, 'h_value': h_value})

    @property
    def h_value(self):
        """The h value returned by the Kruskal test"""
        return self._results['h_value']


class EqualVariance(Test):
    """Checks a group of vectors for equal variance."""

    _name = {'Bartlett': 'Bartlett Test', 'Levene': 'Levene Test'}
    _statistic_name = {'Bartlett': 'T value', 'Levene': 'W value'}
    _h0 = "H0: Variances are equal"
    _ha = "HA: Variances are not equal"

    def run(self):
        if len(self._data) < self._min_size:
            pass
        if NormTest(*self._data, display=False, alpha=self._alpha).p_value > self._alpha:
            statistic, p_value = bartlett(*self._data)
            test = 'Bartlett'
        else:
            statistic, p_value = levene(*self._data)
            test = 'Levene'
        self._results.update({'p_value': p_value, 'statistic': statistic, 'test': test})

    def output(self):
        return "\n".join((
            ' ',
            self._name[self._results['test']],
            '-' * len(self._name[self._results['test']]),
            ' ',
            self._statistic_name[self._results['test']] + " = " + "{:.4f}".format(self.statistic),
            "p value = " + "{:.4f}".format(self.p_value),
            # If the result is greater than the significance, print the null
            # hypothesis, otherwise, the alternate hypothesis
            " ",
            self._h0 if self.p_value > self._alpha else self._ha,
            " "
        ))


class VectorStatistics(Analysis):
    """Reports basic summary stats for a provided vector."""

    _min_size = 2
    _name = 'Statistics'

    def __init__(self, data, sample=True, display=True):
        self._sample = sample
        super(VectorStatistics, self).__init__(self.data_prep(data), display=display)
        self.logic()

    def data_prep(self, data):
        v = drop_nan(data) if is_vector(data) else drop_nan(Vector(data))
        return None if v.is_empty() or len(v) < self._min_size else v

    def run(self):
        dof = 0
        if self._sample:
            dof = 1
        count = len(self._data)
        avg = mean(self._data)
        sd = std(self._data, ddof=dof)
        error = sem(self._data, 0, dof)
        med = median(self._data)
        vmin = amin(self._data)
        vmax = amax(self._data)
        vrange = vmax - vmin
        sk = skew(self._data)
        kurt = kurtosis(self._data)
        q1 = percentile(self._data, 25)
        q3 = percentile(self._data, 75)
        iqr = q3 - q1
        self._results = {"count": count,
                         "mean": avg,
                         "std": sd,
                         "error": error,
                         "median": med,
                         "min": vmin,
                         "max": vmax,
                         "range": vrange,
                         "skew": sk,
                         "kurtosis": kurt,
                         "q1": q1,
                         "q3": q3,
                         "iqr": iqr}

    def output(self):
        return "\n".join((
            " ",
            self._name,
            "-" * len(self._name),
            " ",
            "Count     = " + str(self._results["count"]),
            "Mean      = " + "{:.4f}".format(self._results['mean']),
            "Std Dev   = " + "{:.4f}".format(self._results['std']),
            "Std Error = " + "{:.4f}".format(self._results['error']),
            "Skewness  = " + "{:.4f}".format(self._results['skew']),
            "Kurtosis  = " + "{:.4f}".format(self._results['kurtosis']),
            "Max       = " + "{:.4f}".format(self._results['max']),
            "75%       = " + "{:.4f}".format(self._results['q3']),
            "50%       = " + "{:.4f}".format(self._results['median']),
            "25%       = " + "{:.4f}".format(self._results['q1']),
            "Min       = " + "{:.4f}".format(self._results['min']),
            "IQR       = " + "{:.4f}".format(self._results['iqr']),
            "Range     = " + "{:.4f}".format(self._results['range'])
        ))


class GroupStatistics(Analysis):
    """Reports basic summary stats for a group of vectors."""

    _min_size = 1
    _name = 'Group Statistics'

    def __init__(self, data, groups=None, display=True):
        if not is_dict(data):
            data = dict(zip(groups, data)) if groups else dict(zip(list(range(1, len(data) + 1)), data))
        super(GroupStatistics, self).__init__(self.data_prep(data), display=display)
        self.logic()

    def data_prep(self, data):
        clean_data = dict()
        for i, d in data.items():
            if len(d) == 0:
                continue
            else:
                if not is_vector(d):
                    v = Vector(d)
                if len(v) < self._min_size:
                    continue
                clean_data.update({i: drop_nan(v)})
        return clean_data

    def logic(self):
        if not self._data:
            pass
        self._results = list()
        self.run()
        if self._display:
            str(self)

    def run(self):
        for group, vector in self._data.items():
            count = len(vector)
            avg = mean(vector)
            sd = std(vector, ddof=1)
            vmax = amax(vector)
            vmin = amin(vector)
            q2 = median(vector)
            row_result = {"group": group,
                          "count": count,
                          "mean": avg,
                          "std": sd,
                          "max": vmax,
                          "median": q2,
                          "min": vmin}
            self._results.append(row_result)

    def output(self):
        size = 12
        header = ""
        line = ""
        rows = list()
        offset = 0
        shift = False
        spacing = "{:.5f}"
        labels = ["Count", "Mean", "Std.", "Min", "Q2", "Max", "Group"]

        for s in labels:
            header = header + s + " " * (size - len(s))
        for v in self._results:
            stats = [str(v["count"]),
                     spacing.format(v["mean"]),
                     spacing.format(v["std"]),
                     spacing.format(v["min"]),
                     spacing.format(v["median"]),
                     spacing.format(v["max"]),
                     str(v["group"])
                     ]
            for i, s in enumerate(stats):
                if offset == 1 or shift:
                    offset = -1
                    shift = False
                else:
                    offset = 0
                try:
                    if stats[i + 1][0] == "-":
                        if offset == -1:
                            offset = 0
                            shift = True
                        else:
                            offset = 1
                    line = line + s + " " * (size - offset - len(s))
                except IndexError:
                    line = line + s + " " * (size - offset - len(s))
            rows.append(line)
            line = ""
        rows = "\n".join(rows)
        return "\n".join((
            " ",
            self._name,
            " ",
            header,
            "-" * len(header),
            rows,
            " "
        ))


def analyze(
        xdata,
        ydata=None,
        groups=None,
        name=None,
        xname=None,
        yname=None,
        alpha=0.05,
        categories='Categories'):
    """Magic method for performing quick data analysis.

    :param xdata: A Vector, numPy Array or sequence like object
    :param ydata: An optional secondary Vector, numPy Array or sequence object
    :param groups: A list of group names. The box plots will be graphed in order of groups
    :param name: The response variable label
    :param xname: The predictor variable (x-axis) label
    :param yname: The response variable (y-axis) label
    :param alpha: The significance level of the test
    :param categories: The x-axis label when performing a group analysis
    :return: A tuple of xdata and ydata
    """

    # Compare Group Means and Variance
    if is_group(xdata) or is_dict_group(xdata):
        if is_dict(xdata):
            groups = list(xdata.keys())
            xdata = list(xdata.values())

        # Apply the y data label
        if yname:
            yname = yname
        elif name:
            yname = name
        else:
            yname = 'Values'

        # Apply the x data label
        if xname:
            label = xname
        else:
            label = categories

        # Show the box plot and stats
        GraphBoxplot(xdata, groups, label, yname=yname)
        GroupStatistics(xdata, groups)
        p = EqualVariance(*xdata).results[0]

        # If normally distributed and variances are equal, perform one-way ANOVA
        # Otherwise, perform a non-parametric Kruskal-Wallis test
        if NormTest(*xdata, display=False, alpha=alpha).results[0] > alpha and p > alpha:
            if len(xdata) == 2:
                TTest(xdata[0], xdata[1])
            else:
                Anova(*xdata)
        else:
            if len(xdata) == 2:
                TTest(xdata[0], xdata[1])
            else:
                Kruskal(*xdata)
        pass

    # Correlation and Linear Regression
    elif is_iterable(xdata) and is_iterable(ydata):

        # Apply the x data label
        label = 'Predictor'
        if xname:
            label = xname

        # Apply the y data label
        if yname:
            yname = yname
        elif name:
            yname = name
        else:
            yname = 'Response'

        # Convert xdata and ydata to Vectors
        if not is_vector(xdata):
            xdata = Vector(xdata)
        if not is_vector(ydata):
            ydata = Vector(ydata)

        # Show the scatter plot, correlation and regression stats
        GraphScatter(xdata, ydata, label, yname)
        LinearRegression(xdata, ydata)
        Correlation(xdata, ydata)
        pass

    # Histogram and Basic Stats
    elif is_iterable(xdata):

        # Apply the data label
        label = 'Data'
        if name:
            label = name
        elif xname:
            label = xname

        # Convert xdata to a Vector
        if not is_vector(xdata):
            xdata = Vector(xdata)

        # Show the histogram and stats
        GraphHisto(xdata, name=label)
        VectorStatistics(xdata)
        NormTest(xdata, alpha=alpha)
        pass
    else:
        return xdata, ydata
