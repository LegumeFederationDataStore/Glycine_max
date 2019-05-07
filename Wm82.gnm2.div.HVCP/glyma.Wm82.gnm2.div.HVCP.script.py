#!/usr/bin/env python3.5
# NAME
#    GmHapMapGt-to-vcf.py - convert GmHapMap_GT to VCF w.r.t. Wm82.a2
#
# SYNOPSIS
#     TEXT to VCF file
#
# INPUT FILES
#     SEQLEN_FILE
#         Sequence lengths from JGI Wm82.a2 assembly (two columns: SEQID, LENGTH). The "mtDNA" length is needed.
#
#     ASSEMBLY_REPORT
#         ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA_000004515.3_Glycine_max_v2.0/GCA_000004515.3_Glycine_max_v2.0_assembly_report.txt#
#
#     TEXT_FILE
#         GmHapMap_GT.txt
#
#
# CHANGE HISTORY
#     2016-10-27    Use 
#     2016-09-28    Use sequence lengths from the JGI assembly. Translate coordinates from NCBI- to JGI-assembly space.
#     2016-06-03    Initial version
#
# AUTHOR
#     Anne Brown < anne.brown@ars.usda.gov> edited from Nathan Weeks <nathan.weeks@ars.usda.gov>

import datetime
import gzip
import operator
import os
import re
import sys


print('##fileformat=VCFv4.2')
print('##reference=Wm82.v2')
print('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">')
print('##fileDate=' + datetime.date.today().strftime("%Y%m%d"))

# Get (JGI) sequence lengths
with open("/scratch/abrown1/Genomes/Gmax_275_v2.0.softmasked.fa.seqlen") as seqlen:
     seqid_to_length = {seqid: int(length) for (seqid, length) in (line.split() for line in seqlen)}

for seqid in seqid_to_length:
    print('##contig=<ID={},length={},assembly=Wm82.a2,species="Glycine max",taxonomy=3847>'.format(seqid, seqid_to_length[seqid]))

VCF = []

with open("/scratch/abrown1/SNP-studies/GmHAPMAP_data/GmHapMap_GT_Intermediate2.txt") as f:
    print("#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO",
            "FORMAT", *f.readline().split()[4:], sep="\t")

    for line in f:
        A = line[:-1].split("\t")
        CHROM = A[0]
        POS = A[1]
        REF = A[2]
        ALT = A[3]
        print("\t".join((CHROM, POS, ".", REF, ALT, ".", ".",".", "GT",*A[4:])))
