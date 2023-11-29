# Windows / NVIDIA

First, install Visual Studio 2022 with the CPP desktop development workload.
Any edition should be fine.

Next install CUDA 12.3+

```bat
python -m venv .venv
call .venv\Scripts\activate
python -m pip install -U pip
python -m pip install ninja scikit-build-core[pyproject] scikit-build

@REM Adjust for your VS edition, eg BuildTools, Professional instead of Community
call "c:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
set FORCE_CMAKE=1 && set CMAKE_ARGS=-GNinja -DLLAMA_CUBLAS=on
python -m pip install llama-cpp-python==0.2.19 --force-reinstall --upgrade --no-cache-dir --no-build-isolation -v

python -m pip install torch --index-url https://download.pytorch.org/whl/cu121 --force-reinstall

@REM fixes auto-gptq install error
set DISTUTILS_USE_SDK=1
python -m pip install -r requirements.txt

@REM This shouldn't report any errors
python -m bitsandbytes
✔

@REM but if it does 😠
python -m pip -r req_bitsandbytes.txt
python -m bitsandbytes 
🙏
```
