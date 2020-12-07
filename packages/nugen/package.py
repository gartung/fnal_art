# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys
import os
libdir="%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if not libdir in sys.path:
    sys.path.append(libdir)
from cetmodules_patcher import cetmodules_20_migrator


def patcher(x):
    cetmodules_20_migrator(".","artg4tk","9.07.01")



def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Nugen(CMakePackage):
    """Generator interfaces to art for GENIE and GiBUU."""

    homepage = 'https://cdcvs.fnal.gov/redmine/projects/nugen'
    git_base = 'https://cdcvs.fnal.gov/projects/nugen'

    version('develop', branch='develop', git=git_base)
    version('1.10.02', tag='v1_10_02', git=git_base, get_full_repo=True)
    version('1.10.01', tag='v1_10_01', git=git_base, get_full_repo=True)
    version('1.10.00', tag='v1_10_00', git=git_base, get_full_repo=True)
    version('1.09.00', tag='v1_09_00', git=git_base, get_full_repo=True)
    version('1.08.00', tag='v1_08_00', git=git_base, get_full_repo=True)

    patch = patcher

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    # Build-only dependencies.
    depends_on('cmake@3.12:', type='build')
    depends_on('cetmodules', type='build')
    depends_on('catch2@2.3.0:', type='build')

    # Build and link dependencies.
    depends_on('clhep')
    depends_on('boost')
    depends_on('canvas')
    depends_on('cetlib')
    depends_on('cetlib-except')
    depends_on('fhicl-cpp')
    depends_on('hep-concurrency')
    depends_on('messagefacility')
    depends_on('tbb')
    depends_on('root+python')
    depends_on('perl')
    depends_on('art-root-io')
    depends_on('perl')
    depends_on('pythia6')
    depends_on('libwda')
    depends_on('postgresql')
    depends_on('libxml2')
    depends_on('nusimdata')
    depends_on('dk2nudata')
    depends_on('dk2nugenie')
    depends_on('genie')
    depends_on('xerces-c')
    depends_on('cry')
    depends_on('ifdh-art')
    depends_on('ifdhc')
    depends_on('ifbeam')
    depends_on('nucondb')
    depends_on('libwda')


    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        # Set CMake args.
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DGENIE_INC={0}'.
                format(self.spec['genie'].prefix.include)]
        return args

    def setup_environment(self, spack_env, run_env):
        # Binaries.
        spack_env.prepend_path('PATH',
                               os.path.join(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               os.path.join(self.build_directory, 'lib'))
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(root=False, cover='nodes', order='post',
                                    deptype=('link'), direction='children'):
            spack_env.prepend_path('ROOT_INCLUDE_PATH',
                                   str(self.spec[d.name].prefix.include))
            run_env.prepend_path('ROOT_INCLUDE_PATH',
                                 str(self.spec[d.name].prefix.include))
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Perl modules.
        spack_env.prepend_path('PERL5LIB',
                               os.path.join(self.build_directory, 'perllib'))
        run_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        # Cleaup.
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Perl modules.
        spack_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        run_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        # Cleanup.
        sanitize_environments(spack_env, run_env)