#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DRD1 多巴胺受体基因 → MusicXML 转译脚本
严格遵循《DRD1多巴胺受体基因序列音乐转译方案》
"""

from music21 import stream, note, tempo, dynamics, meter
from music21.instrument import Instrument

# ============================================================
# 1. 读取 DRD1 序列
# ============================================================
with open("DRD1.txt", "r", encoding="utf-8") as f:
    raw = f.read()

sequence = "".join(raw.split())  # 移除换行和空格
print(f"序列长度: {len(sequence)} 个碱基")

# ============================================================
# 2. 碱基→音高映射 (C大调固定调)
# ============================================================
BASE_PITCH = {
    'T': 'C4',   # Do
    'C': 'E4',   # Mi
    'G': 'G4',   # Sol
    'A': 'A4',   # La
}

# ============================================================
# 3. 连续重复碱基八度移位处理
# ============================================================
def apply_octave_shift(notes_list):
    if len(notes_list) < 2:
        return notes_list

    result = [notes_list[0]]
    repeat_count = 1
    for i in range(1, len(notes_list)):
        current = notes_list[i]
        prev_pitch_class = result[-1][0]  # 字母部分
        current_pitch_class = current[0]
        if current_pitch_class == prev_pitch_class:
            repeat_count += 1
            octave = int(current[-1])
            if repeat_count % 2 == 0:
                new_octave = octave + 1
            else:
                new_octave = octave - 1 if octave > 1 else octave
            result.append(current_pitch_class + str(new_octave))
        else:
            repeat_count = 1
            result.append(current)
    return result

# ============================================================
# 4. 序列分段（模拟 Intro-A-B-C-Outro 结构）
# ============================================================
def split_sequence(seq):
    total = len(seq)
    intro_len = int(total * 0.08)        # 约 332 bp
    outro_len = int(total * 0.1)         # 约 415 bp

    intro_seq = seq[:intro_len]
    outro_seq = seq[-outro_len:]

    coding_seq = seq[intro_len:-outro_len]
    len_coding = len(coding_seq)
    a_end = int(0.4 * len_coding)
    b_end = int(0.7 * len_coding)
    a_seq = coding_seq[:a_end]
    b_seq = coding_seq[a_end:b_end]
    c_seq = coding_seq[b_end:]

    return intro_seq, a_seq, b_seq, c_seq, outro_seq

# ============================================================
# 5. 生成音高列表
# ============================================================
def notes_from_sequence(seq):
    pitch_names = [BASE_PITCH.get(base, None) for base in seq]
    valid = [p for p in pitch_names if p is not None]
    shifted = apply_octave_shift(valid)
    return shifted

# ============================================================
# 6. 构建完整音乐流
# ============================================================
def build_complete_stream():
    intro_seq, a_seq, b_seq, c_seq, outro_seq = split_sequence(sequence)

    part = stream.Part()

    # 全局拍号
    part.append(meter.TimeSignature('4/4'))

    # ---------- Intro ----------
    part.append(tempo.MetronomeMark(number=120))
    part.append(dynamics.Dynamic('p'))            # 弱
    part.append(Instrument(midiProgram=1))        # 钢琴
    intro_notes = notes_from_sequence(intro_seq)
    for pitch_name in intro_notes:
        n = note.Note(pitch_name, quarterLength=1.0)
        n.volume.velocity = 60
        part.append(n)

    # ---------- A段 ----------
    part.append(tempo.MetronomeMark(number=140))
    part.append(dynamics.Dynamic('mf'))           # 中强
    part.append(Instrument(midiProgram=81))       # Lead 1 (square)
    a_notes = notes_from_sequence(a_seq)
    for i, pitch_name in enumerate(a_notes):
        n = note.Note(pitch_name, quarterLength=0.25)  # 十六分音符
        # 每4个音符一组，第一个重拍加强
        if i % 4 == 0:
            n.volume.velocity = 110
        else:
            n.volume.velocity = 90
        part.append(n)

    # ---------- B段 ----------
    part.append(tempo.MetronomeMark(number=110))
    part.append(dynamics.Dynamic('mp'))           # 中弱
    part.append(Instrument(midiProgram=1))        # 钢琴
    b_notes = notes_from_sequence(b_seq)
    for pitch_name in b_notes:
        n = note.Note(pitch_name, quarterLength=1.0)  # 四分音符
        n.volume.velocity = 75
        part.append(n)

    # ---------- C段 ----------
    part.append(tempo.MetronomeMark(number=100))
    part.append(dynamics.Dynamic('mp'))           # 中弱
    part.append(Instrument(midiProgram=49))       # 弦乐合奏
    c_notes = notes_from_sequence(c_seq)
    for pitch_name in c_notes:
        n = note.Note(pitch_name, quarterLength=2.0)  # 二分音符
        n.volume.velocity = 80
        part.append(n)

    # ---------- Outro ----------
    part.append(tempo.MetronomeMark(number=80))
    part.append(dynamics.Dynamic('f'))            # 强（起）
    part.append(Instrument(midiProgram=1))        # 回归钢琴
    outro_notes = notes_from_sequence(outro_seq)
    for i, pitch_name in enumerate(outro_notes):
        n = note.Note(pitch_name, quarterLength=1.0)
        # 力度逐渐衰减
        vel = max(20, 100 - i * 2) if i < 40 else 20
        n.volume.velocity = vel
        part.append(n)
    # 最后一个音极弱
    if outro_notes:
        part[-1].volume.velocity = 10

    score = stream.Score()
    score.append(part)
    return score

# ============================================================
# 7. 主程序
# ============================================================
def main():
    score = build_complete_stream()
    output_path = "DRD1_music.musicxml"
    score.write('musicxml', fp=output_path)
    print(f"MusicXML 文件已生成：{output_path}")

if __name__ == "__main__":
    main()