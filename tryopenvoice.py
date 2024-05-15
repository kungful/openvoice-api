from fastapi import FastAPI,Request,HTTPException
from fastapi.staticfiles import StaticFiles

from melo.api import TTS
import torch
import os
import uuid
from openvoice import se_extractor
from openvoice.api import ToneColorConverter

# # 删除根目录下的某个子文件夹内的所有音频文件
# folder_path = ".\\audio_files"  # 替换为你的子文件夹路径
# for filename in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, filename)
#     if filename.endswith(".mp3"):  # 删除所有以.wav结尾的文件，你可以根据需要修改文件类型
#         os.remove(file_path)

device ='cuda' if torch.cuda.is_available() else 'cpu'


app = FastAPI()



AUDIO_FILES_DIRECTORY = ".\\audio_files"
# 创建目录
os.makedirs(".\\audio_files", exist_ok=True)

# 创建一个字典
file_paths = {"默认音频": "resources/example_reference.mp3", "变量音频": "resources/example_reference.mp3"}


#前端发送请求后，这里面的异步函数才会启动显卡推理，这样能节省显存
@app.post("/")
async def generate_audio(request: Request):
    try:
        request_data = await request.form()
        # 表单数据以字典形式返回，您可以如下访问:
        text = request_data.get("text", "")
        language = request_data.get("language", "")
        extra = request_data.get("extra", "")
        voice = request_data.get("voice", "")
        ostype = request_data.get("ostype", "")
        print(text,language,extra,voice,ostype)
        # Speed is adjustable
        speed = 1.0

        # 创建一个语音合成模型，语言为中文，设备为device
        model = TTS(language="ZH", device=device)
        # 获取语音合成模型的语音ID
        speaker_ids = model.hps.data.spk2id
        
        
        # 生成一个随机的唯一文件名
        unique_filename = str(uuid.uuid4())
        # 将随机文件名和音频文件目录连接起来生成音频文件的路径
        output_path = os.path.join(AUDIO_FILES_DIRECTORY, f"{unique_filename}.mp3")

        # 初始化ToneColorConverter，并传入配置文件config.json和设备参数device
        tone_color_converter=ToneColorConverter("config.json",device=device)
        # 加载模型 checkpoint.pth
        tone_color_converter.load_ckpt("checkpoint.pth")

        base_speaker = file_paths["变量音频"]
        source_se, audio_name = se_extractor.get_se(base_speaker, tone_color_converter, vad=True)
        reference_speaker = file_paths["变量音频"] # This is the voice you want to clone
        target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=False)

            
        for speaker_key in speaker_ids.keys():
            speaker_id = speaker_ids[speaker_key]
            speaker_key = speaker_key.lower().replace('_', '-')
                
        source_se = torch.load('.\\checkpoints_v2\\base_speakers\\ses\\zh.pth', map_location=device)
        model.tts_to_file(text, speaker_id, output_path, speed=speed)
        # save_path = f'{AUDIO_FILES_DIRECTORY}/{unique_filename}.mp3'

                # 运行音调颜色转换器
        # encode_message = "@MyShell" # 定义要嵌入音频中的水印信息
        # tone_color_converter.convert(   # 使用音色转换器转换音频并嵌入水印
        #     audio_src_path=output_path,  # 源音频文件路径s
        #     src_se=source_se, # 源音色
        #     tgt_se=target_se,  # 目标音色
        #      output_path=output_path,) # 输出音频文件路径（此处和输入音频路径相同，即直接覆盖原音频）
        #     message=encode_message)   # 要嵌入的水印信息






        # model.tts_to_file(text, speaker_ids['ZH'], output_path, speed=speed)
        file_url = f"http://127.0.0.1:8000/audio_files/{unique_filename}.mp3"
        return {"code":0, "msg": "ok", "data": file_url}
    
    except ValueError as e:
        # 如果数据验证失败，可以抛出HTTPException
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # 处理未知错误
        raise HTTPException(status_code=500, detail="服务器内部错误")
    
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # 自定义异常处理
    return {"code":1, "msg": exc.detail, "data": ""}

app.mount("/audio_files", StaticFiles(directory=AUDIO_FILES_DIRECTORY), name="audio_files")






