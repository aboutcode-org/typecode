typecode
========
typecode provides file type detection functionality to ScanCode toolkit.

To install this package with its full capability (where the binaries for libmagic are installed), use the `full` option:
    pip install typecode[full]

If you want to use the version of libmagic provided by your operating system, use the `minimal` option:
    pip install typecode[minimal]

To set up the typecode development environment:
    source configure

<<<<<<< HEAD
To run unit tests:
    pytest -vvs -n 2 .
=======
    # Create the new repo on GitHub, then update your remote
    git remote set-url origin git@github.com:nexB/your-new-repo.git

From here, you can make the appropriate changes to the files for your specific project.
>>>>>>> refs/remotes/skeleton/main

<<<<<<< HEAD
To clean up development environment:
    ./configure --clean
=======
Update an existing project
---------------------------
.. code-block:: bash

    cd my-existing-project
    git remote add skeleton git@github.com:nexB/skeleton
    git fetch skeleton
    git merge skeleton/main --allow-unrelated-histories

This is also the workflow to use when updating the skeleton files in any given repository.
>>>>>>> refs/remotes/skeleton/main
