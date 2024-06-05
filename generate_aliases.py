#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import itertools
import os.path
import sys
import time
from shutil import which


xrange = range  # Python 3


def main():
    start = time.time()
    time.sleep(3)

    # (alias, full, allow_when_oneof, incompatible_with)
    kubecolor = which('kubecolor')

    cmds = [('k', 'kubectl', None, None)]
    if kubecolor:
        cmds =[('k', 'kubecolor', None, None)]

    globs = [('sys', '--namespace=kube-system', None, ['sys'])]

    ops = [
        ('a',    'apply --recursive -f',                                            None, None),
        ('ak',   'apply -k',                                                        None, ['sys']),
        ('k',    'kustomize',                                                       None, ['sys']),
        ('ex',   'exec -i -t',                                                      None, None),
        ('lo',   'logs -f',                                                         None, None),
        ('lop',  'logs -f -p',                                                      None, None),
        ('p',    'proxy',                                                           None, ['sys']),
        ('pf',   'port-forward',                                                    None, ['sys']),
        ('g',    'get',                                                             None, None),
        ('d',    'describe',                                                        None, None),
        ('rm',   'delete',                                                          None, None),
        ('ror',   'rollout restart',                                                None, None),
        ('roh',   'rollout history',                                                None, None),
        ('rou',   'rollout undo',                                                   None, None),
        ('run',  'run --rm --restart=Never --image-pull-policy=IfNotPresent -i -t', None, None),
        ('c',    'create',                                                          None, ['sys']),
        ('n',    'config set-context --current --namespace',                        None, ['sys']),
        ('e',    'edit',                                                            None, None),
        ('all', 'api-resources --verbs=list --namespaced -o name | xargs -n 1 kubectl get --show-kind --ignore-not-found', None, ['sys'])
    ]

    res = [
        ('po',    'pods',                              ['g', 'd', 'rm', 'e'],      None),
        ('dep',   'deployment',                        ['g', 'd', 'rm', 'e', 'c', 'ror', 'roh', 'rou'], None),
        ('ds',    'daemonset',                         ['g', 'd', 'rm', 'e', 'c', 'ror', 'roh', 'rou'], None),
        ('rs',    'replicaset',                        ['g', 'd', 'rm', 'e', 'c'], None),
        ('sts',   'statefulset',                       ['g', 'd', 'rm', 'e', 'c', 'ror', 'roh', 'rou'], None),
        ('svc',   'service',                           ['g', 'd', 'rm', 'e', 'c'], None),
        ('ing',   'ingress',                           ['g', 'd', 'rm', 'e', 'c'], None),
        ('cm',    'configmap',                         ['g', 'd', 'rm', 'e', 'c'], None),
        ('sec',   'secret',                            ['g', 'd', 'rm', 'e', 'c'], None),
        ('no',    'nodes',                             ['g', 'd'],                 ['sys']),
        ('ns',    'namespaces',                        ['g', 'd', 'rm', 'e'],      ['sys']),
        ('ns',    'namespace',                         ['e', 'c'],                 ['sys']),
        ('np',    'networkpolicies.networking.k8s.io', ['g', 'd', 'rm', 'e', 'c'], None),
        ('r',     'role',                              ['g', 'd', 'rm', 'e', 'c'], None),
        ('rb',    'rolebinding',                       ['g', 'd', 'rm', 'e', 'c'], None),
        ('cr',    'clusterrole',                       ['g', 'd', 'rm', 'e', 'c'], None),
        ('crb',   'clusterrolebinding',                ['g', 'd', 'rm', 'e', 'c'], None),
        ('sa',    'serviceaccount',                    ['g', 'd', 'rm', 'e', 'c'], None),
        ('pv',    'persistentvolume',                  ['g', 'd', 'e', 'c'], None),
        ('pvc',   'persistentvolumeclaim',             ['g', 'd', 'rm', 'e', 'c'], None),
        ('sm',    'servicemonitors',                   ['g', 'd', 'rm', 'e', 'c'], None),
        ('j',     'job',                               ['g', 'd', 'rm', 'e', 'c'], None),
        ('cj',    'cronjob',                           ['g', 'd', 'rm', 'e', 'c'], None),
        ('ep',    'endpoints',                         ['g', 'd', 'rm', 'e'],      None),
        ('cert',  'certificates',                      ['g', 'd', 'rm', 'e'],      None),
        ('hpa',   'horizontalpodautoscalers',          ['g', 'd', 'rm', 'e'],      None),
        ('a',     'all',                               ['g'],                      None),
        ('c',     'cluster',                           ['g', 'd', 'rm', 'e'],      None),
        ('m',     'machine',                           ['g', 'd', 'rm', 'e'],      None),
        ('md',    'machinedeployment',                 ['g', 'd', 'rm', 'e'],      None),
        ('ms',    'machinesets',                       ['g', 'd', 'rm', 'e'],      None),
        ('kacfg', 'kubeadmconfig',                     ['g', 'd', 'rm', 'e'],      None),
        ('kacp',  'kubeadmcontrolplane',               ['g', 'd', 'rm', 'e'],      None),
        ('oc',    'openstackcluster',                  ['g', 'd', 'rm', 'e'],      None),
        ('om',    'openstackmachine',                  ['g', 'd', 'rm', 'e'],      None),
        ('omt',   'OpenStackMachineTemplate',          ['g', 'd', 'rm', 'e'],      None),
    ]
    res_types = [r[0] for r in res]

    args = [
        ('oyaml', '-o=yaml',                  ['g'],        ['owide', 'ojson', 'sl']),
        ('oyamlp', '-o=yaml --plain' if kubecolor else '-o=yaml',         ['g'],        ['owide', 'ojson', 'sl']), #remove kubecolor format
        ('owide', '-o=wide',                  ['g'],        ['oyaml', 'ojson']),
        ('ojson', '-o=json',                  ['g'],        ['owide', 'oyaml', 'sl']),
        ('ojsonp', '-o=json --plain' if kubecolor else '-o=json',         ['g'],        ['owide', 'oyaml', 'sl']), #remove kubecolor format
        ('all',   '--all-namespaces',         ['g', 'd'],   ['rm', 'f', 'no', 'sys']),
        ('sl',    '--show-labels',            ['g'],        ['oyaml', 'ojson'], None),
        ('all',   '--all',                    ['rm'],       None), # caution: reusing the alias
        ('w',     '--watch --force-colors' if kubecolor else '--watch',                  ['g'],        ['oyaml', 'ojson']),
        ('dry',   '--dry-run=client -o yaml', ['c', 'run'], ['oyaml', 'ojson', 'owide', 'all', 'w', 'sl']),
        ('t10',   '--tail=10',                ['lo'],       ['oyaml', 'ojson', 'owide', 'all', 'w', 'sl']),
    ]

    # these accept a value, so they need to be at the end and
    # mutually exclusive within each other.
    positional_args = [
        ('f', '--recursive -f', ['g', 'd', 'rm'],                               res_types + ['all', 'l', 'sys']),
        ('l', '-l',             ['g', 'd', 'rm'],                               ['f', 'all']),
        ('n', '--namespace',    ['g', 'd', 'rm', 'lo', 'ex', 'pf', 'e', 'all'], ['ns', 'no', 'sys']),
        ('t', '--tail',         ['lo'],                                         ['t10'])
    ]

    # [(part, optional, take_exactly_one)]
    parts = [
        (cmds, False, True),
        (globs, True, False),
        (ops, True, True),
        (res, True, True),
        (args, True, False),
        (positional_args, True, True),
        ]

    shellFormatting = {
        "bash": "alias {}='{}'",
        "zsh": "alias {}='{}'",
        "fish": "abbr --add {} \"{}\"",
    }

    shell = sys.argv[1] if len(sys.argv) > 1 else "bash"
    if shell not in shellFormatting:
        raise ValueError("Shell \"{}\" not supported. Options are {}"
                        .format(shell, [key for key in shellFormatting]))

    out = gen(parts)

    # Special case commands :)
    out.append((('kx', 'kubectx', None, None),))

    # prepare output
    if not sys.stdout.isatty():
        header_path = \
            os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'license_header')
        with open(header_path, 'r') as f:
            print(f.read())

    for cmd in out:
        if which('kubens') is not None and len(cmd) > 1 and cmd[1][0] == 'n':
            cmd = (('k', 'kubens', None, None), ('n', '', None, None))
        print(shellFormatting[shell].format(''.join([a[0] for a in cmd]),
              ' '.join([a[1] for a in cmd])))

    m, s = divmod(int(time.time() - start), 60)
    print("DONE: Generated", str(len(out)), "commands in", str(m), "minutes", str(s), "seconds", file=sys.stderr)


def gen(parts):
    out = [()]
    i = 0
    for (items, optional, take_exactly_one) in parts:
        i+=1
        orig = list(out)
        combos = []

        if optional and take_exactly_one:
            combos = combos.append([])

        if take_exactly_one:
            combos = combinations(items, 1, include_0=optional)
        else:
            combos = combinations(items, len(items), include_0=optional)
            if i == 5:
                valid_combos = []
                for c in combos:
                    found = False
                    for arg in c:
                        incompatibles = arg[3]
                        if not incompatibles:
                            continue
                        for arg2 in c:
                            if arg2[0] in incompatibles:
                                found = True
                    if not found:
                        valid_combos.append(c)
                combos = valid_combos


        # permutate the combinations if optional (args are not positional)
        if optional:
            new_combos = []
            for c in combos:
                new_combos += list(itertools.permutations(c))
            combos = new_combos
        new_out = []
        for segment in combos:
            for stuff in orig:
                if is_valid(stuff + segment):
                    new_out.append(stuff + segment)
        out = new_out

    return out


def is_valid(cmd):
    for i in xrange(0, len(cmd)):

        # check at least one of requirements are in the cmd
        requirements = cmd[i][2]
        if requirements:
            found = False
            for r in requirements:
                for j in xrange(0, i):
                    if cmd[j][0] == r:
                        found = True
                        break
                if found:
                    break
            if not found:
                return False

        # check none of the incompatibilities are in the cmd
        incompatibilities = cmd[i][3]
        if incompatibilities:
            found = False
            for inc in incompatibilities:
                for j in xrange(0, i):
                    if cmd[j][0] == inc:
                        found = True
                        break
                if found:
                    break
            if found:
                return False

    return True


def combinations(a, n, include_0=True):
    l = []
    for j in xrange(0, n + 1):
        if not include_0 and j == 0:
            continue
        l += list(itertools.combinations(a, j))
    return l


def diff(a, b):
    return list(set(a) - set(b))


if __name__ == '__main__':
    main()
