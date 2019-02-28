##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Cetmodules(CMakePackage):
    """CMake glue modules and scripts required by packages originating at
    Fermilab and associated experiments and other collaborations.
    """

    homepage = 'https://cdcvs.fnal.gov/projects/cetmodules'

    version('master', branch='master', git=homepage)
    version('develop', branch='develop', git=homepage)
    version('0.08.00',
            sha256='fd2f295c1f91ae41c1f8ae6f014c0fe6c7de8432f8a9020b3bcb9778e1b9f607',
            extension='tbz2')
    version('0.07.00', '60fb6f9ff26605ea4c0648fa43d0a516', extension='tbz2')

    depends_on('cmake@3.4:', type='build')

    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)

    def do_fake_install(self):
        cargs = self.std_cmake_args + self.cmake_args()
        print('\n'.join(['[cmake-args {0}]'.format(self.name)] + cargs +
                        ['[/cmake-args]']))
