# Artificial_intelligence_project

system setting

set http_proxy=http://127.0.0.1:1081

set https_proxy=http://127.0.0.1:1081

conda remove -n xxxnamexxx --all //删除

conda deactivate //退出环境

conda info --env //查看环境

conda create --name tensorflow2.6 python==3.8

conda activate tensorflow2.6

conda install cudatoolkit=11.3 cudnn=8.2

pip install tensorflow-gpu==2.6
