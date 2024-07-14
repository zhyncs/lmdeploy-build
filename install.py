import argparse
import os
import subprocess
import sys

import requests


def install_latest_lmdeploy(sha=None):
    res = subprocess.run(['nvcc', '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         text=True,
                         check=True)
    cuda_major_ver = (next(line for line in res.stdout.split('\n')
                           if 'release' in line.lower()).split()[-1]).replace(
                               "V", "").split('.')[0]
    if cuda_major_ver == '11':
        cuda_major_ver += '8'
    elif cuda_major_ver == '12':
        cuda_major_ver += '1'
    else:
        print(f'Fail to support CUDA version=={cuda_major_ver}')
        exit(1)

    if int(sys.version_info.minor) < 10:
        python_ver = sys.version_info.major * 10 + sys.version_info.minor
    else:
        python_ver = sys.version_info.major * 100 + sys.version_info.minor

    if sha:
        lmdeploy_commit = sha
    else:
        lmdeploy_url = 'https://api.github.com/repos/InternLM/LMDeploy/commits'
        resp = requests.get(lmdeploy_url)
        if resp.status_code == 200:
            lmdeploy_commit = resp.json()[0]["sha"][:7]
        else:
            print('Fail to get LMDeploy latest commit')
            exit(1)

    release_url = 'https://api.github.com/repos/InternLM/lmdeploy/releases/latest'  # noqa E501

    lmdeploy_resp = requests.get(release_url)

    if lmdeploy_resp.status_code == 200:
        lmdeploy_ver = lmdeploy_resp.json().get('tag_name').strip().lstrip('v')
    else:
        print('Fail to get LMDeploy latest version')
        exit(1)

    exit_code = os.system(
        f'pip3 install https://github.com/zhyncs/lmdeploy-build/releases/download/{lmdeploy_commit}/lmdeploy-{lmdeploy_ver}+cu{cuda_major_ver}+{lmdeploy_commit}-cp{python_ver}-cp{python_ver}-manylinux2014_x86_64.whl --force-reinstall --no-deps'  # noqa E501
    )

    if exit_code == 0:
        print(f'Succeed to install LMDeploy with commit=={lmdeploy_commit}')
    else:
        print(f'Fail to install LMDeploy with commit=={lmdeploy_commit}')
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sha', type=str)
    args = parser.parse_args()
    install_latest_lmdeploy(args.sha)
