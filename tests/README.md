## Test GitLab projects structure

- [`python-gitlab-submodule-test/test-projects`](https://gitlab.com/python-gitlab-submodule-test/test-projects)

  - [`gitlab-relative-urls`](https://gitlab.com/python-gitlab-submodule-test/test-projects/gitlab-relative-urls)
    - submodule [`1`](https://gitlab.com/python-gitlab-submodule-test/dummy-projects/1)
      (`../../dummy-projects/1.git`)
    - submodule [`2`](https://gitlab.com/python-gitlab-submodule-test/dummy-projects/2)
      (`../../../python-gitlab-submodule-test/dummy-projects/2.git`)
    - submodule [`3`](https://gitlab.com/python-gitlab-submodule-test/dummy-projects/3)
      (`./../../../python-gitlab-submodule-test/dummy-projects/3.git`)
    - submodule [`4`](https://gitlab.com/python-gitlab-submodule-test/dummy-projects/4)
      (`./../../dummy-projects/4.git`)

  - [`gitlab-absolute-urls`](https://gitlab.com/python-gitlab-submodule-test/test-projects/gitlab-relative-urls)
    - submodule [`OpenRGB`](https://gitlab.com/CalcProgrammer1/OpenRGB)
      (`ssh://git@gitlab.com/CalcProgrammer1/OpenRGB.git`)
    - submodule [`fdroidclient`](https://gitlab.com/fdroid/fdroidclient)
      (`git@gitlab.com:fdroid/fdroidclient.git`)
    - submodule [`inkscape`](https://gitlab.com/inkscape/inkscape.git)
      (`https://gitlab.com/inkscape/inkscape.git`)

  - [`external-urls`](https://gitlab.com/python-gitlab-submodule-test/test-projects/gitlab-relative-urls)
    - submodule [`3dutilities`](https://opensource.ncsa.illinois.edu/bitbucket/scm/u3d/3dutilities)
      (`https://opensource.ncsa.illinois.edu/bitbucket/scm/u3d/3dutilities.git`)
    - submodule [`opencv`](https://github.com/opencv/opencv)
      (`ssh://git@github.com/opencv/opencv.git`)
    - submodule [`scribus-code`](https://sourceforge.net/p/scribus/code/ci/master/tree/)
      (`git://git.code.sf.net/p/scribus/code`)
