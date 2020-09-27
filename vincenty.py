import math

ELLIPSOID = {'GRS80': [6378137.0, 1 / 298.257222101],
             'WGS84': [6378137.0, 1 / 298.257223563]}  # [長軸半径, 扁平率]

REPEAT_RIMIT = 1000


def vincenty_inverse(latitude1, longitude1, latitude2, longitude2, ellipsoid='WGS84'):
    """vincenty 逆解法
    2地点の緯度経度から距離・方位角を求める

    Args:
        latitude1(float): 始点の緯度
        longitude1(float): 始点の経度
        latitude2(float): 終点の緯度
        longitude2(float): 終点の経度

    returns:
        dict:
            'distance': 距離
            'azimuth12': 始点から終点の方位
            'azimuth21': 終点から始点の方位

    """

    if math.isclose(latitude1, latitude2) and math.isclose(longitude1, longitude2):
        return {'distance': 0.0,
                'azimuth12': 0.0,
                'azimuth21': 0.0}

    # 楕円体選択
    if type(ellipsoid) == list:
        a, f = ellipsoid
    else:
        a, f = ELLIPSOID[ellipsoid]

    # 短軸半径
    b = (1 - f) * a
    # 緯度ラジアン
    φ1 = math.radians(latitude1)
    φ2 = math.radians(latitude2)
    # 経度ラジアン
    L1 = math.radians(longitude1)
    L2 = math.radians(longitude2)
    L = L2 - L1  # 多分日本語Wiki間違えてる
    # 更成緯度
    U1 = math.atan((1 - f) * math.tan(φ1))
    sin_U1 = math.sin(U1)
    cos_U1 = math.cos(U1)
    U2 = math.atan((1 - f) * math.tan(φ2))
    sin_U2 = math.sin(U2)
    cos_U2 = math.cos(U2)

    # λ初期化
    λ = L
    # 収束させる
    for i in range(REPEAT_RIMIT):
        sin_λ = math.sin(λ)
        cos_λ = math.cos(λ)
        sin_σ = math.sqrt((cos_U2 * sin_λ) ** 2 + (cos_U1 *
                                                   sin_U2 - sin_U1 * cos_U2 * cos_λ) ** 2)
        cos_σ = sin_U1 * sin_U2 + cos_U1 * cos_U2 * cos_λ
        σ = math.atan2(sin_σ, cos_σ)
        sin_α = cos_U1 * cos_U2 * sin_λ / sin_σ
        cos2_α = 1 - sin_α ** 2
        cos_2σm = cos_σ - 2 * sin_U1 * sin_U2 / cos2_α
        C = f / 16 * cos2_α * (4 + f * (4 - 3 * cos2_α))
        λ_ = λ
        λ = L + (1 - C) * f * sin_α * (σ + C * sin_σ *
                                       (cos_2σm + C * cos_σ * (-1 + 2 * cos_2σm ** 2)))
        if abs(λ_ - λ) <= 1e-12:
            break
    else:  # 収束失敗
        print("WARNING: Repeat exceeded {} times.".format(i))
        return None

    # 収束後
    u2 = cos2_α * (a ** 2 - b ** 2) / (b ** 2)
    A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    Δσ = B * sin_σ * (cos_2σm + B / 4 * (cos_σ * (-1 + 2 * cos_2σm ** 2) -
                                         B / 6 * cos_2σm * (-3 + 4 * sin_σ ** 2) * (-3 + 4 * cos_2σm ** 2)))

    # 距離
    s = b * A * (σ - Δσ)

    # 方位
    α1 = math.atan2(cos_U2 * sin_λ, cos_U1 * sin_U2 - sin_U1 * cos_U2 * cos_λ)
    α2 = math.atan2(cos_U1 * sin_λ, (-sin_U1) * cos_U2 +
                    cos_U1 * sin_U2 * cos_λ) + math.pi
    if α1 < 0:
        α1 = α1 + math.pi * 2

    return {'distance': s,
            'azimuth12': math.degrees(α1),
            'azimuth21': math.degrees(α2)}


# def vincenty_direct():
#     pass


if __name__ == "__main__":
    lat1 = 38.260295
    lon1 = 140.882385  # 仙台駅
    lat2 = 38.255435
    lon2 = 140.840823  # 創造工学センター
    print(vincenty_inverse(lat1, lon1, lat2, lon2))
