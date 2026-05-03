# DRD1-music
将多巴胺受体DRD1基因序列转译为音乐的Python脚本 | A Python script for translating DRD1 gene sequences into music.

# 碱基作响：聆听多巴胺受体DRD1的音乐旋律
> When Bases Resonate: The Melody of Dopamine Receptor DRD1

## 项目简介
本项目提供了一套完整的基因-音乐转译方案，将人类多巴胺D1受体（DRD1）的全部4,147个碱基序列转化为可听的MusicXML总谱。
严格遵循以下生物学逻辑：
- **碱基→音高**：T=Do, C=Mi, G=Sol, A=La (C大调固定调)
- **GC含量→节奏**：高GC区域使用密集十六分音符脉冲，模拟神经元放电
- **蛋白结构→音色**：跨膜区加速+低频，配体结合域舒展弦乐
- **功能状态→动态**：从静息(钢琴单音)→激活(全音色齐奏)→恢复(渐弱回归)

## 文件说明
- `drd1_to_musicxml.py`：核心转译脚本，读取 `DRD1.txt` 序列文件，生成 `DRD1_music.musicxml`
- `DRD1.txt`（需自行准备）：DRD1受体全基因序列
- `DRD1_music.musicxml`（运行后生成）：可用MuseScore等软件打开的乐谱文件

## 使用方法
1. 安装依赖：`pip install music21`
2. 将 `DRD1.txt` 序列文件放入同一目录
3. 运行脚本：`python drd1_to_musicxml.py`
4. 用 [MuseScore](https://musescore.org/) 打开生成的 `.musicxml` 文件，即可播放

## 背景故事
本项目动机、方法论细节及音频试听，请关注微信公众号「基因N方」的推文《碱基作响：聆听多巴胺受体DRD1的音乐旋律》。

## 原创声明
本项目基因-音乐转译方案及生成作品为「基因N方」原创。学术合作或转载请联系公众号。
