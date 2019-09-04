#! /usr/bin/python

import sys
import re
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import argparse
from argparse import ArgumentParser

g_colors = ['red', 'blue', 'green', 'orange', 'brown', 'cyan']
g_markers = ['o', 'x', '^', '*', 'h', 'v']

def plot_results(wer_results, ax, keys=None, legend_loc=0, ylim=(27.5,33.5)):
    i = 0
    ax.hlines(30.6, 0, 1, color='black', linestyle='dashed')#, label='Baseline\_dev')
    ax.hlines(33.3, 0, 1, color='black', label='Baseline')# + '\_eval')

    for result_id, wer_result_lines in wer_results.items():
        if keys is not None and result_id not in keys:
            continue

        betas = []
        dev_wers = []
        eval_wers = []
        for line in wer_result_lines.split('\n'):
            parts = line.strip().split()
            if len(parts) == 0:
                continue
            assert len(parts) == 7

            betas.append(float(parts[-3]))
            dev_wers.append(float(parts[-2]))
            eval_wers.append(float(parts[-1]))

        if keys is None:
            label = result_id
        else:
            label = keys[result_id]

        ax.plot(betas, dev_wers, marker=g_markers[i], color=g_colors[i], linestyle='dashed') #, label=result_id + '\_dev')
        ax.plot(betas, eval_wers, marker=g_markers[i], color=g_colors[i], label=label)# + '\_eval')

        i += 1

    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_ylabel('WER (\%)')
    ax.set_xlabel(r'$\beta$')

    ax.set_ylim(ylim[0], ylim[1])

    ax.legend(loc=legend_loc)


def annotate_line(line, ax, color='k'):
  xdata = line[0].get_xdata()
  ydata = line[0].get_ydata()
  for i in range(0,len(xdata)):
    ax.text(0.05+xdata[i], ydata[i], str(ydata[i]), fontsize=9, color=color)


def annotate_bar(bars, ax, color='k'):
  for i in range(0,len(bars)):
    bar = bars[i]
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.5, height + 0.05, '%4.1f' % height, ha='center', va='bottom', fontsize=13, rotation=90, color=color)

def main():
    wer_results = {}

    #wer_result_lines = """
    #0  30.3  31.5
    #0.1  30.0  31.2
    #0.25  29.4  30.8
    #0.5  29.0  30.4
    #0.75  29.0  30.4
    #1  29.6  31.2
    #"""
    #wer_result_lines = """
    #0  30.3  31.5
    #0.1  30.0  31.2
    #0.25  29.4  30.8
    #0.5  29.0  30.4
    #0.75  29.0  30.4
    #1  29.6  31.2
    #"""

    wer_results['multilingual\_klfst0.0'] = """
    1k lm1_3 3g 0.0 0.0 27.9 29.9
    1k lm1_3 3g 0.0 0.25 27.7 29.6
    1k lm1_3 3g 0.0 0.5 27.9 29.9
    1k lm1_3 3g 0.0 0.75 28.1 29.8
    1k lm1_3 3g 0.0 1.0 28.4 30.5
    """

    wer_results['multilingual\_klfst0.5'] = """
    1j lm1_3 3g 0.5 0.0 27.8 29.5
    1j lm1_3 3g 0.5 0.25 27.7 29.7
    1j lm1_3 3g 0.5 0.5 28.6 31.1
    1j lm1_3 3g 0.5 0.75 29.2 31.2
    1j lm1_3 3g 0.5 1.0 28.8 31.0
    """

    wer_results['klfst0.5'] = """
    1b3 lm1_3 3g 0.5 0.0 29.8 31.3
    1b3 lm1_3 3g 0.5 0.25 29.3 30.9
    1b3 lm1_3 3g 0.5 0.5 29.3 31.2
    1b3 lm1_3 3g 0.5 0.75 29.3 31.3
    1b3 lm1_3 3g 0.5 1.0 29.4 31.5
    """

    wer_results['klfst0.5\_lm1\_0'] = """
    1b3 lm1_0 3g 0.5 0.0 30.0 31.5
    1b3 lm1_0 3g 0.5 0.25 29.7 31.0
    1b3 lm1_0 3g 0.5 0.5 29.5 31.1
    1b3 lm1_0 3g 0.5 0.75 29.5 31.2
    1b3 lm1_0 3g 0.5 1.0 29.6 31.5
    """

    wer_results['klfst0.5\_lm1\_0\_ug'] = """
    1b3 lm1_0 1g 0.5 0.0 30.4 31.4
    1b3 lm1_0 1g 0.5 0.25 29.7 31.2
    1b3 lm1_0 1g 0.5 0.5 29.4 31.1
    1b3 lm1_0 1g 0.5 0.75 29.6 31.4
    1b3 lm1_0 1g 0.5 1.0 29.8 31.3
    """

    wer_results['klfst0.0'] = """
    1b3 lm1_3 3g 0.0 0.0 29.6 31.4
    1b3 lm1_3 3g 0.0 0.25 29.0 30.9
    1b3 lm1_3 3g 0.0 0.5 28.8 30.6
    1b3 lm1_3 3g 0.0 0.75 28.7 30.6
    1b3 lm1_3 3g 0.0 1.0 28.9 30.5
    """

    #wer_results['klfst0.5\_ug'] = """
    #1b3 lm1_3 1g 0.5 0.0 29.7 31.3
    #1b3 lm1_3 1g 0.5 0.25 29.2 30.9
    #1b3 lm1_3 1g 0.5 0.5 29.2 31.1
    #1b3 lm1_3 1g 0.5 0.75 29.4 31.2
    #1b3 lm1_3 1g 0.5 1.0 29.6 31.4
    #"""

    wer_results['klfst0.5\_ug'] = """
    1b3 lm1_3 1g 0.5 0.0 29.7 31.3
    1b3 lm1_3 1g 0.5 0.25 29.2 30.9
    1b3 lm1_3 1g 0.5 0.5 29.2 31.1
    1b3 lm1_3 1g 0.5 0.75 29.4 31.2
    1b3 lm1_3 1g 0.5 1.0 29.6 31.4
    """

    #wer_results['klfst0.0\_ug'] = """
    #1b3 lm1_3 1g 0.0 0.0 29.8 31.5
    #1b3 lm1_3 1g 0.0 0.25 29.1 30.7
    #1b3 lm1_3 1g 0.0 0.5 28.7 30.5
    #1b3 lm1_3 1g 0.0 0.75 28.8 30.4
    #1b3 lm1_3 1g 0.0 1.0 28.8 30.5
    #"""

    wer_results['klfst0.0\_ug'] = """
    1b3 lm1_3 1g 0.0 0.0 29.9 31.5
    1b3 lm1_3 1g 0.0 0.25 30.2 30.7
    1b3 lm1_3 1g 0.0 0.5 31.2 33.6
    1b3 lm1_3 1g 0.0 0.75 32.5 35.3
    1b3 lm1_3 1g 0.0 1.0 33.3 36.4
    """

    betas = []
    dev_wers = []
    eval_wers = []

    plt.rc('text', usetex=True)

    fig, ax = plt.subplots()
    plot_results(wer_results, ax,
                 #keys={'multilingual\_klfst0.0': "Semisup multitask: LM scale = 0.0",
                 #      'multilingual\_klfst0.5': "Semisup multitask: LM scale = 0.5",
                 #      'klfst0.0': "Unsup only: LM scale = 0.0",
                 #      'klfst0.5': "Unsup only: LM scale = 0.5"},
                 keys={'multilingual\_klfst0.0': "Semisup multitask",
                       'klfst0.0': "Unsup only"},
                 legend_loc='upper left')
    plt.savefig('figures/multilingual_comparison.pdf')
    plt.close()

    fig, ax = plt.subplots()
    plot_results(wer_results, ax, keys={'klfst0.0': "3 gram LM: LM scale = 0.0",
                                        'klfst0.5': "3 gram LM: LM scale = 0.5",
                                        'klfst0.0\_ug': "1 gram LM: LM scale = 0.0",
                                        'klfst0.5\_ug': "1 gram LM: LM scale = 0.5"},
                 legend_loc='upper left',
                 ylim=(28.5,36.5))
    plt.savefig('figures/ug_comparison.pdf')
    plt.close()

    fig, ax = plt.subplots()
    plot_results(wer_results, ax, keys={'klfst0.0': "KL LM scale = 0.0",
                                        'klfst0.5': "KL LM scale = 0.5" },
                 legend_loc='upper left')
    plt.savefig('figures/klfst_comparison.pdf')
    plt.close()

    # ind = np.arange(len(betas))

    #for a,b in zip(betas,dev_wers):
    #    plt.text(a, b, str(b))
    #for a,b in zip(betas,eval_wers):
    #    plt.text(a, b, str(b))



if __name__ == "__main__":
    main()
