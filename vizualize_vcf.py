import os
import sys
import vcf
import glob
import argparse
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def vcf_stats(vcfin, outdir, sample):
    inp = vcf.Reader(open(vcfin))
    variants = list()
    ref = list()
    alt = list()
    basename = os.path.splitext(os.path.basename(vcfin))[1]
    genotype = {'0/0':'Homozygous Rerfeence','0/1':'Heterozygous','1/1':'Homozygous Alternate', '1/2':'Non Reference Heterozygous'}
    for lines in inp:
        try:
            var = {'Chrom':lines.CHROM,'Pos':lines.POS, 'Ref':lines.REF, 'Alt': ','.join([str(alt) for alt in lines.ALT]),
                 'Sample':sample, 'Genotype': genotype[lines.genotype(sample)['GT']],'Depth_at_reference':lines.genotype(sample)['AD'][0],
                'Depth_at_alternate':lines.genotype(sample)['AD'][1]}
            variants.append(var)
        except KeyError:
            continue
    variants = pd.DataFrame(variants)
    plt.figure()
    sns.set(style='ticks', context='talk')
    sns.lmplot('Depth_at_reference','Depth_at_alternate',hue='Genotype', data=variants, fit_reg=False)
    plt.xlim([0,max([max(variants.Depth_at_reference), max(variants.Depth_at_alternate)])])
    plt.ylim([0,max([max(variants.Depth_at_reference), max(variants.Depth_at_alternate)])])
    plt.xlabel('Depth at reference allele')
    plt.ylabel('Depth at alternate allele')
    plt.title('Allelic depth distribution')
    plt.savefig(basename+'_allele_depth')
    plt.close()
    return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Vcf stats and visualization')
    parser.add_argument('-i', '--input', dest='input', help='Input vcf file path')
    parser.add_argument('-o', '--output', dest='output', help='Output directory path')
    parser.add_argument('-s', '--samples', dest='samples', help='Sample to be analyzed')
    args = parser.parse_args()
    vcf_stats(args.input, args.output, args.samples) 
