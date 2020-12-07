# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


import os
import sys
libdir="%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if not libdir in sys.path:
    sys.path.append(libdir)
from cetmodules_patcher import cetmodules_20_migrator

def patcher(x):
    cetmodules_20_migrator(".","larsoftobj","08.26.02")

def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Larsoftobj(CMakePackage):
    """Larsoftobj"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsoftobj"
    url      = "https://github.com/LArSoft/larsoftobj.git"

    version('MVP1a', git='https://github.com/LArSoft/larsoftobj.git', branch='feature/MVP1a')
    version('1.48.00', tag='v1_48_00', git='https://github.com/LArSoft/larsoftobj.git', get_full_repo=True)
    version('1.49.00', tag='v1_49_00', git='https://github.com/LArSoft/larsoftobj.git', get_full_repo=True)
    version('1.50.00', tag='v1_50_00', git='https://github.com/LArSoft/larsoftobj.git', get_full_repo=True)
    version('08.26.02', tag='v08_26_02', git='https://github.com/LArSoft/larsoftobj.git', get_full_repo=True)
    version('08.26.03', tag='v08_26_03', git='https://github.com/LArSoft/larsoftobj.git', get_full_repo=True)
    version('08.27.06', tag='v08_27_06', git='https://github.com/LArSoft/larsoftobj.git', get_full_repo=True)
    version('09.03.00', tag='v09_03_00', git='https://github.com/LArSoft/larsoftobj.git', get_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch = patcher

    depends_on('gallery')
    depends_on('lardataobj')
    depends_on('lardataalg')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        spack_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        run_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        spack_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        run_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        sanitize_environments(spack_env, run_env)