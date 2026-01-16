"""
INCI Converter - 화장품 성분명 변환 유틸리티

Korean ↔ INCI name bidirectional conversion utility for cosmetic ingredients.

Author: EVAS Cosmetic
License: MIT
Version: 1.0.0
"""

from typing import Optional, Union


# =============================================================================
# KOREAN TO INCI MAPPING (200+ ingredients)
# =============================================================================

KOREAN_INCI_MAP = {
    # =========================================================================
    # 기본 원료 (Base Ingredients)
    # =========================================================================
    "정제수": "AQUA",
    "물": "AQUA",
    "워터": "AQUA",

    # =========================================================================
    # 보습제 (Humectants & Moisturizers)
    # =========================================================================
    "글리세린": "GLYCERIN",
    "글리세롤": "GLYCERIN",
    "부틸렌글라이콜": "BUTYLENE GLYCOL",
    "프로판다이올": "PROPANEDIOL",
    "프로필렌글라이콜": "PROPYLENE GLYCOL",
    "디프로필렌글라이콜": "DIPROPYLENE GLYCOL",
    "펜틸렌글라이콜": "PENTYLENE GLYCOL",
    "헥실렌글라이콜": "HEXYLENE GLYCOL",
    "카프릴릴글라이콜": "CAPRYLYL GLYCOL",
    "에틸헥실글리세린": "ETHYLHEXYLGLYCERIN",
    "베타인": "BETAINE",
    "솔비톨": "SORBITOL",
    "자일리톨": "XYLITOL",
    "만니톨": "MANNITOL",
    "트레할로스": "TREHALOSE",
    "에리스리톨": "ERYTHRITOL",
    "폴리글리세릴-10": "POLYGLYCERYL-10",
    "폴리글리세릴-3": "POLYGLYCERYL-3",
    "소듐피씨에이": "SODIUM PCA",
    "소듐피롤리돈카복실산": "SODIUM PCA",
    "우레아": "UREA",
    "요소": "UREA",
    "알란토인": "ALLANTOIN",
    "판테놀": "PANTHENOL",
    "덱스판테놀": "PANTHENOL",
    "프로비타민B5": "PANTHENOL",
    "히알루론산": "HYALURONIC ACID",
    "히알루론산나트륨": "SODIUM HYALURONATE",
    "소듐히알루로네이트": "SODIUM HYALURONATE",
    "가수분해히알루론산": "HYDROLYZED HYALURONIC ACID",
    "아세틸히알루론산나트륨": "SODIUM ACETYLATED HYALURONATE",
    "히알루론산크로스폴리머나트륨": "SODIUM HYALURONATE CROSSPOLYMER",
    "세라마이드NP": "CERAMIDE NP",
    "세라마이드AP": "CERAMIDE AP",
    "세라마이드EOP": "CERAMIDE EOP",
    "세라마이드NS": "CERAMIDE NS",
    "세라마이드AS": "CERAMIDE AS",
    "피토스핑고신": "PHYTOSPHINGOSINE",
    "스핑고신": "SPHINGOSINE",
    "콜레스테롤": "CHOLESTEROL",
    "스쿠알란": "SQUALANE",
    "스쿠알렌": "SQUALENE",

    # =========================================================================
    # 유화제 (Emulsifiers)
    # =========================================================================
    "세테아릴알코올": "CETEARYL ALCOHOL",
    "세틸알코올": "CETYL ALCOHOL",
    "스테아릴알코올": "STEARYL ALCOHOL",
    "베헤닐알코올": "BEHENYL ALCOHOL",
    "미리스틸알코올": "MYRISTYL ALCOHOL",
    "세테아릴올리베이트": "CETEARYL OLIVATE",
    "소르비탄올리베이트": "SORBITAN OLIVATE",
    "폴리소르베이트20": "POLYSORBATE 20",
    "폴리소르베이트60": "POLYSORBATE 60",
    "폴리소르베이트80": "POLYSORBATE 80",
    "소르비탄스테아레이트": "SORBITAN STEARATE",
    "소르비탄올레이트": "SORBITAN OLEATE",
    "글리세릴스테아레이트": "GLYCERYL STEARATE",
    "글리세릴스테아레이트SE": "GLYCERYL STEARATE SE",
    "글리세릴모노스테아레이트": "GLYCERYL STEARATE",
    "피이지-100스테아레이트": "PEG-100 STEARATE",
    "피이지-40스테아레이트": "PEG-40 STEARATE",
    "피이지-20스테아레이트": "PEG-20 STEARATE",
    "피이지-8스테아레이트": "PEG-8 STEARATE",
    "피이지-40수소첨가피마자유": "PEG-40 HYDROGENATED CASTOR OIL",
    "피이지-60수소첨가피마자유": "PEG-60 HYDROGENATED CASTOR OIL",
    "세테아릴글루코사이드": "CETEARYL GLUCOSIDE",
    "라우릴글루코사이드": "LAURYL GLUCOSIDE",
    "데실글루코사이드": "DECYL GLUCOSIDE",
    "코코글루코사이드": "COCO-GLUCOSIDE",
    "레시틴": "LECITHIN",
    "수소첨가레시틴": "HYDROGENATED LECITHIN",
    "포스파티딜콜린": "PHOSPHATIDYLCHOLINE",

    # =========================================================================
    # 계면활성제 (Surfactants)
    # =========================================================================
    "소듐라우릴설페이트": "SODIUM LAURYL SULFATE",
    "소듐라우레스설페이트": "SODIUM LAURETH SULFATE",
    "암모늄라우릴설페이트": "AMMONIUM LAURYL SULFATE",
    "암모늄라우레스설페이트": "AMMONIUM LAURETH SULFATE",
    "소듐코코일이세티오네이트": "SODIUM COCOYL ISETHIONATE",
    "소듐코코일글루타메이트": "SODIUM COCOYL GLUTAMATE",
    "소듐라우로일글루타메이트": "SODIUM LAUROYL GLUTAMATE",
    "디소듐코코암포디아세테이트": "DISODIUM COCOAMPHODIACETATE",
    "코카미도프로필베타인": "COCAMIDOPROPYL BETAINE",
    "코카미드디이에이": "COCAMIDE DEA",
    "코카미드엠이에이": "COCAMIDE MEA",
    "라우릴베타인": "LAURYL BETAINE",
    "코코베타인": "COCO-BETAINE",
    "라우라미도프로필베타인": "LAURAMIDOPROPYL BETAINE",
    "소듐코코일애플아미노산": "SODIUM COCOYL APPLE AMINO ACIDS",
    "소듐코코일알라니네이트": "SODIUM COCOYL ALANINATE",
    "소듐메틸코코일타우레이트": "SODIUM METHYL COCOYL TAURATE",
    "소듐라우로일메틸이세티오네이트": "SODIUM LAUROYL METHYL ISETHIONATE",
    "소듐코코일글리시네이트": "SODIUM COCOYL GLYCINATE",

    # =========================================================================
    # 점증제 (Thickeners & Viscosity Modifiers)
    # =========================================================================
    "카보머": "CARBOMER",
    "잔탄검": "XANTHAN GUM",
    "하이드록시에틸셀룰로오스": "HYDROXYETHYLCELLULOSE",
    "하이드록시프로필메틸셀룰로오스": "HYDROXYPROPYL METHYLCELLULOSE",
    "메틸셀룰로오스": "METHYLCELLULOSE",
    "셀룰로오스검": "CELLULOSE GUM",
    "소듐카복시메틸셀룰로오스": "SODIUM CARBOXYMETHYL CELLULOSE",
    "아크릴레이트/C10-30알킬아크릴레이트크로스폴리머": "ACRYLATES/C10-30 ALKYL ACRYLATE CROSSPOLYMER",
    "아크릴레이트코폴리머": "ACRYLATES COPOLYMER",
    "구아검": "GUAR GUM",
    "하이드록시프로필구아검": "HYDROXYPROPYL GUAR",
    "로커스트빈검": "CERATONIA SILIQUA GUM",
    "캐롭검": "CERATONIA SILIQUA GUM",
    "아라비아검": "ACACIA SENEGAL GUM",
    "젤란검": "GELLAN GUM",
    "키토산": "CHITOSAN",
    "알긴산나트륨": "SODIUM ALGINATE",
    "알지네이트": "ALGIN",
    "카라기난": "CARRAGEENAN",
    "펙틴": "PECTIN",
    "한천": "AGAR",
    "폴리아크릴아미드": "POLYACRYLAMIDE",
    "소듐폴리아크릴레이트": "SODIUM POLYACRYLATE",
    "암모늄아크릴로일디메틸타우레이트/VP코폴리머": "AMMONIUM ACRYLOYLDIMETHYLTAURATE/VP COPOLYMER",

    # =========================================================================
    # 방부제 (Preservatives)
    # =========================================================================
    "페녹시에탄올": "PHENOXYETHANOL",
    "벤질알코올": "BENZYL ALCOHOL",
    "에칠헥실글리세린": "ETHYLHEXYLGLYCERIN",
    "메칠파라벤": "METHYLPARABEN",
    "에칠파라벤": "ETHYLPARABEN",
    "프로필파라벤": "PROPYLPARABEN",
    "부틸파라벤": "BUTYLPARABEN",
    "소듐벤조에이트": "SODIUM BENZOATE",
    "벤조산": "BENZOIC ACID",
    "포타슘소르베이트": "POTASSIUM SORBATE",
    "소르브산": "SORBIC ACID",
    "데하이드로아세트산": "DEHYDROACETIC ACID",
    "소듐데하이드로아세테이트": "SODIUM DEHYDROACETATE",
    "클로르페네신": "CHLORPHENESIN",
    "디아졸리디닐우레아": "DIAZOLIDINYL UREA",
    "이미다졸리디닐우레아": "IMIDAZOLIDINYL UREA",
    "디엠디엠히단토인": "DMDM HYDANTOIN",
    "소듐하이드록시메틸글리시네이트": "SODIUM HYDROXYMETHYLGLYCINATE",
    "1,2-헥산다이올": "1,2-HEXANEDIOL",
    "에틸헥산다이올": "ETHYLHEXANEDIOL",
    "오-사이멘-5-올": "O-CYMEN-5-OL",
    "글리코모날락타마이드": "GLYCERYL CAPRYLATE",
    "트리클로산": "TRICLOSAN",
    "아이오도프로피닐부틸카바메이트": "IODOPROPYNYL BUTYLCARBAMATE",

    # =========================================================================
    # 활성 성분 - 미백 (Whitening Actives)
    # =========================================================================
    "나이아신아마이드": "NIACINAMIDE",
    "니코틴아마이드": "NIACINAMIDE",
    "비타민B3": "NIACINAMIDE",
    "알파알부틴": "ALPHA-ARBUTIN",
    "아르부틴": "ARBUTIN",
    "베타알부틴": "BETA-ARBUTIN",
    "트라넥사믹애씨드": "TRANEXAMIC ACID",
    "트라넥삼산": "TRANEXAMIC ACID",
    "아스코르브산": "ASCORBIC ACID",
    "비타민C": "ASCORBIC ACID",
    "아스코르빌글루코사이드": "ASCORBYL GLUCOSIDE",
    "에틸아스코르빌에테르": "ETHYL ASCORBIC ACID",
    "3-O-에틸아스코르브산": "3-O-ETHYL ASCORBIC ACID",
    "아스코르빌팔미테이트": "ASCORBYL PALMITATE",
    "소듐아스코르빌포스페이트": "SODIUM ASCORBYL PHOSPHATE",
    "마그네슘아스코르빌포스페이트": "MAGNESIUM ASCORBYL PHOSPHATE",
    "아스코르빌테트라이소팔미테이트": "ASCORBYL TETRAISOPALMITATE",
    "글루타치온": "GLUTATHIONE",
    "코직산": "KOJIC ACID",
    "감초추출물": "GLYCYRRHIZA GLABRA ROOT EXTRACT",
    "글라브리딘": "GLABRIDIN",

    # =========================================================================
    # 활성 성분 - 주름개선 (Anti-aging Actives)
    # =========================================================================
    "레티놀": "RETINOL",
    "레티닐팔미테이트": "RETINYL PALMITATE",
    "레티닐아세테이트": "RETINYL ACETATE",
    "레티날": "RETINAL",
    "레티노익애씨드": "RETINOIC ACID",
    "아데노신": "ADENOSINE",
    "펩타이드": "PEPTIDE",
    "아세틸헥사펩타이드-8": "ACETYL HEXAPEPTIDE-8",
    "팔미토일펜타펩타이드-4": "PALMITOYL PENTAPEPTIDE-4",
    "팔미토일트리펩타이드-1": "PALMITOYL TRIPEPTIDE-1",
    "팔미토일테트라펩타이드-7": "PALMITOYL TETRAPEPTIDE-7",
    "구리펩타이드": "COPPER TRIPEPTIDE-1",
    "카퍼트리펩타이드-1": "COPPER TRIPEPTIDE-1",
    "마트리킬": "PALMITOYL PENTAPEPTIDE-4",
    "아르지렐린": "ACETYL HEXAPEPTIDE-8",
    "바이오펩타이드CL": "PALMITOYL TRIPEPTIDE-5",
    "콜라겐": "COLLAGEN",
    "수용성콜라겐": "SOLUBLE COLLAGEN",
    "가수분해콜라겐": "HYDROLYZED COLLAGEN",
    "엘라스틴": "ELASTIN",
    "가수분해엘라스틴": "HYDROLYZED ELASTIN",
    "코엔자임Q10": "UBIQUINONE",
    "유비퀴논": "UBIQUINONE",
    "이데베논": "IDEBENONE",

    # =========================================================================
    # 활성 성분 - 진정 (Soothing Actives)
    # =========================================================================
    "판테놀": "PANTHENOL",
    "비사보롤": "BISABOLOL",
    "알파비사보롤": "ALPHA-BISABOLOL",
    "아줄렌": "AZULENE",
    "구아이아줄렌": "GUAIAZULENE",
    "마데카소사이드": "MADECASSOSIDE",
    "아시아티코사이드": "ASIATICOSIDE",
    "아시아틱애씨드": "ASIATIC ACID",
    "마데카식애씨드": "MADECASSIC ACID",
    "베타글루칸": "BETA-GLUCAN",
    "카렌둘라추출물": "CALENDULA OFFICINALIS FLOWER EXTRACT",
    "캐모마일추출물": "CHAMOMILLA RECUTITA FLOWER EXTRACT",
    "자먹추출물": "CENTAUREA CYANUS FLOWER EXTRACT",

    # =========================================================================
    # 비타민류 (Vitamins)
    # =========================================================================
    "토코페롤": "TOCOPHEROL",
    "비타민E": "TOCOPHEROL",
    "토코페릴아세테이트": "TOCOPHERYL ACETATE",
    "토코트리에놀": "TOCOTRIENOLS",
    "알파토코페롤": "ALPHA-TOCOPHEROL",
    "비타민A": "RETINOL",
    "비타민B1": "THIAMINE",
    "티아민": "THIAMINE",
    "비타민B2": "RIBOFLAVIN",
    "리보플라빈": "RIBOFLAVIN",
    "비타민B5": "PANTHENOL",
    "판토텐산": "PANTOTHENIC ACID",
    "칼슘판토테네이트": "CALCIUM PANTOTHENATE",
    "비타민B6": "PYRIDOXINE",
    "피리독신": "PYRIDOXINE",
    "비타민B7": "BIOTIN",
    "비오틴": "BIOTIN",
    "비타민B9": "FOLIC ACID",
    "엽산": "FOLIC ACID",
    "비타민B12": "CYANOCOBALAMIN",
    "시아노코발라민": "CYANOCOBALAMIN",
    "비타민D": "CHOLECALCIFEROL",
    "콜레칼시페롤": "CHOLECALCIFEROL",
    "비타민K": "PHYTONADIONE",
    "피토나디온": "PHYTONADIONE",

    # =========================================================================
    # 식물 추출물 (Plant Extracts)
    # =========================================================================
    "녹차추출물": "CAMELLIA SINENSIS LEAF EXTRACT",
    "녹차잎추출물": "CAMELLIA SINENSIS LEAF EXTRACT",
    "알로에베라잎추출물": "ALOE BARBADENSIS LEAF EXTRACT",
    "알로에추출물": "ALOE BARBADENSIS LEAF EXTRACT",
    "알로에베라잎즙": "ALOE BARBADENSIS LEAF JUICE",
    "병풀추출물": "CENTELLA ASIATICA EXTRACT",
    "센텔라아시아티카추출물": "CENTELLA ASIATICA EXTRACT",
    "티카추출물": "CENTELLA ASIATICA EXTRACT",
    "장미추출물": "ROSA DAMASCENA FLOWER EXTRACT",
    "다마스크장미추출물": "ROSA DAMASCENA FLOWER EXTRACT",
    "장미워터": "ROSA DAMASCENA FLOWER WATER",
    "장미꽃수": "ROSA DAMASCENA FLOWER WATER",
    "라벤더추출물": "LAVANDULA ANGUSTIFOLIA FLOWER EXTRACT",
    "라벤더워터": "LAVANDULA ANGUSTIFOLIA FLOWER WATER",
    "라벤더꽃수": "LAVANDULA ANGUSTIFOLIA FLOWER WATER",
    "라벤더오일": "LAVANDULA ANGUSTIFOLIA FLOWER OIL",
    "카모마일추출물": "CHAMOMILLA RECUTITA FLOWER EXTRACT",
    "캐모마일추출물": "CHAMOMILLA RECUTITA FLOWER EXTRACT",
    "저먼카모마일추출물": "CHAMOMILLA RECUTITA FLOWER EXTRACT",
    "로만카모마일추출물": "ANTHEMIS NOBILIS FLOWER EXTRACT",
    "위치하젤추출물": "HAMAMELIS VIRGINIANA EXTRACT",
    "위치하젤워터": "HAMAMELIS VIRGINIANA WATER",
    "인삼추출물": "PANAX GINSENG ROOT EXTRACT",
    "홍삼추출물": "PANAX GINSENG ROOT EXTRACT",
    "백삼추출물": "PANAX GINSENG ROOT EXTRACT",
    "감초뿌리추출물": "GLYCYRRHIZA GLABRA ROOT EXTRACT",
    "로즈마리추출물": "ROSMARINUS OFFICINALIS LEAF EXTRACT",
    "로즈메리잎추출물": "ROSMARINUS OFFICINALIS LEAF EXTRACT",
    "유칼립투스잎추출물": "EUCALYPTUS GLOBULUS LEAF EXTRACT",
    "페퍼민트잎추출물": "MENTHA PIPERITA LEAF EXTRACT",
    "박하추출물": "MENTHA PIPERITA LEAF EXTRACT",
    "티트리잎추출물": "MELALEUCA ALTERNIFOLIA LEAF EXTRACT",
    "어성초추출물": "HOUTTUYNIA CORDATA EXTRACT",
    "약모밀추출물": "HOUTTUYNIA CORDATA EXTRACT",
    "쑥추출물": "ARTEMISIA VULGARIS EXTRACT",
    "애엽추출물": "ARTEMISIA PRINCEPS LEAF EXTRACT",
    "백년초추출물": "OPUNTIA FICUS-INDICA EXTRACT",
    "선인장추출물": "OPUNTIA FICUS-INDICA EXTRACT",
    "백합추출물": "LILIUM CANDIDUM FLOWER EXTRACT",
    "연꽃추출물": "NELUMBO NUCIFERA FLOWER EXTRACT",
    "자스민추출물": "JASMINUM OFFICINALE FLOWER EXTRACT",
    "국화추출물": "CHRYSANTHEMUM INDICUM FLOWER EXTRACT",
    "동백추출물": "CAMELLIA JAPONICA FLOWER EXTRACT",
    "동백꽃추출물": "CAMELLIA JAPONICA FLOWER EXTRACT",
    "벚꽃추출물": "PRUNUS SERRULATA FLOWER EXTRACT",
    "살구꽃추출물": "PRUNUS ARMENIACA FLOWER EXTRACT",
    "모과추출물": "CHAENOMELES SINENSIS FRUIT EXTRACT",
    "석류추출물": "PUNICA GRANATUM FRUIT EXTRACT",
    "블루베리추출물": "VACCINIUM ANGUSTIFOLIUM FRUIT EXTRACT",
    "포도추출물": "VITIS VINIFERA FRUIT EXTRACT",
    "레몬추출물": "CITRUS LIMON FRUIT EXTRACT",
    "오렌지추출물": "CITRUS AURANTIUM DULCIS FRUIT EXTRACT",
    "자몽추출물": "CITRUS GRANDIS FRUIT EXTRACT",
    "라임추출물": "CITRUS AURANTIFOLIA FRUIT EXTRACT",
    "오이추출물": "CUCUMIS SATIVUS FRUIT EXTRACT",
    "수박추출물": "CITRULLUS LANATUS FRUIT EXTRACT",
    "사과추출물": "PYRUS MALUS FRUIT EXTRACT",
    "배추출물": "PYRUS COMMUNIS FRUIT EXTRACT",
    "키위추출물": "ACTINIDIA CHINENSIS FRUIT EXTRACT",
    "파파야추출물": "CARICA PAPAYA FRUIT EXTRACT",
    "망고추출물": "MANGIFERA INDICA FRUIT EXTRACT",
    "아보카도추출물": "PERSEA GRATISSIMA FRUIT EXTRACT",
    "코코넛추출물": "COCOS NUCIFERA FRUIT EXTRACT",
    "올리브잎추출물": "OLEA EUROPAEA LEAF EXTRACT",
    "포도씨추출물": "VITIS VINIFERA SEED EXTRACT",
    "아마씨추출물": "LINUM USITATISSIMUM SEED EXTRACT",
    "호박씨추출물": "CUCURBITA PEPO SEED EXTRACT",
    "해바라기씨추출물": "HELIANTHUS ANNUUS SEED EXTRACT",
    "참깨추출물": "SESAMUM INDICUM SEED EXTRACT",
    "밀배아추출물": "TRITICUM VULGARE GERM EXTRACT",
    "귀리추출물": "AVENA SATIVA KERNEL EXTRACT",
    "콩추출물": "GLYCINE SOJA SEED EXTRACT",
    "대두추출물": "GLYCINE SOJA SEED EXTRACT",
    "율피추출물": "CASTANEA CRENATA SHELL EXTRACT",
    "밤껍질추출물": "CASTANEA CRENATA SHELL EXTRACT",

    # =========================================================================
    # 오일류 (Oils)
    # =========================================================================
    "호호바오일": "SIMMONDSIA CHINENSIS (JOJOBA) SEED OIL",
    "호호바씨오일": "SIMMONDSIA CHINENSIS (JOJOBA) SEED OIL",
    "아르간오일": "ARGANIA SPINOSA KERNEL OIL",
    "티트리오일": "MELALEUCA ALTERNIFOLIA (TEA TREE) LEAF OIL",
    "올리브오일": "OLEA EUROPAEA (OLIVE) FRUIT OIL",
    "스위트아몬드오일": "PRUNUS AMYGDALUS DULCIS (SWEET ALMOND) OIL",
    "아몬드오일": "PRUNUS AMYGDALUS DULCIS (SWEET ALMOND) OIL",
    "코코넛오일": "COCOS NUCIFERA (COCONUT) OIL",
    "피마자유": "RICINUS COMMUNIS (CASTOR) SEED OIL",
    "캐스터오일": "RICINUS COMMUNIS (CASTOR) SEED OIL",
    "마카다미아넛오일": "MACADAMIA TERNIFOLIA SEED OIL",
    "아보카도오일": "PERSEA GRATISSIMA (AVOCADO) OIL",
    "로즈힙오일": "ROSA CANINA FRUIT OIL",
    "로즈힙씨오일": "ROSA CANINA SEED OIL",
    "해바라기씨오일": "HELIANTHUS ANNUUS (SUNFLOWER) SEED OIL",
    "포도씨오일": "VITIS VINIFERA (GRAPE) SEED OIL",
    "달맞이꽃종자유": "OENOTHERA BIENNIS (EVENING PRIMROSE) OIL",
    "이브닝프림로즈오일": "OENOTHERA BIENNIS (EVENING PRIMROSE) OIL",
    "보리지오일": "BORAGO OFFICINALIS SEED OIL",
    "밀배아유": "TRITICUM VULGARE (WHEAT) GERM OIL",
    "동백유": "CAMELLIA JAPONICA SEED OIL",
    "쌀겨오일": "ORYZA SATIVA (RICE) BRAN OIL",
    "미강유": "ORYZA SATIVA (RICE) BRAN OIL",
    "참기름": "SESAMUM INDICUM (SESAME) SEED OIL",
    "참깨오일": "SESAMUM INDICUM (SESAME) SEED OIL",
    "면실유": "GOSSYPIUM HERBACEUM (COTTON) SEED OIL",
    "대마씨오일": "CANNABIS SATIVA SEED OIL",
    "헴프시드오일": "CANNABIS SATIVA SEED OIL",
    "아마씨오일": "LINUM USITATISSIMUM (LINSEED) SEED OIL",
    "미네랄오일": "MINERAL OIL",
    "화이트미네랄오일": "MINERAL OIL",
    "파라핀오일": "PARAFFINUM LIQUIDUM",
    "바셀린": "PETROLATUM",
    "페트롤라툼": "PETROLATUM",

    # =========================================================================
    # 버터류 (Butters)
    # =========================================================================
    "시어버터": "BUTYROSPERMUM PARKII (SHEA) BUTTER",
    "코코아버터": "THEOBROMA CACAO (COCOA) SEED BUTTER",
    "카카오버터": "THEOBROMA CACAO (COCOA) SEED BUTTER",
    "망고버터": "MANGIFERA INDICA (MANGO) SEED BUTTER",
    "아보카도버터": "PERSEA GRATISSIMA (AVOCADO) BUTTER",
    "커피버터": "COFFEA ARABICA (COFFEE) SEED BUTTER",

    # =========================================================================
    # 자외선차단제 (UV Filters)
    # =========================================================================
    "티타늄디옥사이드": "TITANIUM DIOXIDE",
    "이산화티탄": "TITANIUM DIOXIDE",
    "징크옥사이드": "ZINC OXIDE",
    "산화아연": "ZINC OXIDE",
    "옥시벤존": "BENZOPHENONE-3",
    "벤조페논-3": "BENZOPHENONE-3",
    "에칠헥실메톡시신나메이트": "ETHYLHEXYL METHOXYCINNAMATE",
    "옥티녹세이트": "ETHYLHEXYL METHOXYCINNAMATE",
    "옥틸메톡시신나메이트": "ETHYLHEXYL METHOXYCINNAMATE",
    "에칠헥실살리실레이트": "ETHYLHEXYL SALICYLATE",
    "옥틸살리실레이트": "ETHYLHEXYL SALICYLATE",
    "부틸메톡시디벤조일메탄": "BUTYL METHOXYDIBENZOYLMETHANE",
    "아보벤존": "BUTYL METHOXYDIBENZOYLMETHANE",
    "호모살레이트": "HOMOSALATE",
    "옥토크릴렌": "OCTOCRYLENE",
    "비스에칠헥실옥시페놀메톡시페닐트리아진": "BIS-ETHYLHEXYLOXYPHENOL METHOXYPHENYL TRIAZINE",
    "티노소르브S": "BIS-ETHYLHEXYLOXYPHENOL METHOXYPHENYL TRIAZINE",
    "에칠헥실트리아존": "ETHYLHEXYL TRIAZONE",
    "디에칠아미노하이드록시벤조일헥실벤조에이트": "DIETHYLAMINO HYDROXYBENZOYL HEXYL BENZOATE",

    # =========================================================================
    # 향료 관련 (Fragrance)
    # =========================================================================
    "향료": "FRAGRANCE",
    "인공향료": "FRAGRANCE",
    "합성향료": "FRAGRANCE",
    "퍼퓸": "PARFUM",
    "리날룰": "LINALOOL",
    "리모넨": "LIMONENE",
    "시트로넬롤": "CITRONELLOL",
    "제라니올": "GERANIOL",
    "시트랄": "CITRAL",
    "유제놀": "EUGENOL",
    "쿠마린": "COUMARIN",
    "벤질벤조에이트": "BENZYL BENZOATE",
    "벤질신나메이트": "BENZYL CINNAMATE",
    "신나밀알코올": "CINNAMYL ALCOHOL",
    "신나말": "CINNAMAL",
    "아밀신나밀알코올": "AMYL CINNAMYL ALCOHOL",
    "아밀신나말": "AMYL CINNAMAL",
    "헥실신나말": "HEXYL CINNAMAL",
    "알파이소메틸이오논": "ALPHA-ISOMETHYL IONONE",
    "부틸페닐메틸프로피오날": "BUTYLPHENYL METHYLPROPIONAL",
    "하이드록시시트로넬랄": "HYDROXYCITRONELLAL",
    "이소유제놀": "ISOEUGENOL",
    "파네솔": "FARNESOL",
    "벤질살리실레이트": "BENZYL SALICYLATE",
    "오크모스추출물": "EVERNIA PRUNASTRI EXTRACT",
    "트리모스추출물": "EVERNIA FURFURACEA EXTRACT",

    # =========================================================================
    # 기타 (Others)
    # =========================================================================
    "에탄올": "ALCOHOL",
    "알코올": "ALCOHOL",
    "변성알코올": "ALCOHOL DENAT.",
    "이소프로필알코올": "ISOPROPYL ALCOHOL",
    "에틸알코올": "ETHYL ALCOHOL",
    "소듐하이드록사이드": "SODIUM HYDROXIDE",
    "가성소다": "SODIUM HYDROXIDE",
    "트리에탄올아민": "TRIETHANOLAMINE",
    "아미노메틸프로판올": "AMINOMETHYL PROPANOL",
    "소듐클로라이드": "SODIUM CHLORIDE",
    "염화나트륨": "SODIUM CHLORIDE",
    "소금": "SODIUM CHLORIDE",
    "디소듐이디티에이": "DISODIUM EDTA",
    "이디티에이": "EDTA",
    "테트라소듐이디티에이": "TETRASODIUM EDTA",
    "구연산": "CITRIC ACID",
    "시트릭애씨드": "CITRIC ACID",
    "소듐시트레이트": "SODIUM CITRATE",
    "락틱애씨드": "LACTIC ACID",
    "젖산": "LACTIC ACID",
    "소듐락테이트": "SODIUM LACTATE",
    "글리콜릭애씨드": "GLYCOLIC ACID",
    "글리콜산": "GLYCOLIC ACID",
    "살리실릭애씨드": "SALICYLIC ACID",
    "살리실산": "SALICYLIC ACID",
    "만델릭애씨드": "MANDELIC ACID",
    "만델산": "MANDELIC ACID",
    "타르타릭애씨드": "TARTARIC ACID",
    "주석산": "TARTARIC ACID",
    "말릭애씨드": "MALIC ACID",
    "사과산": "MALIC ACID",
    "피틱애씨드": "PHYTIC ACID",
    "피트산": "PHYTIC ACID",
    "아젤라익애씨드": "AZELAIC ACID",
    "아젤라산": "AZELAIC ACID",
    "실리카": "SILICA",
    "이산화규소": "SILICA",
    "탈크": "TALC",
    "활석": "TALC",
    "마이카": "MICA",
    "운모": "MICA",
    "카올린": "KAITE",
    "고령토": "KAOLIN",
    "벤토나이트": "BENTONITE",
    "몬모릴로나이트": "MONTMORILLONITE",
    "제올라이트": "ZEOLITE",
    "디메티콘": "DIMETHICONE",
    "사이클로펜타실록산": "CYCLOPENTASILOXANE",
    "사이클로메티콘": "CYCLOMETHICONE",
    "페닐트리메티콘": "PHENYL TRIMETHICONE",
    "아모디메티콘": "AMODIMETHICONE",
    "디메티코놀": "DIMETHICONOL",
    "트리메틸실록시실리케이트": "TRIMETHYLSILOXYSILICATE",
    "BHT": "BHT",
    "뷰틸레이티드하이드록시톨루엔": "BHT",
    "BHA": "BHA",
    "뷰틸레이티드하이드록시아니솔": "BHA",
    "카페인": "CAFFEINE",
    "아미노산": "AMINO ACIDS",
    "아르기닌": "ARGININE",
    "글루타민산": "GLUTAMIC ACID",
    "글리신": "GLYCINE",
    "알라닌": "ALANINE",
    "세린": "SERINE",
    "프롤린": "PROLINE",
    "발린": "VALINE",
    "트레오닌": "THREONINE",
    "이소류신": "ISOLEUCINE",
    "류신": "LEUCINE",
    "아스파르트산": "ASPARTIC ACID",
    "페닐알라닌": "PHENYLALANINE",
    "히스티딘": "HISTIDINE",
    "라이신": "LYSINE",
    "메티오닌": "METHIONINE",
    "시스테인": "CYSTEINE",
    "트립토판": "TRYPTOPHAN",
    "타이로신": "TYROSINE",
}

# =============================================================================
# TRADENAME TO INCI MAPPING
# =============================================================================

TRADENAME_INCI_MAP = {
    # Vitamins
    "Vitamin A": "RETINOL",
    "Vitamin B1": "THIAMINE",
    "Vitamin B2": "RIBOFLAVIN",
    "Vitamin B3": "NIACINAMIDE",
    "Vitamin B5": "PANTHENOL",
    "Pro-Vitamin B5": "PANTHENOL",
    "D-Panthenol": "PANTHENOL",
    "DL-Panthenol": "PANTHENOL",
    "Vitamin B6": "PYRIDOXINE",
    "Vitamin B7": "BIOTIN",
    "Vitamin B9": "FOLIC ACID",
    "Vitamin B12": "CYANOCOBALAMIN",
    "Vitamin C": "ASCORBIC ACID",
    "L-Ascorbic Acid": "ASCORBIC ACID",
    "Vitamin D": "CHOLECALCIFEROL",
    "Vitamin D3": "CHOLECALCIFEROL",
    "Vitamin E": "TOCOPHEROL",
    "Vitamin K": "PHYTONADIONE",

    # Common trade names
    "AHA": "GLYCOLIC ACID",
    "Alpha Hydroxy Acid": "GLYCOLIC ACID",
    "BHA": "SALICYLIC ACID",
    "Beta Hydroxy Acid": "SALICYLIC ACID",
    "PHA": "GLUCONOLACTONE",
    "Polyhydroxy Acid": "GLUCONOLACTONE",

    "Hyaluronic Acid": "HYALURONIC ACID",
    "HA": "HYALURONIC ACID",
    "Squalane": "SQUALANE",
    "Squalene": "SQUALENE",
    "Niacinamide": "NIACINAMIDE",
    "Nicotinamide": "NIACINAMIDE",

    "Retinol": "RETINOL",
    "Retinyl Palmitate": "RETINYL PALMITATE",
    "Retinaldehyde": "RETINAL",
    "Retinal": "RETINAL",
    "Tretinoin": "RETINOIC ACID",

    "Glycerin": "GLYCERIN",
    "Glycerol": "GLYCERIN",
    "Glycerine": "GLYCERIN",

    "Allantoin": "ALLANTOIN",
    "Urea": "UREA",
    "Betaine": "BETAINE",
    "Trehalose": "TREHALOSE",

    "Adenosine": "ADENOSINE",
    "Caffeine": "CAFFEINE",
    "Coenzyme Q10": "UBIQUINONE",
    "CoQ10": "UBIQUINONE",
    "Ubiquinone": "UBIQUINONE",
    "Idebenone": "IDEBENONE",

    "Arbutin": "ARBUTIN",
    "Alpha Arbutin": "ALPHA-ARBUTIN",
    "Beta Arbutin": "BETA-ARBUTIN",
    "Kojic Acid": "KOJIC ACID",
    "Tranexamic Acid": "TRANEXAMIC ACID",
    "Glutathione": "GLUTATHIONE",
    "Glabridin": "GLABRIDIN",

    "Aloe Vera": "ALOE BARBADENSIS LEAF EXTRACT",
    "Green Tea Extract": "CAMELLIA SINENSIS LEAF EXTRACT",
    "Centella Asiatica": "CENTELLA ASIATICA EXTRACT",
    "Cica": "CENTELLA ASIATICA EXTRACT",
    "Madecassoside": "MADECASSOSIDE",
    "Asiaticoside": "ASIATICOSIDE",
    "Bisabolol": "ALPHA-BISABOLOL",
    "Alpha-Bisabolol": "ALPHA-BISABOLOL",

    "Ceramide NP": "CERAMIDE NP",
    "Ceramide AP": "CERAMIDE AP",
    "Ceramide EOP": "CERAMIDE EOP",
    "Phytosphingosine": "PHYTOSPHINGOSINE",
    "Cholesterol": "CHOLESTEROL",

    "Argireline": "ACETYL HEXAPEPTIDE-8",
    "Matrixyl": "PALMITOYL PENTAPEPTIDE-4",
    "Matrixyl 3000": "PALMITOYL TRIPEPTIDE-1",
    "Copper Peptide": "COPPER TRIPEPTIDE-1",
    "GHK-Cu": "COPPER TRIPEPTIDE-1",

    "Collagen": "COLLAGEN",
    "Marine Collagen": "SOLUBLE COLLAGEN",
    "Hydrolyzed Collagen": "HYDROLYZED COLLAGEN",
    "Elastin": "ELASTIN",

    "Jojoba Oil": "SIMMONDSIA CHINENSIS (JOJOBA) SEED OIL",
    "Argan Oil": "ARGANIA SPINOSA KERNEL OIL",
    "Tea Tree Oil": "MELALEUCA ALTERNIFOLIA (TEA TREE) LEAF OIL",
    "Rosehip Oil": "ROSA CANINA SEED OIL",
    "Shea Butter": "BUTYROSPERMUM PARKII (SHEA) BUTTER",
    "Cocoa Butter": "THEOBROMA CACAO (COCOA) SEED BUTTER",

    "Titanium Dioxide": "TITANIUM DIOXIDE",
    "Zinc Oxide": "ZINC OXIDE",
    "Avobenzone": "BUTYL METHOXYDIBENZOYLMETHANE",
    "Octinoxate": "ETHYLHEXYL METHOXYCINNAMATE",
    "Oxybenzone": "BENZOPHENONE-3",
    "Octocrylene": "OCTOCRYLENE",
    "Homosalate": "HOMOSALATE",
    "Tinosorb S": "BIS-ETHYLHEXYLOXYPHENOL METHOXYPHENYL TRIAZINE",

    "Phenoxyethanol": "PHENOXYETHANOL",
    "Benzyl Alcohol": "BENZYL ALCOHOL",
    "Ethylhexylglycerin": "ETHYLHEXYLGLYCERIN",
    "Sodium Benzoate": "SODIUM BENZOATE",
    "Potassium Sorbate": "POTASSIUM SORBATE",

    "Carbomer": "CARBOMER",
    "Xanthan Gum": "XANTHAN GUM",
    "Guar Gum": "GUAR GUM",

    "Dimethicone": "DIMETHICONE",
    "Cyclomethicone": "CYCLOMETHICONE",
    "Cyclopentasiloxane": "CYCLOPENTASILOXANE",

    "EDTA": "DISODIUM EDTA",
    "Citric Acid": "CITRIC ACID",
    "Lactic Acid": "LACTIC ACID",
    "Mandelic Acid": "MANDELIC ACID",
    "Azelaic Acid": "AZELAIC ACID",
    "Phytic Acid": "PHYTIC ACID",
}

# =============================================================================
# PLANT EXTRACT MAPPING
# =============================================================================

PLANT_EXTRACT_MAP = {
    # Leaf extracts
    "녹차": "CAMELLIA SINENSIS LEAF EXTRACT",
    "알로에": "ALOE BARBADENSIS LEAF EXTRACT",
    "티트리": "MELALEUCA ALTERNIFOLIA LEAF EXTRACT",
    "유칼립투스": "EUCALYPTUS GLOBULUS LEAF EXTRACT",
    "페퍼민트": "MENTHA PIPERITA LEAF EXTRACT",
    "박하": "MENTHA PIPERITA LEAF EXTRACT",
    "로즈마리": "ROSMARINUS OFFICINALIS LEAF EXTRACT",
    "올리브잎": "OLEA EUROPAEA LEAF EXTRACT",

    # Flower extracts
    "장미": "ROSA DAMASCENA FLOWER EXTRACT",
    "라벤더": "LAVANDULA ANGUSTIFOLIA FLOWER EXTRACT",
    "카모마일": "CHAMOMILLA RECUTITA FLOWER EXTRACT",
    "캐모마일": "CHAMOMILLA RECUTITA FLOWER EXTRACT",
    "재스민": "JASMINUM OFFICINALE FLOWER EXTRACT",
    "자스민": "JASMINUM OFFICINALE FLOWER EXTRACT",
    "국화": "CHRYSANTHEMUM INDICUM FLOWER EXTRACT",
    "연꽃": "NELUMBO NUCIFERA FLOWER EXTRACT",
    "백합": "LILIUM CANDIDUM FLOWER EXTRACT",
    "동백": "CAMELLIA JAPONICA FLOWER EXTRACT",
    "벚꽃": "PRUNUS SERRULATA FLOWER EXTRACT",
    "카렌둘라": "CALENDULA OFFICINALIS FLOWER EXTRACT",
    "금잔화": "CALENDULA OFFICINALIS FLOWER EXTRACT",

    # Root extracts
    "인삼": "PANAX GINSENG ROOT EXTRACT",
    "홍삼": "PANAX GINSENG ROOT EXTRACT",
    "감초": "GLYCYRRHIZA GLABRA ROOT EXTRACT",
    "황기": "ASTRAGALUS MEMBRANACEUS ROOT EXTRACT",
    "작약": "PAEONIA LACTIFLORA ROOT EXTRACT",

    # Fruit extracts
    "석류": "PUNICA GRANATUM FRUIT EXTRACT",
    "블루베리": "VACCINIUM ANGUSTIFOLIUM FRUIT EXTRACT",
    "포도": "VITIS VINIFERA FRUIT EXTRACT",
    "레몬": "CITRUS LIMON FRUIT EXTRACT",
    "오렌지": "CITRUS AURANTIUM DULCIS FRUIT EXTRACT",
    "자몽": "CITRUS GRANDIS FRUIT EXTRACT",
    "오이": "CUCUMIS SATIVUS FRUIT EXTRACT",
    "사과": "PYRUS MALUS FRUIT EXTRACT",
    "파파야": "CARICA PAPAYA FRUIT EXTRACT",
    "망고": "MANGIFERA INDICA FRUIT EXTRACT",
    "아보카도": "PERSEA GRATISSIMA FRUIT EXTRACT",
    "키위": "ACTINIDIA CHINENSIS FRUIT EXTRACT",

    # Seed extracts
    "포도씨": "VITIS VINIFERA SEED EXTRACT",
    "해바라기씨": "HELIANTHUS ANNUUS SEED EXTRACT",
    "참깨": "SESAMUM INDICUM SEED EXTRACT",
    "아마씨": "LINUM USITATISSIMUM SEED EXTRACT",

    # Whole plant extracts
    "병풀": "CENTELLA ASIATICA EXTRACT",
    "센텔라": "CENTELLA ASIATICA EXTRACT",
    "티카": "CENTELLA ASIATICA EXTRACT",
    "어성초": "HOUTTUYNIA CORDATA EXTRACT",
    "약모밀": "HOUTTUYNIA CORDATA EXTRACT",
    "쑥": "ARTEMISIA VULGARIS EXTRACT",
    "위치하젤": "HAMAMELIS VIRGINIANA EXTRACT",
    "알란토인": "ALLANTOIN",

    # Other
    "백년초": "OPUNTIA FICUS-INDICA EXTRACT",
    "선인장": "OPUNTIA FICUS-INDICA EXTRACT",
}

# =============================================================================
# CAS NUMBER MAPPING
# =============================================================================

CAS_NUMBER_MAP = {
    "NIACINAMIDE": "98-92-0",
    "GLYCERIN": "56-81-5",
    "HYALURONIC ACID": "9004-61-9",
    "SODIUM HYALURONATE": "9067-32-7",
    "BUTYLENE GLYCOL": "107-88-0",
    "PROPANEDIOL": "504-63-2",
    "PROPYLENE GLYCOL": "57-55-6",
    "TOCOPHEROL": "59-02-9",
    "TOCOPHERYL ACETATE": "58-95-7",
    "ASCORBIC ACID": "50-81-7",
    "RETINOL": "68-26-8",
    "RETINYL PALMITATE": "79-81-2",
    "ADENOSINE": "58-61-7",
    "PANTHENOL": "81-13-0",
    "ALLANTOIN": "97-59-6",
    "UREA": "57-13-6",
    "CAFFEINE": "58-08-2",
    "SALICYLIC ACID": "69-72-7",
    "GLYCOLIC ACID": "79-14-1",
    "LACTIC ACID": "50-21-5",
    "CITRIC ACID": "77-92-9",
    "ARBUTIN": "497-76-7",
    "ALPHA-ARBUTIN": "84380-01-8",
    "KOJIC ACID": "501-30-4",
    "TRANEXAMIC ACID": "1197-18-8",
    "GLUTATHIONE": "70-18-8",
    "CARBOMER": "9007-20-9",
    "XANTHAN GUM": "11138-66-2",
    "PHENOXYETHANOL": "122-99-6",
    "SODIUM BENZOATE": "532-32-1",
    "POTASSIUM SORBATE": "24634-61-5",
    "TITANIUM DIOXIDE": "13463-67-7",
    "ZINC OXIDE": "1314-13-2",
    "DIMETHICONE": "9006-65-9",
    "CYCLOPENTASILOXANE": "541-02-6",
    "SQUALANE": "111-01-3",
    "SQUALENE": "111-02-4",
    "UBIQUINONE": "303-98-0",
    "ALPHA-BISABOLOL": "23089-26-1",
    "BENZYL ALCOHOL": "100-51-6",
    "ETHYLHEXYLGLYCERIN": "70445-33-9",
    "1,2-HEXANEDIOL": "6920-22-5",
    "BETAINE": "107-43-7",
    "TREHALOSE": "99-20-7",
    "SODIUM CHLORIDE": "7647-14-5",
    "DISODIUM EDTA": "139-33-3",
    "BHT": "128-37-0",
    "SODIUM HYDROXIDE": "1310-73-2",
    "TRIETHANOLAMINE": "102-71-6",
    "CETYL ALCOHOL": "36653-82-4",
    "STEARYL ALCOHOL": "112-92-5",
    "CETEARYL ALCOHOL": "67762-27-0",
    "STEARIC ACID": "57-11-4",
    "PALMITIC ACID": "57-10-3",
    "OLEIC ACID": "112-80-1",
    "LINOLEIC ACID": "60-33-3",
    "ACETYL HEXAPEPTIDE-8": "616204-22-9",
    "PALMITOYL PENTAPEPTIDE-4": "214047-00-4",
    "COPPER TRIPEPTIDE-1": "49557-75-7",
    "CERAMIDE NP": "100403-19-8",
    "CERAMIDE AP": "100403-19-8",
    "PHYTOSPHINGOSINE": "554-62-1",
    "CHOLESTEROL": "57-88-5",
    "BENZOPHENONE-3": "131-57-7",
    "ETHYLHEXYL METHOXYCINNAMATE": "5466-77-3",
    "BUTYL METHOXYDIBENZOYLMETHANE": "70356-09-1",
    "HOMOSALATE": "118-56-9",
    "OCTOCRYLENE": "6197-30-4",
    "LINALOOL": "78-70-6",
    "LIMONENE": "5989-27-5",
    "CITRONELLOL": "106-22-9",
    "GERANIOL": "106-24-1",
    "EUGENOL": "97-53-0",
    "COUMARIN": "91-64-5",
}


# =============================================================================
# INCI CONVERTER CLASS
# =============================================================================

class InciConverter:
    """
    INCI Name Converter for cosmetic ingredients.

    Supports:
    - Korean to INCI conversion
    - INCI to Korean conversion
    - Tradename to INCI conversion
    - CAS number lookup
    - Batch conversion

    Example:
        converter = InciConverter()
        converter.korean_to_inci("나이아신아마이드")  # "NIACINAMIDE"
        converter.inci_to_korean("NIACINAMIDE")       # "나이아신아마이드"
        converter.tradename_to_inci("Vitamin B3")     # "NIACINAMIDE"
        converter.get_cas_number("NIACINAMIDE")       # "98-92-0"
    """

    def __init__(self):
        """Initialize the converter with mapping dictionaries."""
        self.korean_to_inci_map = KOREAN_INCI_MAP
        self.inci_to_korean_map = {v: k for k, v in KOREAN_INCI_MAP.items()}
        self.tradename_to_inci_map = TRADENAME_INCI_MAP
        self.plant_extract_map = PLANT_EXTRACT_MAP
        self.cas_number_map = CAS_NUMBER_MAP

    def korean_to_inci(self, name: str) -> Optional[str]:
        """
        Convert Korean ingredient name to INCI name.

        Args:
            name: Korean ingredient name (e.g., "나이아신아마이드")

        Returns:
            INCI name (e.g., "NIACINAMIDE") or None if not found
        """
        if not name:
            return None

        # Clean input
        name = name.strip()

        # Direct lookup
        if name in self.korean_to_inci_map:
            return self.korean_to_inci_map[name]

        # Try plant extract mapping
        if name in self.plant_extract_map:
            return self.plant_extract_map[name]

        # Try variations (remove spaces, add "추출물" suffix)
        name_no_space = name.replace(" ", "")
        if name_no_space in self.korean_to_inci_map:
            return self.korean_to_inci_map[name_no_space]

        # Try with "추출물" suffix
        if not name.endswith("추출물"):
            name_with_suffix = name + "추출물"
            if name_with_suffix in self.korean_to_inci_map:
                return self.korean_to_inci_map[name_with_suffix]

        return None

    def inci_to_korean(self, inci: str) -> Optional[str]:
        """
        Convert INCI name to Korean ingredient name.

        Args:
            inci: INCI name (e.g., "NIACINAMIDE")

        Returns:
            Korean name (e.g., "나이아신아마이드") or None if not found
        """
        if not inci:
            return None

        # Normalize to uppercase
        inci = inci.strip().upper()

        # Direct lookup
        if inci in self.inci_to_korean_map:
            return self.inci_to_korean_map[inci]

        return None

    def tradename_to_inci(self, name: str) -> Optional[str]:
        """
        Convert commercial/trade name to INCI name.

        Args:
            name: Trade name (e.g., "Vitamin B3")

        Returns:
            INCI name (e.g., "NIACINAMIDE") or None if not found
        """
        if not name:
            return None

        name = name.strip()

        # Direct lookup (case-insensitive)
        for key, value in self.tradename_to_inci_map.items():
            if key.lower() == name.lower():
                return value

        return None

    def get_cas_number(self, inci: str) -> Optional[str]:
        """
        Get CAS number for an INCI name.

        Args:
            inci: INCI name (e.g., "NIACINAMIDE")

        Returns:
            CAS number (e.g., "98-92-0") or None if not found
        """
        if not inci:
            return None

        inci = inci.strip().upper()
        return self.cas_number_map.get(inci)

    def get_cas_number_korean(self, korean_name: str) -> Optional[str]:
        """
        Get CAS number for a Korean ingredient name.

        Args:
            korean_name: Korean name (e.g., "나이아신아마이드")

        Returns:
            CAS number (e.g., "98-92-0") or None if not found
        """
        inci = self.korean_to_inci(korean_name)
        if inci:
            return self.get_cas_number(inci)
        return None

    def batch_convert(
        self,
        names: list,
        direction: str = "korean_to_inci",
        as_dict: bool = False
    ) -> Union[list, dict]:
        """
        Batch convert multiple ingredient names.

        Args:
            names: List of ingredient names
            direction: Conversion direction
                - "korean_to_inci": Korean to INCI (default)
                - "inci_to_korean": INCI to Korean
                - "tradename_to_inci": Trade name to INCI
            as_dict: If True, return dict with original names as keys

        Returns:
            List or dict of converted names
        """
        if direction == "korean_to_inci":
            converter_func = self.korean_to_inci
        elif direction == "inci_to_korean":
            converter_func = self.inci_to_korean
        elif direction == "tradename_to_inci":
            converter_func = self.tradename_to_inci
        else:
            raise ValueError(f"Invalid direction: {direction}")

        results = []
        result_dict = {}

        for name in names:
            converted = converter_func(name)
            results.append(converted if converted else name)
            result_dict[name] = converted if converted else name

        return result_dict if as_dict else results

    def get_tradenames(self, inci: str) -> list:
        """
        Get trade names for an INCI name.

        Args:
            inci: INCI name

        Returns:
            List of trade names
        """
        if not inci:
            return []

        inci = inci.strip().upper()
        tradenames = []

        for tradename, mapped_inci in self.tradename_to_inci_map.items():
            if mapped_inci == inci:
                tradenames.append(tradename)

        return tradenames

    def get_category(self, inci: str) -> Optional[str]:
        """
        Get ingredient category for an INCI name.

        Args:
            inci: INCI name

        Returns:
            Category name or None
        """
        # Define category patterns
        categories = {
            "Humectant": ["GLYCERIN", "BUTYLENE GLYCOL", "PROPANEDIOL",
                         "SODIUM HYALURONATE", "HYALURONIC ACID", "BETAINE",
                         "SORBITOL", "TREHALOSE", "UREA", "SODIUM PCA"],
            "Emollient": ["SQUALANE", "SQUALENE", "DIMETHICONE", "MINERAL OIL",
                         "PETROLATUM", "ISOPROPYL MYRISTATE"],
            "Active Ingredient": ["NIACINAMIDE", "RETINOL", "ADENOSINE",
                                  "ASCORBIC ACID", "ARBUTIN", "ALPHA-ARBUTIN",
                                  "TRANEXAMIC ACID", "KOJIC ACID", "UBIQUINONE"],
            "Preservative": ["PHENOXYETHANOL", "BENZYL ALCOHOL", "METHYLPARABEN",
                            "ETHYLPARABEN", "SODIUM BENZOATE", "POTASSIUM SORBATE"],
            "Emulsifier": ["CETEARYL ALCOHOL", "GLYCERYL STEARATE",
                          "POLYSORBATE 20", "POLYSORBATE 60", "POLYSORBATE 80"],
            "Surfactant": ["SODIUM LAURYL SULFATE", "COCAMIDOPROPYL BETAINE",
                          "SODIUM COCOYL GLUTAMATE"],
            "Thickener": ["CARBOMER", "XANTHAN GUM", "HYDROXYETHYLCELLULOSE"],
            "UV Filter": ["TITANIUM DIOXIDE", "ZINC OXIDE", "BENZOPHENONE-3",
                         "ETHYLHEXYL METHOXYCINNAMATE", "OCTOCRYLENE"],
            "Antioxidant": ["TOCOPHEROL", "TOCOPHERYL ACETATE", "BHT", "BHA"],
            "Vitamin": ["RETINOL", "TOCOPHEROL", "ASCORBIC ACID", "PANTHENOL",
                       "NIACINAMIDE", "BIOTIN", "THIAMINE", "RIBOFLAVIN"],
        }

        if not inci:
            return None

        inci = inci.strip().upper()

        for category, ingredients in categories.items():
            if inci in ingredients:
                return category

        # Check for extract patterns
        if "EXTRACT" in inci:
            return "Plant Extract"
        if "OIL" in inci:
            return "Oil"
        if "BUTTER" in inci:
            return "Butter"
        if "WATER" in inci or "AQUA" in inci:
            return "Solvent"

        return None

    def search(self, query: str) -> list:
        """
        Search for ingredients by partial name match.

        Args:
            query: Search query (Korean or INCI)

        Returns:
            List of matching (korean_name, inci_name) tuples
        """
        if not query:
            return []

        query = query.strip().lower()
        results = []

        # Search in Korean names
        for korean, inci in self.korean_to_inci_map.items():
            if query in korean.lower():
                results.append((korean, inci))

        # Search in INCI names
        for korean, inci in self.korean_to_inci_map.items():
            if query in inci.lower() and (korean, inci) not in results:
                results.append((korean, inci))

        return results

    def get_stats(self) -> dict:
        """
        Get statistics about the converter database.

        Returns:
            Dict with database statistics
        """
        return {
            "korean_to_inci_count": len(self.korean_to_inci_map),
            "tradename_to_inci_count": len(self.tradename_to_inci_map),
            "plant_extract_count": len(self.plant_extract_map),
            "cas_number_count": len(self.cas_number_map),
        }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_ingredient_list(korean_ingredients: list, separator: str = ", ") -> str:
    """
    Create INCI ingredient list from Korean names.

    Args:
        korean_ingredients: List of Korean ingredient names (in order)
        separator: Separator string (default: ", ")

    Returns:
        INCI ingredient list string

    Example:
        ingredients = ["정제수", "글리세린", "나이아신아마이드"]
        create_ingredient_list(ingredients)
        # "AQUA, GLYCERIN, NIACINAMIDE"
    """
    converter = InciConverter()
    results = converter.batch_convert(korean_ingredients, "korean_to_inci")
    return separator.join(results)


def validate_inci_format(inci: str) -> bool:
    """
    Validate INCI name format.

    Args:
        inci: INCI name to validate

    Returns:
        True if format is valid, False otherwise
    """
    if not inci:
        return False

    # INCI names should be uppercase
    if inci != inci.upper():
        return False

    # Check for invalid characters
    valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-() /,.'")
    if not all(c in valid_chars for c in inci):
        return False

    return True


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Command-line interface for INCI converter."""
    import sys

    converter = InciConverter()

    if len(sys.argv) < 2:
        print("INCI Converter - Korean Cosmetic Ingredient Name Converter")
        print("\nUsage:")
        print("  python inci_convert.py <name>           Convert Korean to INCI")
        print("  python inci_convert.py -i <inci>        Convert INCI to Korean")
        print("  python inci_convert.py -t <tradename>   Convert tradename to INCI")
        print("  python inci_convert.py -c <inci>        Get CAS number")
        print("  python inci_convert.py -s <query>       Search ingredients")
        print("  python inci_convert.py --stats          Show database statistics")
        print("\nExamples:")
        print('  python inci_convert.py "나이아신아마이드"')
        print('  python inci_convert.py -i "NIACINAMIDE"')
        print('  python inci_convert.py -t "Vitamin B3"')
        return

    if sys.argv[1] == "--stats":
        stats = converter.get_stats()
        print("\nINCI Converter Database Statistics:")
        print(f"  Korean to INCI mappings: {stats['korean_to_inci_count']}")
        print(f"  Tradename to INCI mappings: {stats['tradename_to_inci_count']}")
        print(f"  Plant extract mappings: {stats['plant_extract_count']}")
        print(f"  CAS number mappings: {stats['cas_number_count']}")
        return

    if sys.argv[1] == "-i" and len(sys.argv) >= 3:
        inci = " ".join(sys.argv[2:])
        result = converter.inci_to_korean(inci)
        if result:
            print(f"{inci} -> {result}")
        else:
            print(f"Not found: {inci}")
        return

    if sys.argv[1] == "-t" and len(sys.argv) >= 3:
        tradename = " ".join(sys.argv[2:])
        result = converter.tradename_to_inci(tradename)
        if result:
            print(f"{tradename} -> {result}")
        else:
            print(f"Not found: {tradename}")
        return

    if sys.argv[1] == "-c" and len(sys.argv) >= 3:
        inci = " ".join(sys.argv[2:])
        result = converter.get_cas_number(inci)
        if result:
            print(f"{inci} CAS Number: {result}")
        else:
            print(f"CAS number not found: {inci}")
        return

    if sys.argv[1] == "-s" and len(sys.argv) >= 3:
        query = " ".join(sys.argv[2:])
        results = converter.search(query)
        if results:
            print(f"\nSearch results for '{query}':")
            for korean, inci in results[:20]:  # Limit to 20 results
                print(f"  {korean} -> {inci}")
        else:
            print(f"No results found for: {query}")
        return

    # Default: Korean to INCI
    korean = " ".join(sys.argv[1:])
    result = converter.korean_to_inci(korean)
    if result:
        print(f"{korean} -> {result}")
        cas = converter.get_cas_number(result)
        if cas:
            print(f"CAS Number: {cas}")
    else:
        print(f"Not found: {korean}")


if __name__ == "__main__":
    main()
