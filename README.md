# Stray Pet Mapper   [![Build Status](https://secure.travis-ci.org/codeforamerica/straymapper.png)](http://travis-ci.org/codeforamerica/straymapper)
Reunite more stray animals with their human companions



## <a name="screenshot"></a>Screenshot
![Stray Pet Mapper](https://github.com/codeforamerica/straymapper/raw/master/screenshot.png "Stray Pet Mapper")

## <a name="demo"></a>Demo
You can see a running version of the application at
[http://straymapper.com/][demo].

[demo]: http://straymapper.com/

## <a name="environment"></a>Development Environment

### Ubuntu Environment
Instructions for creating a development environment for Ubuntu Linux.  This has been tested using Ubuntu 12.04.
    
    #Initial libraries needed
    $sudo apt-get install build-essential git-core python-software-properties python-dev python-pip python-virtualenv

    #SQLite Dependencies
    $sudo apt-get install sqlite3 libsqlite3-dev

    #Spatialite Dependencies
    $sudo apt-get install libproj-dev proj-bin libgeos-dev libgdal-dev libspatialite3 libspatialite-dev spatialite-bin

### Mac Environment
Instructions for creating a development environment on Mac.  This requires that [Homebrew] is installed.     
    
    $ brew install sqlite3
    $ brew isntall geos
    $ brew install proj
    $ brew install gdal
    $ brew install libspatialite

**Note: Without Homebrew**

Install the correct libspatialite library from [Spatialite] for your Mac.

[Homebrew]: http://mxcl.github.com/homebrew/
[Spatialite]: http://www.gaia-gis.it/spatialite-2.3.1/binaries.html

## <a name="installation"></a>Installation
    git clone git://github.com/codeforamerica/straymapper.git
    cd straymapper
    pip install -r requirements.txt
    touch straymapperdb
    spatialite straymapperdb "SELECT InitSpatialMetaData();"
    ./manage.py syncdb

## <a name="usage"></a>Usage
    ./manage.py runserver

## <a name="seed"></a>Seed Data
    ./manage.py runscript animals.scripts.populate

## <a name="contributing"></a>Contributing
In the spirit of [free software][free-sw], **everyone** is encouraged to help
improve this project.

[free-sw]: http://www.fsf.org/licensing/essays/free-sw.html

Here are some ways *you* can contribute:

* by using alpha, beta, and prerelease versions
* by reporting bugs
* by suggesting new features
* by translating to a new language
* by writing or editing documentation
* by writing specifications
* by writing code (**no patch is too small**: fix typos, add comments, clean up
  inconsistent whitespace)
* by refactoring code
* by closing [issues][]
* by reviewing patches
* [financially][]

[issues]: https://github.com/codeforamerica/straymapper/issues
[financially]: https://secure.codeforamerica.org/page/contribute

## <a name="issues"></a>Submitting an Issue
We use the [GitHub issue tracker][issues] to track bugs and features. Before
submitting a bug report or feature request, check to make sure it hasn't
already been submitted. You can indicate support for an existing issue by
voting it up. When submitting a bug report, please include a [Gist][] that
includes a stack trace and any details that may be necessary to reproduce the
bug, including your gem version, Ruby version, and operating system. Ideally, a
bug report should include a pull request with failing specs.

[gist]: https://gist.github.com/

## <a name="pulls"></a>Submitting a Pull Request
1. Fork the project.
2. Create a topic branch.
3. Implement your feature or bug fix.
4. Add tests for your feature or bug fix.
5. Run `./manage.py test`. If your changes are not 100% covered, go back
   to step 4.
6. Commit and push your changes.
7. Submit a pull request. Please do not include changes to the gemspec or
   version file. (If you want to create your own version for some reason,
   please do so in a separate commit.)

## <a name="copyright"></a>Copyright
Copyright (c) 2012 Code for America. See [LICENSE][] for details.

[license]: https://github.com/codeforamerica/cfa_template/blob/master/LICENSE.mkd
