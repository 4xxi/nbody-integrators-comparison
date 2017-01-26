# nbody-integrators-comparison
Comparison of n-body integrators, f.e. Mercury6, Rebound, etc

    Here are some tests of comparing Mercury6 and Rebound packages in a frame of Solar system
    gravitational problem (in tests/ directory).
    Methods for test used:
    
    IAS15 for Rebound
    BS (by  default) and RADAU (optionally) for Mercury6
    
    (here and below: .dat is from Rebound, and .aei is from Mercury6)
    .aei and .dat for A309239 Trans-Neptunian Object
    .aei and .dat for Apophis (both RADAU and BS are used)
    .aei and .dat for Mercury (planet, control sample)
    
    Timesteps for A309239 and Mercury may be a little different in these files,
    that causes some unconsistency, but doesn't affect general pattern
    
    There are apollo.py (main testing program) and my_jd.py (additional library)
    in the root.
    
    The results show good, almost perfect accordance for planets and A309239.
    (NOTE: some .aei data values are truncated to 5-6 decimals while .dat values provide more digits)
    
    For Apophis the difference in semimajor axis values(*) is 1e-12 before encounter-2029,
    1e-7 - 1e-8 after encounter and 1e-5 after 100 years of integration.
    
    (*) in AU units