---
name: rdkit-cosmetic
description: RDKit 기반 화장품 원료 분자 분석 스킬. 분자량, LogP, PSA, 수소결합 공여/수용체 등 물리화학적 특성 계산을 통해 피부 침투성 예측, HLB 추정, Lipinski Rule of Five 검증을 수행합니다. 신규 원료 평가 및 제형 설계에 활용됩니다.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT license
metadata:
    skill-author: EVAS Cosmetic
    original-source: K-Dense Inc. (claude-scientific-skills structure)
    version: 1.0.0
    rdkit-version: "2023.09.1+"
---

# RDKit Cosmetic Skill

## Overview

**RDKit**은 화학정보학(Cheminformatics) 분야에서 가장 널리 사용되는 오픈소스 라이브러리입니다. 이 스킬은 RDKit을 활용하여 화장품 원료의 분자 수준 분석을 수행합니다.

화장품 R&D에서 분자 특성 분석이 중요한 이유:
- **피부 침투성 예측**: LogP, 분자량, PSA를 통해 경피 흡수 가능성 평가
- **제형 적합성 평가**: 용해도 특성을 통한 제형 선택
- **안전성 스크리닝**: Lipinski 규칙을 통한 생체이용률 예측
- **HLB 추정**: 분자 구조 기반 HLB 예측으로 유화 시스템 설계

**RDKit 설치**: https://www.rdkit.org/docs/Install.html

```bash
# Conda 설치 (권장)
conda install -c conda-forge rdkit

# pip 설치
pip install rdkit
```

## When to Use This Skill

- **신규 원료 평가**: SMILES로부터 물리화학적 특성 추출
- **피부 침투성 예측**: 활성 성분의 경피 흡수 가능성 분석
- **유화제 특성 분석**: 분자 구조 기반 HLB 추정
- **원료 스크리닝**: 대량의 후보 물질 중 적합한 원료 선별
- **Lipinski 검증**: 약물 유사성(Drug-likeness) 평가
- **분자 시각화**: 2D/3D 분자 구조 생성

## Core Capabilities

### 1. SMILES 기반 분자 분석

SMILES(Simplified Molecular Input Line Entry System)는 분자 구조를 문자열로 표현하는 표준 표기법입니다.

#### 화장품 원료의 SMILES 예시

| 원료 | INCI명 | SMILES |
|------|--------|--------|
| 나이아신아마이드 | Niacinamide | `NC(=O)c1cccnc1` |
| 레티놀 | Retinol | `CC1=C(C(CCC1)(C)C)C=CC(=CC=CC(=CC=CO)C)C` |
| 아스코르빈산 | Ascorbic Acid | `C(C(C1C(=C(C(=O)O1)O)O)O)O` |
| 글리세린 | Glycerin | `C(C(CO)O)O` |
| 살리실산 | Salicylic Acid | `OC(=O)c1ccccc1O` |
| 하이드로퀴논 | Hydroquinone | `Oc1ccc(O)cc1` |
| 카페인 | Caffeine | `Cn1cnc2c1c(=O)n(c(=O)n2C)C` |
| 알란토인 | Allantoin | `C1(NC(NC1N=C(N)O)=O)=O` |

```python
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, rdMolDescriptors

def analyze_molecule(smiles: str) -> dict:
    """
    SMILES로부터 분자 특성 분석

    Args:
        smiles: SMILES 문자열

    Returns:
        분자 특성 딕셔너리
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")

    return {
        "smiles": smiles,
        "molecular_weight": round(Descriptors.MolWt(mol), 2),
        "logp": round(Descriptors.MolLogP(mol), 2),
        "tpsa": round(Descriptors.TPSA(mol), 2),  # Topological PSA
        "hbd": Lipinski.NumHDonors(mol),  # H-bond donors
        "hba": Lipinski.NumHAcceptors(mol),  # H-bond acceptors
        "rotatable_bonds": Descriptors.NumRotatableBonds(mol),
        "heavy_atoms": Lipinski.HeavyAtomCount(mol),
        "formula": rdMolDescriptors.CalcMolFormula(mol)
    }
```

### 2. 핵심 분자 기술자 (Molecular Descriptors)

화장품에서 중요한 분자 기술자:

#### LogP (Partition Coefficient)

옥탄올/물 분배계수로, 분자의 친유성/친수성 균형을 나타냅니다.

```
LogP = log10([분자]_octanol / [분자]_water)

LogP < 0  : 친수성 (수용성)
LogP 0-1  : 약한 친유성
LogP 1-3  : 중간 친유성 (피부 침투 최적)
LogP 3-5  : 강한 친유성
LogP > 5  : 매우 친유성 (피부 잔류)
```

```python
def calculate_logp(smiles: str) -> float:
    """Crippen 방법으로 LogP 계산"""
    mol = Chem.MolFromSmiles(smiles)
    return round(Descriptors.MolLogP(mol), 2)

# 예시
print(calculate_logp("NC(=O)c1cccnc1"))  # Niacinamide: LogP = -0.37 (친수성)
print(calculate_logp("OC(=O)c1ccccc1O"))  # Salicylic Acid: LogP = 2.24 (중간)
```

#### 분자량 (Molecular Weight)

```
< 500 Da  : 피부 침투 가능 (Lipinski 기준)
300-500 Da: 최적 피부 침투 범위
> 500 Da  : 피부 침투 제한적 (거대 분자)
```

```python
def calculate_mw(smiles: str) -> float:
    """분자량 계산"""
    mol = Chem.MolFromSmiles(smiles)
    return round(Descriptors.MolWt(mol), 2)
```

#### PSA (Polar Surface Area)

극성 표면적 - 피부 장벽 통과와 관련:

```
PSA < 60 Å²  : 우수한 피부 침투
PSA 60-140 Å²: 보통 침투
PSA > 140 Å² : 제한적 침투
```

```python
def calculate_psa(smiles: str) -> float:
    """위상적 극성 표면적 계산"""
    mol = Chem.MolFromSmiles(smiles)
    return round(Descriptors.TPSA(mol), 2)
```

#### HBD/HBA (Hydrogen Bond Donors/Acceptors)

수소 결합 공여체/수용체 수:

```
HBD (NH, OH 등): ≤ 5 (Lipinski 기준)
HBA (N, O 등)  : ≤ 10 (Lipinski 기준)

수소결합이 많을수록:
- 수용성 증가
- 피부 침투성 감소
```

```python
def count_hbd_hba(smiles: str) -> tuple:
    """수소결합 공여체/수용체 개수"""
    mol = Chem.MolFromSmiles(smiles)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)
    return hbd, hba
```

### 3. Lipinski's Rule of Five (Ro5)

약물 유사성 평가를 위한 경험적 규칙 - 화장품 활성 성분의 생체이용률 예측에도 활용:

```
Lipinski Rule of Five:
1. 분자량 ≤ 500 Da
2. LogP ≤ 5
3. 수소결합 공여체(HBD) ≤ 5
4. 수소결합 수용체(HBA) ≤ 10

→ 2개 이상 위반 시 낮은 경구 생체이용률
→ 화장품: 피부 침투성 예측에 참고
```

```python
def check_lipinski(smiles: str) -> dict:
    """
    Lipinski Rule of Five 검증

    Returns:
        {
            "passes": bool,
            "violations": int,
            "details": {
                "mw": {"value": float, "pass": bool},
                "logp": {"value": float, "pass": bool},
                "hbd": {"value": int, "pass": bool},
                "hba": {"value": int, "pass": bool}
            }
        }
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES")

    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)

    violations = 0
    details = {}

    details["mw"] = {"value": round(mw, 2), "pass": mw <= 500}
    if mw > 500: violations += 1

    details["logp"] = {"value": round(logp, 2), "pass": logp <= 5}
    if logp > 5: violations += 1

    details["hbd"] = {"value": hbd, "pass": hbd <= 5}
    if hbd > 5: violations += 1

    details["hba"] = {"value": hba, "pass": hba <= 10}
    if hba > 10: violations += 1

    return {
        "passes": violations <= 1,
        "violations": violations,
        "details": details
    }
```

### 4. 피부 침투성 예측

분자 특성 기반 경피 흡수 예측:

```python
def predict_skin_penetration(smiles: str) -> dict:
    """
    피부 침투성 예측 (Bos & Meinardi 규칙 기반)

    기준:
    - MW < 500 Da
    - LogP 1-3 (최적)
    - 충분한 친유성(각질층 통과)과 친수성(진피층 이동) 균형

    Returns:
        {
            "penetration_score": float (0-100),
            "classification": str,
            "factors": dict
        }
    """
    mol = Chem.MolFromSmiles(smiles)

    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    psa = Descriptors.TPSA(mol)

    # 점수 계산 (단순 모델)
    score = 100

    # MW 패널티
    if mw > 500:
        score -= min(50, (mw - 500) / 10)
    elif mw < 150:
        score -= 10  # 너무 작으면 휘발 가능성

    # LogP 최적 범위
    if 1 <= logp <= 3:
        score += 10  # 보너스
    elif logp < 0:
        score -= 20 * abs(logp)  # 친수성 과다
    elif logp > 5:
        score -= 10 * (logp - 5)  # 친유성 과다

    # PSA 패널티
    if psa > 140:
        score -= (psa - 140) / 5

    score = max(0, min(100, score))

    # 분류
    if score >= 70:
        classification = "Excellent"
    elif score >= 50:
        classification = "Good"
    elif score >= 30:
        classification = "Moderate"
    else:
        classification = "Poor"

    return {
        "penetration_score": round(score, 1),
        "classification": classification,
        "factors": {
            "mw": round(mw, 2),
            "logp": round(logp, 2),
            "psa": round(psa, 2)
        },
        "optimal_ranges": {
            "mw": "< 500 Da",
            "logp": "1-3",
            "psa": "< 140 Å²"
        }
    }
```

### 5. HLB 추정 (구조 기반)

분자 구조로부터 HLB를 추정하는 방법:

```python
def estimate_hlb_from_structure(smiles: str) -> dict:
    """
    분자 구조 기반 HLB 추정

    Griffin 방법 변형 사용:
    HLB ≈ 20 × (친수성 기여 / 총 분자량)

    Davies 방법 근사 사용 시:
    HLB = 7 + Σ(친수성 기값) - 0.475 × n_carbons
    """
    mol = Chem.MolFromSmiles(smiles)

    mw = Descriptors.MolWt(mol)

    # 친수성 기 계산
    # -OH (알코올)
    n_oh = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[OX2H]')))
    # -O- (에테르)
    n_ether = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[OD2]([#6])[#6]')))
    # -COOH (카르복실산)
    n_cooh = len(mol.GetSubstructMatches(Chem.MolFromSmarts('C(=O)[OH]')))
    # C=O (카르보닐)
    n_carbonyl = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[CX3]=[OX1]')))
    # PEO 단위 추정
    n_peo = len(mol.GetSubstructMatches(Chem.MolFromSmarts('OCCO')))

    # Davies 방법 근사
    hydrophilic_sum = (
        n_oh * 1.9 +
        n_ether * 1.3 +
        n_cooh * 2.1 +
        n_peo * 2.6  # -OCH2CH2O- 근사
    )

    # 탄소 수 계산
    n_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    lipophilic_sum = n_carbons * 0.475

    hlb_davies = 7 + hydrophilic_sum - lipophilic_sum

    # Griffin 방법 근사 (산소 기반)
    n_oxygen = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    hydrophilic_mw = n_oxygen * 16 + n_oh * 17  # 근사값
    hlb_griffin = 20 * (hydrophilic_mw / mw) if mw > 0 else 0

    # 두 방법의 평균
    hlb_estimated = (hlb_davies + hlb_griffin) / 2

    return {
        "hlb_davies": round(hlb_davies, 1),
        "hlb_griffin": round(hlb_griffin, 1),
        "hlb_average": round(hlb_estimated, 1),
        "structure_features": {
            "OH_groups": n_oh,
            "ether_groups": n_ether,
            "COOH_groups": n_cooh,
            "carbons": n_carbons
        },
        "note": "추정값임. 실험적 검증 권장."
    }
```

### 6. 화장품 원료 SMILES 데이터베이스

주요 화장품 원료의 SMILES 컬렉션:

```python
COSMETIC_INGREDIENTS_SMILES = {
    # 활성 성분
    "niacinamide": {
        "inci": "Niacinamide",
        "smiles": "NC(=O)c1cccnc1",
        "cas": "98-92-0",
        "function": "Skin conditioning"
    },
    "retinol": {
        "inci": "Retinol",
        "smiles": "CC1=C(C(CCC1)(C)C)/C=C/C(=C/C=C/C(=C/CO)/C)/C",
        "cas": "68-26-8",
        "function": "Anti-aging"
    },
    "ascorbic_acid": {
        "inci": "Ascorbic Acid",
        "smiles": "C([C@@H]([C@@H]1C(=C(C(=O)O1)O)O)O)O",
        "cas": "50-81-7",
        "function": "Antioxidant"
    },
    "salicylic_acid": {
        "inci": "Salicylic Acid",
        "smiles": "OC(=O)c1ccccc1O",
        "cas": "69-72-7",
        "function": "Keratolytic"
    },
    "glycolic_acid": {
        "inci": "Glycolic Acid",
        "smiles": "OCC(=O)O",
        "cas": "79-14-1",
        "function": "AHA, Exfoliant"
    },
    "lactic_acid": {
        "inci": "Lactic Acid",
        "smiles": "CC(C(=O)O)O",
        "cas": "50-21-5",
        "function": "AHA, Moisturizing"
    },
    "hyaluronic_acid_monomer": {
        "inci": "Hyaluronic Acid (repeat unit)",
        "smiles": "CC(=O)NC1C(C(C(OC1O)CO)O)OC2C(C(C(C(O2)C(=O)O)O)O)O",
        "cas": "9004-61-9",
        "function": "Humectant"
    },
    "alpha_arbutin": {
        "inci": "Alpha-Arbutin",
        "smiles": "OC[C@H]1O[C@H](Oc2ccc(O)cc2)[C@H](O)[C@@H](O)[C@@H]1O",
        "cas": "84380-01-8",
        "function": "Skin brightening"
    },
    "kojic_acid": {
        "inci": "Kojic Acid",
        "smiles": "OCC1=CC(=O)C(O)=CO1",
        "cas": "501-30-4",
        "function": "Tyrosinase inhibitor"
    },
    "tranexamic_acid": {
        "inci": "Tranexamic Acid",
        "smiles": "NCC1CCC(CC1)C(=O)O",
        "cas": "1197-18-8",
        "function": "Brightening"
    },

    # 보습제
    "glycerin": {
        "inci": "Glycerin",
        "smiles": "C(C(CO)O)O",
        "cas": "56-81-5",
        "function": "Humectant"
    },
    "propylene_glycol": {
        "inci": "Propylene Glycol",
        "smiles": "CC(CO)O",
        "cas": "57-55-6",
        "function": "Humectant, Solvent"
    },
    "butylene_glycol": {
        "inci": "Butylene Glycol",
        "smiles": "CC(CCO)O",
        "cas": "107-88-0",
        "function": "Humectant, Solvent"
    },
    "pentylene_glycol": {
        "inci": "Pentylene Glycol",
        "smiles": "CCCCC(O)CO",
        "cas": "5343-92-0",
        "function": "Humectant, Antimicrobial"
    },

    # 방부제
    "phenoxyethanol": {
        "inci": "Phenoxyethanol",
        "smiles": "OCCOc1ccccc1",
        "cas": "122-99-6",
        "function": "Preservative"
    },
    "benzoic_acid": {
        "inci": "Benzoic Acid",
        "smiles": "OC(=O)c1ccccc1",
        "cas": "65-85-0",
        "function": "Preservative"
    },
    "sorbic_acid": {
        "inci": "Sorbic Acid",
        "smiles": "CC=CC=CC(=O)O",
        "cas": "110-44-1",
        "function": "Preservative"
    },

    # UV 필터
    "avobenzone": {
        "inci": "Avobenzone",
        "smiles": "CC(C)(C)c1ccc(C(=O)CC(=O)c2ccc(OC)cc2)cc1",
        "cas": "70356-09-1",
        "function": "UVA filter"
    },
    "octinoxate": {
        "inci": "Ethylhexyl Methoxycinnamate",
        "smiles": "CCCCC(CC)COC(=O)/C=C/c1ccc(OC)cc1",
        "cas": "5466-77-3",
        "function": "UVB filter"
    },
    "octocrylene": {
        "inci": "Octocrylene",
        "smiles": "CCCCC(CC)COC(=O)C(=C1CCCC1=O)c1ccccc1",
        "cas": "6197-30-4",
        "function": "UVB filter"
    },

    # 유화제 (단순 구조)
    "sorbitan_stearate": {
        "inci": "Sorbitan Stearate",
        "smiles": "CCCCCCCCCCCCCCCCCC(=O)OC1C(OC(C1O)CO)O",  # 단순화
        "cas": "1338-41-6",
        "function": "W/O Emulsifier"
    },
}
```

## Common Workflows

### Workflow 1: 신규 원료 전체 분석

```python
def full_ingredient_analysis(smiles: str, inci_name: str = None) -> dict:
    """
    화장품 원료 종합 분석

    수행 내용:
    1. 기본 분자 특성
    2. Lipinski 규칙 검증
    3. 피부 침투성 예측
    4. HLB 추정
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")

    # 1. 기본 특성
    basic = analyze_molecule(smiles)

    # 2. Lipinski
    lipinski = check_lipinski(smiles)

    # 3. 피부 침투성
    penetration = predict_skin_penetration(smiles)

    # 4. HLB 추정
    hlb = estimate_hlb_from_structure(smiles)

    return {
        "inci_name": inci_name or "Unknown",
        "smiles": smiles,
        "molecular_properties": basic,
        "lipinski_analysis": lipinski,
        "skin_penetration": penetration,
        "hlb_estimation": hlb,
        "summary": {
            "mw": f"{basic['molecular_weight']} Da",
            "logp": basic['logp'],
            "psa": f"{basic['tpsa']} Å²",
            "penetration": penetration['classification'],
            "lipinski_pass": lipinski['passes']
        }
    }

# 사용 예시
result = full_ingredient_analysis(
    smiles="NC(=O)c1cccnc1",
    inci_name="Niacinamide"
)
```

### Workflow 2: 대량 원료 스크리닝

```python
def screen_ingredients(ingredients: list, criteria: dict = None) -> list:
    """
    여러 원료를 기준에 따라 스크리닝

    Args:
        ingredients: [{"name": str, "smiles": str}, ...]
        criteria: {
            "max_mw": 500,
            "logp_range": (-1, 4),
            "max_psa": 140,
            "require_lipinski": True
        }

    Returns:
        필터링된 원료 리스트 (점수 포함)
    """
    if criteria is None:
        criteria = {
            "max_mw": 500,
            "logp_range": (-1, 5),
            "max_psa": 140,
            "require_lipinski": True
        }

    results = []

    for ing in ingredients:
        try:
            analysis = full_ingredient_analysis(ing["smiles"], ing["name"])
            props = analysis["molecular_properties"]

            # 기준 확인
            passes = True
            flags = []

            if props["molecular_weight"] > criteria.get("max_mw", 500):
                passes = False
                flags.append("MW too high")

            logp_min, logp_max = criteria.get("logp_range", (-1, 5))
            if not (logp_min <= props["logp"] <= logp_max):
                passes = False
                flags.append(f"LogP outside range ({logp_min}-{logp_max})")

            if props["tpsa"] > criteria.get("max_psa", 140):
                passes = False
                flags.append("PSA too high")

            if criteria.get("require_lipinski") and not analysis["lipinski_analysis"]["passes"]:
                passes = False
                flags.append("Lipinski violation")

            results.append({
                "name": ing["name"],
                "passes_criteria": passes,
                "flags": flags,
                "penetration_score": analysis["skin_penetration"]["penetration_score"],
                "properties": analysis["summary"]
            })

        except Exception as e:
            results.append({
                "name": ing["name"],
                "error": str(e)
            })

    # 점수순 정렬
    results.sort(key=lambda x: x.get("penetration_score", 0), reverse=True)

    return results
```

### Workflow 3: 유사 원료 검색 (분자 유사성)

```python
from rdkit.Chem import AllChem
from rdkit import DataStructs

def find_similar_ingredients(query_smiles: str, database: list,
                              threshold: float = 0.7) -> list:
    """
    분자 지문(Fingerprint) 기반 유사 원료 검색

    Args:
        query_smiles: 검색 기준 분자의 SMILES
        database: [{"name": str, "smiles": str}, ...]
        threshold: Tanimoto 유사도 임계값 (0-1)

    Returns:
        유사도 순 정렬된 결과
    """
    query_mol = Chem.MolFromSmiles(query_smiles)
    query_fp = AllChem.GetMorganFingerprintAsBitVect(query_mol, 2, nBits=2048)

    results = []

    for item in database:
        mol = Chem.MolFromSmiles(item["smiles"])
        if mol:
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
            similarity = DataStructs.TanimotoSimilarity(query_fp, fp)

            if similarity >= threshold:
                results.append({
                    "name": item["name"],
                    "smiles": item["smiles"],
                    "similarity": round(similarity, 3)
                })

    # 유사도 순 정렬
    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results
```

### Workflow 4: 분자 시각화

```python
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D

def visualize_molecule(smiles: str, filename: str = None,
                        size: tuple = (400, 300)) -> str:
    """
    분자 구조 이미지 생성

    Args:
        smiles: SMILES 문자열
        filename: 저장할 파일명 (None이면 저장 안 함)
        size: 이미지 크기 (width, height)

    Returns:
        SVG 문자열 또는 저장된 파일 경로
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES")

    # 2D 좌표 계산
    AllChem.Compute2DCoords(mol)

    if filename:
        if filename.endswith('.png'):
            img = Draw.MolToImage(mol, size=size)
            img.save(filename)
            return filename
        elif filename.endswith('.svg'):
            drawer = rdMolDraw2D.MolDraw2DSVG(size[0], size[1])
            drawer.DrawMolecule(mol)
            drawer.FinishDrawing()
            svg = drawer.GetDrawingText()
            with open(filename, 'w') as f:
                f.write(svg)
            return filename

    # SVG 반환
    drawer = rdMolDraw2D.MolDraw2DSVG(size[0], size[1])
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    return drawer.GetDrawingText()
```

## Best Practices

### 1. SMILES 검증

```python
def validate_smiles(smiles: str) -> bool:
    """SMILES 유효성 검증"""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False
    # 추가 검증: 원자 수, 결합 등
    return mol.GetNumAtoms() > 0
```

### 2. 정규화 (Canonicalization)

```python
def canonicalize_smiles(smiles: str) -> str:
    """표준 SMILES로 변환"""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES")
    return Chem.MolToSmiles(mol, canonical=True)
```

### 3. 에러 핸들링

```python
def safe_analyze(smiles: str) -> dict:
    """안전한 분자 분석 (에러 처리 포함)"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return {"error": "Invalid SMILES", "smiles": smiles}

        return {
            "smiles": smiles,
            "canonical_smiles": Chem.MolToSmiles(mol, canonical=True),
            "mw": round(Descriptors.MolWt(mol), 2),
            "logp": round(Descriptors.MolLogP(mol), 2),
            "error": None
        }
    except Exception as e:
        return {"error": str(e), "smiles": smiles}
```

### 4. 배치 처리 최적화

```python
def batch_analyze(smiles_list: list, parallel: bool = False) -> list:
    """
    대량 분자 분석

    Args:
        smiles_list: SMILES 리스트
        parallel: 병렬 처리 여부
    """
    if parallel:
        # multiprocessing 사용
        from multiprocessing import Pool
        with Pool() as p:
            results = p.map(safe_analyze, smiles_list)
    else:
        results = [safe_analyze(s) for s in smiles_list]

    return results
```

## Reference Files

상세 정보는 아래 참조 문서 확인:

| 파일 | 내용 |
|------|------|
| `references/molecular_descriptors.md` | 핵심 분자 기술자 상세 설명 |
| `references/cosmetic_applications.md` | 화장품 특화 RDKit 활용 사례 |

## Scripts

| 스크립트 | 기능 |
|---------|------|
| `scripts/molecular_analyzer.py` | 분자 특성 계산 CLI 도구 |

## Troubleshooting

### 문제: RDKit 설치 오류

```
원인: conda/pip 환경 충돌
해결:
1. 새 가상환경 생성: conda create -n rdkit_env python=3.10
2. RDKit 단독 설치: conda install -c conda-forge rdkit
```

### 문제: SMILES 파싱 실패

```
원인 1: 잘못된 SMILES 문법
해결: SMILES 검증 도구 사용 (https://cactus.nci.nih.gov/translate/)

원인 2: 입체화학 표기 오류
해결: 입체화학 제거 후 재시도
    smiles = smiles.replace('@', '').replace('/', '').replace('\\', '')
```

### 문제: 대용량 처리 시 메모리 부족

```
원인: 분자 객체 누적
해결:
1. 배치 단위 처리
2. 명시적 메모리 해제: del mol
3. Generator 패턴 사용
```

## Additional Resources

- **RDKit 공식 문서**: https://www.rdkit.org/docs/
- **SMILES 튜토리얼**: https://www.daylight.com/dayhtml/doc/theory/theory.smiles.html
- **PubChem** (SMILES 검색): https://pubchem.ncbi.nlm.nih.gov/
- **ChemSpider**: https://www.chemspider.com/
- **RDKit Cookbook**: https://www.rdkit.org/docs/Cookbook.html

## Quick Reference

```python
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

# SMILES로부터 분자 객체 생성
mol = Chem.MolFromSmiles("NC(=O)c1cccnc1")  # Niacinamide

# 분자량
mw = Descriptors.MolWt(mol)  # 122.13

# LogP (Crippen)
logp = Descriptors.MolLogP(mol)  # -0.37

# PSA
psa = Descriptors.TPSA(mol)  # 56.0

# 수소결합 공여/수용체
hbd = Lipinski.NumHDonors(mol)  # 1
hba = Lipinski.NumHAcceptors(mol)  # 2

# 회전 결합
rot = Descriptors.NumRotatableBonds(mol)  # 1

# 분자식
from rdkit.Chem import rdMolDescriptors
formula = rdMolDescriptors.CalcMolFormula(mol)  # C6H6N2O
```

## Summary

**rdkit-cosmetic** 스킬은 화장품 원료의 분자 수준 분석을 위한 강력한 도구입니다:

1. **분자 특성 계산**: 분자량, LogP, PSA, HBD/HBA
2. **피부 침투성 예측**: 분자 특성 기반 경피 흡수 예측
3. **Lipinski 검증**: 생체이용률/피부 침투 적합성 평가
4. **HLB 추정**: 분자 구조 기반 유화제 특성 예측
5. **유사 원료 검색**: 분자 지문 기반 유사성 분석

신규 원료 평가, 제형 설계, 대량 스크리닝에 활용하여 R&D 효율성을 높이세요.
