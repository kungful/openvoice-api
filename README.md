# tryopenvoice.py适用于 openvoiceV2 的api调用接口 

这个api是openvoiceV2 和 pyVideoTrans进行交互的驱动文件

 首先你需要安装：
 
 openvoiceV2（Windows系统推荐[conda](https://www.anaconda.com/)环境里部署）：https://github.com/myshell-ai/OpenVoice
 pyVideoTrans: https://github.com/jianchang512/pyvideotrans.git

 

## 替换参考音频 
```shell
#在代码里面改成你的参考音频文件
"变量音频": "resources/example_reference.mp3"
#或者把你的音频改成example_reference.mp3放入resources进行替换，格式和名称一样替换就能克隆音色
```
### 安装和运行
文件放入openvoice根目录，在目录下召唤终端，如果是虚拟环境安装的openvoice先进入虚拟环境再运行以下命令
```shell
pip install notebook
pip install uvicorn
uvicorn tryopenvoice:app --reload
```
运行成功后，打开pyvideotrans的GUI，点击设置TTS与翻译Key，选择自定义TTS-API，输入API地址：http://127.0.0.1:8000
