import streamlit as st
from PIL import Image
import numpy as np
from scipy.spatial import distance

def ext_mean_rgb(file):
    image = np.array(Image.open(file).convert('RGB')).reshape(-1, 3)
    return np.array([np.mean(image[:, 0]), np.mean(image[:, 1]), np.mean(image[:, 2])])

def gen_color_vec(rgbvec):
    colorvec = np.array([])
    palette = np.array(
        [
        [255, 0, 0], # 赤
        [255, 102, 0], # 橙
        [255, 255, 0], # 黄
        [0, 128, 0], # 緑
        [0, 0, 255], # 青
        [128, 0, 128], # 紫
        [255, 0, 255], # ピンク
        [255, 255, 255], # 白
        [128, 128, 128], # グレー
        [0, 0, 0] # 黒
        ]
    )
    for col in palette:
        colorvec = np.append(colorvec, distance.euclidean(col, rgbvec))
    colorvec = 1 - colorvec/np.linalg.norm(colorvec, np.inf)
    return colorvec.reshape(-1, 1)

st.title('画像の印象を簡単に抽出！')
upload_file = st.file_uploader('画像をアップロード', ['png', 'jpg', 'jpeg'])
if upload_file:
    st.image(upload_file, use_column_width=True)
    impression_vec = gen_color_vec(ext_mean_rgb(upload_file))
    impression_vec = np.ravel(impression_vec)
    impression_word = ['情熱', '元気', '冷静', '優しい', '安らぎ', '不安', '高貴', '純粋', '悲しい', '孤独']
    impression_dict = dict(zip(impression_word, impression_vec))
    sorted_dict = sorted(impression_dict.items(), key=lambda x:x[1], reverse=True)
    st.header(f'印象TOP3: {sorted_dict[0][0]}, {sorted_dict[1][0]}, {sorted_dict[2][0]}')