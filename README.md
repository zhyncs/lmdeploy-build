# LMDeploy Build

The tag for the nightly build is commit id, so to install the corresponding whl of the commit, you need to use the commit id to find the corresponding tag at https://github.com/zhyncs/lmdeploy-build/tags and then download the corresponding whl based on CUDA version and Python version.

```bash
# This is usually the case when the environment dependencies are already in place.
pip3 install 'lmdeploy-0.5.0+cu118+ab5b7ce-cp39-cp39-manylinux2014_x86_64.whl' --force-reinstall --no-deps
```
