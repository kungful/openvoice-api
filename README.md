# tryopenvoice.py适用于 openvoiceV2 的api调用接口 

这个api是openvoiceV2 和 pyVideoTrans进行交互的驱动文件

 首先你需要安装：
              openvoiceV2（Windows系统推荐[conda](https://www.anaconda.com/)环境里部署）：https://github.com/myshell-ai/OpenVoice
              pyVideoTrans: https://github.com/jianchang512/pyvideotrans.git

## 安装运行 
         

```shell
pip install notebook
pip install uvicorn
uvicorn tryopenvoice:app --reload
...

```shell
#在代码里面改成你的参考音频，一分钟左右的音频文件
"变量音频": "resources/maikease.wav"
#或者在resources目录里把你的音频改成maikease.wav，格式和名称一样替换就能克隆音色
...

