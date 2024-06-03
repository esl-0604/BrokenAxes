import matplotlib.pyplot as plt
import seaborn as sns
from data import df
from scipy.stats import ttest_ind

# Seaborn 테마 설정
sns.set_theme(style='ticks')

# 여기를 수정하세요. ----------------------------------------------------------------------
## chartSize (가로, 세로)       : 전체 차트의 크기
## chartScale [상단, 하단]      : 상단, 하단 차트의 Y축 스케일 비율
## upper_Yrange (minY, maxY)   : 상단 차트의 Y값 범위
## lower_Yrange (minY, maxY)   : 하단 차트의 Y값 범위
## y_label                     : 선택할 y축 데이터
## whitespace                  : 차트를 위아래로 자르게 되면, 두 차트 각각 y_label을 설정하도록 되어서 아래쪽만 label을 남겨두고, 공백을 삽입하여 중앙을 맞춘다...ㅎㅎ 
#                                (chartSize와 잘 맞춰가며 조절할 것)

chartSize = (9,9)
chartScale = [1,1]
upper_Yrange = (35, 45)
lower_Yrange = (0, 10)
y_label = 'Number of wrist snaps per tool change (n)'
whitespace = "                                                                         "  # 공백 삽입

# chartSize = (9,9)
# chartScale = [3,1]
# upper_Yrange = (500, 800)
# lower_Yrange = (40, 100)
# y_label = 'Number of wrist snaps per ESD (n)'
# whitespace = "                                                                                                    "  # 공백 삽입
# ----------------------------------------------------------------------------------------

# Calculate p-values
group1 = df[df[' '] == 'INSERTrument'][y_label]
group2 = df[df[' '] == 'Conventional'][y_label]
t_stat, p_value = ttest_ind(group1, group2)

# 두 개의 (상, 하) 차트 각각 생성
fig, (axUp, axDown) = plt.subplots(2, 1, sharex=True, figsize=chartSize, gridspec_kw={'height_ratios': chartScale})

# 상단 박스플롯 설정
sns.boxplot(x=' ', y=y_label, data=df, ax=axUp, palette='Paired')
axUp.set_ylim(upper_Yrange)                     # 상단 축의 y범위 설정
axUp.spines['bottom'].set_visible(False)        # 아래쪽 테두리 숨김
axUp.tick_params(axis='x',                      # 'x'축에 대해
                 which='both',                  # 메이저 및 마이너 틱 모두
                 bottom=False,                  # 아래쪽 틱 비활성화
                 top=False,                     # 위쪽 틱 비활성화
                 labelbottom=False)             # 아래쪽 틱 레이블 비활성화
axUp.set_ylabel('')                             # 상단 그래프 y축 레이블 제거

# 하단 박스플롯 설정
sns.boxplot(x=' ', y=y_label, data=df, ax=axDown, palette='Paired')
axDown.set_ylim(lower_Yrange)                   # 하단 축의 y범위 설정
axDown.spines['top'].set_visible(False)         # 상단 테두리 숨김
axDown.set_ylabel(whitespace + y_label, fontsize=14)         # 하단 그래프에만 y축 레이블 설정


# p-value에 따른 별표 추가 함수
def add_pvalue_star(ax, p_value, x1, x2, y, height, text_height):
    """p-value에 따른 별표를 그래프에 추가하는 함수"""
    if p_value < 0.001:
        stars = '***'
    elif p_value < 0.01:
        stars = '**'
    elif p_value < 0.05:
        stars = '*'
    else:
        stars = 'ns'
    
    print("p-value : " + str(p_value))
    
    # 두 그룹 사이에 선과 별표 추가
    ax.plot([x1, x1, x2, x2], [y, y + height, y + height, y], lw = 2, color='black')
    ax.text((x1 + x2) * 0.5, y + height - text_height, stars, ha='center', va='bottom', color='black')

# 별표 추가 위치 설정
x1, x2 = 0, 1 
y, h, text_h = upper_Yrange[1] - 2, 0.5, 0.15
add_pvalue_star(axUp, p_value, x1, x2, y, h, text_h)


# 축 단절 대각선 표시
d = .015 
kwargs = dict(transform=axUp.transAxes, color='k', clip_on=False)
axUp.plot((-d, +d), (-d, +d), **kwargs)
axUp.plot((1 - d, 1 + d), (-d, +d), **kwargs)

kwargs.update(transform=axDown.transAxes)
axDown.plot((-d, +d), (1 - (chartScale[0] / chartScale[1]) * d, 1 + (chartScale[0] / chartScale[1]) * d), **kwargs)
axDown.plot((1 - d, 1 + d), (1 - (chartScale[0] / chartScale[1]) * d, 1 + (chartScale[0] / chartScale[1]) * d), **kwargs)

plt.show()