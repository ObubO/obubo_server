import random

NICKNAME_ADJ = [
    '가냘픈', '가는', '가엾은', '가파른', '같은', '거센', '거친', '검은', '게으른', '고달픈',
    '고른', '고마운', '고운', '고픈', '곧은', '괜찮은', '구석진', '굳은', '굵은', '귀여운',
    '그런', '그른', '그리운', '기다란', '기쁜', '깊은', '깎아지른', '깨끗한', '나쁜', '나은',
    '난데없는', '날랜', '날카로운', '낮은', '너그러운', '너른', '널따란', '넓은', '네모난', '노란',
    '높은', '누런', '눅은', '느닷없는', '느린', '늦은', '다른', '더러운', '더운', '덜된', '동그란',
    '돼먹잖은', '둥그런', '둥근', '뒤늦은', '드문', '딱한', '때늦은', '뛰어난', '뜨거운', '막다른',
    '많은', '매운', '멋진', '메마른', '메스꺼운', '모난', '못난', '못된', '못생긴', '무거운',
    '무딘', '무른', '무서운', '미운', '반가운', '밝은', '밤늦은', '보드라운', '보람찬', '부드러운',
    '부른', '붉은', '비싼', '빠른', '빨간', '뻘건', '뼈저린', '뽀얀', '뿌연', '새로운', '서툰',
    '섣부른', '설운', '성가신', '수줍은', '쉬운', '스스러운', '슬픈', '시원찮은', '싫은', '쌀쌀맞은',
    '쏜살같은', '쓰디쓴', '쓰린', '아니꼬운', '아닌', '아름다운', '아쉬운', '아픈', '안된', '안쓰러운',
    '안타까운', '않은', '알맞은', '약빠른', '약은', '얇은', '얕은', '어두운', '어려운', '어린',
    '언짢은', '엄청난', '없는', '여문', '열띤', '예쁜', '올바른', '옳은', '외로운', '우스운', '의심쩍은',
    '이른', '익은', '있는', '작은', '잘난', '잘빠진', '잘생긴', '재미있는', '적은', '젊은',
    '점잖은', '조그만', '좁은', '좋은', '주제넘은', '줄기찬', '즐거운', '지나친', '지혜로운', '질긴',
    '짓궂은', '짙은', '짧은', '케케묵은', '탐스러운', '턱없는', '푸른', '하나같은', '한결같은', '흐린',
    '희망찬', '힘겨운', '힘찬', '군침싹도는', '망가져가는', '현란한', '미친척하는', '뻑이가는', '부유한',
    '책임감쩌는', '돼지같은', '표독스러운', '탐스러운삭', '삭아보이는'
]

NICKNAME_CHAR = [
    '튜브', '나니즈', '버즈', '킨더', '미키', '구피', '엘사', '푸', '플루토', '티아나',
    '자스민', '카리오카', '벨', '에리얼', '맥덕', '안나', '구스', '울라프', '피트', '스티치',
    '스카', '엘리스', '알라딘', '스펠', '맬러드', '스패로', '심바', '지니', '메리다', '우디',
    '보핍', '맥퀸', '메이터', '포키', '프레드릭슨', '스톰', '카붐', '개비', '버즈', '니모', '도리',
    '라따뚜이', '피글렛', '티거', '이요르', '스벤', '한스', '트롤', '티몬', '품바', '덤보', '마리',
    '백설', '마이크', '설리', '부', '알린', '제시', '랏소', '미스터 포테이토', '불스아이', '렉스',
    '슬링키 독', '주디', '뚱이', '핑핑이', '징징이', '다람이', '집게사장', '플랑크톤', '쿠키 몬스터',
    '엘모', '빅 버드', '어니', '조이', '그로버', '버트', '데이지', '바이', '마이', '바이퍼',
    '베인', '티모', '피즈', '룰루', '딩거', '뽀삐'
]


def create_nickname():
    adj = random.choice(NICKNAME_ADJ)
    char = random.choice(NICKNAME_CHAR)

    return f"{adj} {char}"

