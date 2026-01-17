# RDKit Cosmetic Applications

## 화장품 R&D를 위한 RDKit 활용 사례

이 문서는 RDKit을 화장품 연구개발에 실제로 적용하는 방법과 사례를 제공합니다.

---

## 1. 피부 침투성 예측

### Potts-Guy Equation

피부 투과계수(Permeability coefficient) 예측의 대표적 모델:

```
log Kp = 0.71 × LogP - 0.0061 × MW - 2.72

Kp: 투과계수 (cm/s)
LogP: 옥탄올/물 분배계수
MW: 분자량 (Da)
```

```python
from rdkit import Chem
from rdkit.Chem import Descriptors
import math

def predict_skin_permeability(smiles: str) -> dict:
    """
    Potts-Guy 방정식 기반 피부 투과계수 예측

    Returns:
        log_kp: log10(투과계수)
        kp: 투과계수 (cm/s)
        permeation_rate: 침투 속도 등급
    """
    mol = Chem.MolFromSmiles(smiles)

    logp = Descriptors.MolLogP(mol)
    mw = Descriptors.MolWt(mol)

    # Potts-Guy equation
    log_kp = 0.71 * logp - 0.0061 * mw - 2.72
    kp = 10 ** log_kp

    # 침투 속도 분류
    if log_kp > -3:
        rate = "Very fast"
    elif log_kp > -4:
        rate = "Fast"
    elif log_kp > -5:
        rate = "Moderate"
    elif log_kp > -6:
        rate = "Slow"
    else:
        rate = "Very slow"

    return {
        "smiles": smiles,
        "logp": round(logp, 2),
        "mw": round(mw, 2),
        "log_kp": round(log_kp, 2),
        "kp_cm_per_s": f"{kp:.2e}",
        "permeation_rate": rate
    }

# 예시
results = [
    predict_skin_permeability("NC(=O)c1cccnc1"),      # Niacinamide
    predict_skin_permeability("OC(=O)c1ccccc1O"),    # Salicylic Acid
    predict_skin_permeability("C(C(CO)O)O"),         # Glycerin
]
for r in results:
    print(f"{r['smiles'][:20]}: log Kp = {r['log_kp']}, Rate = {r['permeation_rate']}")
```

### 피부층별 침투 예측

```python
def predict_layer_penetration(smiles: str) -> dict:
    """
    피부 각 층에서의 예상 거동 예측

    피부 구조:
    1. 각질층 (Stratum Corneum): 친유성 장벽
    2. 생존 표피 (Viable Epidermis): 수성 환경
    3. 진피 (Dermis): 혈관, 수성 환경
    """
    mol = Chem.MolFromSmiles(smiles)

    logp = Descriptors.MolLogP(mol)
    mw = Descriptors.MolWt(mol)
    psa = Descriptors.TPSA(mol)

    layers = {}

    # 각질층 (Stratum Corneum)
    # LogP 1-3이 최적
    if mw > 500:
        layers["stratum_corneum"] = {
            "penetration": "Blocked",
            "reason": "MW too high for intercellular pathway"
        }
    elif logp < 0:
        layers["stratum_corneum"] = {
            "penetration": "Difficult",
            "reason": "Too hydrophilic for lipid matrix"
        }
    elif 1 <= logp <= 3:
        layers["stratum_corneum"] = {
            "penetration": "Optimal",
            "reason": "Good lipophilicity for SC penetration"
        }
    elif logp > 5:
        layers["stratum_corneum"] = {
            "penetration": "Retention",
            "reason": "May accumulate in SC due to high lipophilicity"
        }
    else:
        layers["stratum_corneum"] = {
            "penetration": "Moderate",
            "reason": "Acceptable lipophilicity"
        }

    # 생존 표피 (Viable Epidermis)
    if logp > 4:
        layers["viable_epidermis"] = {
            "penetration": "Limited",
            "reason": "Too lipophilic for aqueous environment"
        }
    elif psa > 140:
        layers["viable_epidermis"] = {
            "penetration": "Slow",
            "reason": "High polarity may slow diffusion"
        }
    else:
        layers["viable_epidermis"] = {
            "penetration": "Good",
            "reason": "Compatible with aqueous matrix"
        }

    # 진피 (Dermis)
    if logp > 3:
        layers["dermis"] = {
            "penetration": "Limited",
            "reason": "May not reach deeper dermis"
        }
    else:
        layers["dermis"] = {
            "penetration": "Possible",
            "reason": "Can diffuse through aqueous dermis"
        }

    # 전체 평가
    sc_ok = layers["stratum_corneum"]["penetration"] in ["Optimal", "Moderate"]
    ve_ok = layers["viable_epidermis"]["penetration"] in ["Good", "Slow"]
    d_ok = layers["dermis"]["penetration"] == "Possible"

    overall = "Surface" if not sc_ok else "Epidermis" if not d_ok else "Dermal"

    return {
        "layers": layers,
        "deepest_penetration": overall,
        "parameters": {
            "mw": round(mw, 2),
            "logp": round(logp, 2),
            "psa": round(psa, 2)
        }
    }
```

---

## 2. HLB 추정 (유화제 특성)

### Griffin 방법 기반 HLB 추정

```python
def estimate_hlb_griffin(smiles: str) -> dict:
    """
    Griffin 방법 근사를 사용한 HLB 추정

    HLB = 20 × (Mh / M)
    Mh = 친수성 부분 분자량
    M = 전체 분자량
    """
    mol = Chem.MolFromSmiles(smiles)

    mw = Descriptors.MolWt(mol)

    # 친수성 원자 (O, N) 기여 추정
    hydrophilic_mw = 0

    for atom in mol.GetAtoms():
        symbol = atom.GetSymbol()
        if symbol == 'O':
            hydrophilic_mw += 16  # O 원자량
            # -OH 추가 (수소 포함)
            if atom.GetTotalNumHs() > 0:
                hydrophilic_mw += 1  # H 원자량
        elif symbol == 'N':
            hydrophilic_mw += 14  # N 원자량
            hydrophilic_mw += atom.GetTotalNumHs()  # 연결된 H

    # HLB 계산
    hlb = 20 * (hydrophilic_mw / mw) if mw > 0 else 0

    # 범위 제한 (0-20)
    hlb = max(0, min(20, hlb))

    # 분류
    if hlb < 4:
        classification = "W/O emulsifier"
    elif hlb < 8:
        classification = "Wetting agent / W/O"
    elif hlb < 12:
        classification = "O/W emulsifier"
    elif hlb < 16:
        classification = "Detergent / O/W"
    else:
        classification = "Solubilizer"

    return {
        "hlb_estimated": round(hlb, 1),
        "classification": classification,
        "hydrophilic_mw": round(hydrophilic_mw, 2),
        "total_mw": round(mw, 2),
        "note": "Estimation based on Griffin method approximation"
    }
```

### Davies 방법 기반 HLB 추정

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

def estimate_hlb_davies(smiles: str) -> dict:
    """
    Davies 방법을 사용한 HLB 추정

    HLB = 7 + Σ(친수성 기값) - 0.475 × (탄소 수)
    """
    mol = Chem.MolFromSmiles(smiles)

    # 기능기 패턴 (SMARTS)
    patterns = {
        "SO4Na": "[S](=[O])(=[O])([O-])",
        "COOH": "C(=O)[OH]",
        "COO_salt": "C(=O)[O-]",
        "OH_free": "[OX2H]",
        "O_ether": "[OD2]([#6])[#6]",
        "NH2": "[NH2]",
        "NH": "[NH]",
    }

    # Davies 그룹 값
    davies_values = {
        "SO4Na": 38.7,
        "COOH": 2.1,
        "COO_salt": 19.1,  # -COONa 근사
        "OH_free": 1.9,
        "O_ether": 1.3,
        "NH2": 9.4,  # tertiary amine 근사
        "NH": 4.7,   # secondary amine 근사
    }

    # 기능기 카운트
    hydrophilic_sum = 0
    group_counts = {}

    for name, smarts in patterns.items():
        pattern = Chem.MolFromSmarts(smarts)
        if pattern:
            matches = mol.GetSubstructMatches(pattern)
            count = len(matches)
            if count > 0:
                group_counts[name] = count
                hydrophilic_sum += count * davies_values.get(name, 0)

    # 탄소 수
    n_carbons = sum(1 for a in mol.GetAtoms() if a.GetSymbol() == 'C')

    # 친유성 기여
    lipophilic_sum = 0.475 * n_carbons

    # HLB 계산
    hlb = 7 + hydrophilic_sum - lipophilic_sum

    return {
        "hlb_davies": round(hlb, 1),
        "hydrophilic_contribution": round(hydrophilic_sum, 2),
        "lipophilic_contribution": round(lipophilic_sum, 2),
        "carbon_count": n_carbons,
        "functional_groups": group_counts,
        "note": "Davies method estimation"
    }
```

---

## 3. 용해도 예측

### ESOL (Estimated SOLubility)

수용해도 예측 모델:

```python
def predict_aqueous_solubility(smiles: str) -> dict:
    """
    Delaney ESOL 방법 기반 수용해도 예측

    log S = 0.16 - 0.63 × cLogP - 0.0062 × MW + 0.066 × RB
            - 0.74 × AP

    S: 몰 용해도 (mol/L)
    cLogP: 계산된 LogP
    MW: 분자량
    RB: 회전 결합 수
    AP: 방향족 비율
    """
    mol = Chem.MolFromSmiles(smiles)

    logp = Descriptors.MolLogP(mol)
    mw = Descriptors.MolWt(mol)
    rb = Descriptors.NumRotatableBonds(mol)

    # 방향족 비율
    n_aromatic = sum(1 for a in mol.GetAtoms() if a.GetIsAromatic())
    n_heavy = mol.GetNumHeavyAtoms()
    ap = n_aromatic / n_heavy if n_heavy > 0 else 0

    # ESOL 방정식
    log_s = 0.16 - 0.63 * logp - 0.0062 * mw + 0.066 * rb - 0.74 * ap

    # mol/L to mg/mL
    s_mol_l = 10 ** log_s
    s_mg_ml = s_mol_l * mw / 1000

    # 분류 (USP 기준 근사)
    if s_mg_ml >= 100:
        category = "Freely soluble"
    elif s_mg_ml >= 33:
        category = "Soluble"
    elif s_mg_ml >= 10:
        category = "Sparingly soluble"
    elif s_mg_ml >= 1:
        category = "Slightly soluble"
    elif s_mg_ml >= 0.1:
        category = "Very slightly soluble"
    else:
        category = "Practically insoluble"

    return {
        "log_s_mol_l": round(log_s, 2),
        "solubility_mol_l": f"{s_mol_l:.2e}",
        "solubility_mg_ml": round(s_mg_ml, 3),
        "solubility_category": category,
        "parameters": {
            "logp": round(logp, 2),
            "mw": round(mw, 2),
            "rotatable_bonds": rb,
            "aromatic_proportion": round(ap, 2)
        }
    }
```

### 오일 용해도 추정

```python
def estimate_oil_solubility(smiles: str) -> dict:
    """
    LogP 기반 오일 용해도 추정

    LogP > 2: 오일 용해성 양호
    LogP < 0: 오일 용해성 불량
    """
    mol = Chem.MolFromSmiles(smiles)

    logp = Descriptors.MolLogP(mol)

    # 오일 용해도 추정
    if logp >= 4:
        oil_solubility = "Excellent"
        recommended_phase = "Oil phase"
    elif logp >= 2:
        oil_solubility = "Good"
        recommended_phase = "Oil phase or co-solvent"
    elif logp >= 0:
        oil_solubility = "Limited"
        recommended_phase = "Co-solvent needed"
    else:
        oil_solubility = "Poor"
        recommended_phase = "Water phase"

    return {
        "logp": round(logp, 2),
        "oil_solubility": oil_solubility,
        "recommended_phase": recommended_phase
    }
```

---

## 4. UV 필터 특성 분석

### UV 흡수 예측

```python
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

def analyze_uv_filter(smiles: str) -> dict:
    """
    UV 필터 후보 물질의 특성 분석

    UV 흡수는 공액계(conjugated system)와 발색단(chromophore)에 의존
    """
    mol = Chem.MolFromSmiles(smiles)

    # 방향족 고리 수
    n_aromatic_rings = rdMolDescriptors.CalcNumAromaticRings(mol)

    # 공액 이중결합 (근사)
    # C=C-C=C 패턴 검색
    conjugated_pattern = Chem.MolFromSmarts("C=C-C=C")
    n_conjugated = len(mol.GetSubstructMatches(conjugated_pattern)) if conjugated_pattern else 0

    # 카르보닐 공액
    carbonyl_conj = Chem.MolFromSmarts("C=C-C(=O)")
    n_carbonyl_conj = len(mol.GetSubstructMatches(carbonyl_conj)) if carbonyl_conj else 0

    # UV 흡수 예측
    has_uv_absorption = n_aromatic_rings > 0 or n_conjugated > 0 or n_carbonyl_conj > 0

    # 대략적인 흡수 영역 추정
    if n_aromatic_rings >= 2 or (n_aromatic_rings >= 1 and n_carbonyl_conj >= 1):
        predicted_absorption = "UVA (320-400nm)"
    elif n_aromatic_rings >= 1 or n_conjugated >= 2:
        predicted_absorption = "UVB (280-320nm)"
    elif n_conjugated >= 1:
        predicted_absorption = "UVC-UVB (200-320nm)"
    else:
        predicted_absorption = "Minimal UV absorption"

    # 물리화학적 특성
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)

    return {
        "has_uv_absorption": has_uv_absorption,
        "predicted_absorption_range": predicted_absorption,
        "chromophore_analysis": {
            "aromatic_rings": n_aromatic_rings,
            "conjugated_systems": n_conjugated,
            "carbonyl_conjugation": n_carbonyl_conj
        },
        "physicochemical": {
            "mw": round(mw, 2),
            "logp": round(logp, 2)
        },
        "note": "실제 UV 흡수는 실험적 측정 필요"
    }
```

---

## 5. 원료 호환성 예측

### 산화 민감성 분석

```python
def analyze_oxidation_sensitivity(smiles: str) -> dict:
    """
    분자 구조 기반 산화 민감성 평가

    산화에 취약한 구조:
    - 이중결합 (특히 공액)
    - 페놀기
    - 티올기
    - 알데히드기
    """
    mol = Chem.MolFromSmiles(smiles)

    # 민감 구조 패턴
    sensitive_patterns = {
        "unsaturated": ("C=C", 2),  # 이중결합, 민감도 점수
        "phenol": ("c1ccccc1O", 3),  # 페놀
        "thiol": ("[SH]", 4),  # 티올
        "aldehyde": ("[CH]=O", 3),  # 알데히드
        "polyunsaturated": ("C=CC=C", 4),  # 공액 이중결합
        "benzyl": ("c1ccccc1C", 1),  # 벤질 위치
    }

    findings = {}
    total_score = 0

    for name, (smarts, score) in sensitive_patterns.items():
        pattern = Chem.MolFromSmarts(smarts)
        if pattern:
            matches = mol.GetSubstructMatches(pattern)
            count = len(matches)
            if count > 0:
                findings[name] = {
                    "count": count,
                    "risk_contribution": count * score
                }
                total_score += count * score

    # 분류
    if total_score == 0:
        sensitivity = "Low"
        recommendation = "Standard storage conditions"
    elif total_score < 5:
        sensitivity = "Moderate"
        recommendation = "Protect from light and heat"
    elif total_score < 10:
        sensitivity = "High"
        recommendation = "Add antioxidants, N2 blanket, light-protected packaging"
    else:
        sensitivity = "Very High"
        recommendation = "Requires strong antioxidant system, cold storage"

    return {
        "oxidation_sensitivity": sensitivity,
        "risk_score": total_score,
        "sensitive_structures": findings,
        "recommendation": recommendation
    }
```

### pH 민감성 분석

```python
def analyze_ph_sensitivity(smiles: str) -> dict:
    """
    pH 민감 구조 분석

    pH에 민감한 구조:
    - 에스테르 (가수분해)
    - 아미드 (느린 가수분해)
    - 락톤 (고리 에스테르)
    - 글리코사이드 (당 결합)
    """
    mol = Chem.MolFromSmiles(smiles)

    sensitive_patterns = {
        "ester": {
            "smarts": "C(=O)O[C]",
            "ph_range": "Stable pH 4-7, hydrolysis at extremes",
            "risk": "Medium"
        },
        "amide": {
            "smarts": "C(=O)N",
            "ph_range": "Stable pH 4-8, slow hydrolysis",
            "risk": "Low"
        },
        "lactone": {
            "smarts": "[C]1[C][O]C(=O)[C]1",  # 단순화된 패턴
            "ph_range": "Sensitive to base, ring opening",
            "risk": "High"
        },
        "imine": {
            "smarts": "C=N",
            "ph_range": "Hydrolysis in acidic conditions",
            "risk": "Medium"
        },
        "carboxylic_acid": {
            "smarts": "C(=O)O",
            "ph_range": "pKa ~4-5, ionization affects solubility",
            "risk": "Low"
        },
        "amine": {
            "smarts": "[NH2,NH,N]",
            "ph_range": "pKa varies, protonation affects activity",
            "risk": "Low"
        }
    }

    findings = {}

    for name, info in sensitive_patterns.items():
        pattern = Chem.MolFromSmarts(info["smarts"])
        if pattern:
            matches = mol.GetSubstructMatches(pattern)
            if len(matches) > 0:
                findings[name] = {
                    "count": len(matches),
                    "ph_behavior": info["ph_range"],
                    "stability_risk": info["risk"]
                }

    # 전체 평가
    if not findings:
        overall = "Low pH sensitivity"
        optimal_ph = "Wide range (3-9)"
    elif any(f.get("stability_risk") == "High" for f in findings.values()):
        overall = "High pH sensitivity"
        optimal_ph = "Narrow range, formulation dependent"
    else:
        overall = "Moderate pH sensitivity"
        optimal_ph = "pH 4-7 recommended"

    return {
        "ph_sensitivity": overall,
        "optimal_ph_range": optimal_ph,
        "sensitive_groups": findings
    }
```

---

## 6. 분자 유사성 기반 원료 검색

### Tanimoto 유사성

```python
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs

def find_similar_molecules(query_smiles: str, database: list,
                            min_similarity: float = 0.5) -> list:
    """
    분자 지문(Fingerprint) 기반 유사 분자 검색

    Args:
        query_smiles: 검색 기준 분자
        database: [{"name": str, "smiles": str, "function": str}, ...]
        min_similarity: 최소 유사도 (0-1)

    Returns:
        유사 분자 리스트 (유사도 순)
    """
    query_mol = Chem.MolFromSmiles(query_smiles)
    if query_mol is None:
        return []

    # Morgan Fingerprint (ECFP4 유사)
    query_fp = AllChem.GetMorganFingerprintAsBitVect(query_mol, 2, nBits=2048)

    results = []

    for item in database:
        mol = Chem.MolFromSmiles(item.get("smiles", ""))
        if mol:
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
            similarity = DataStructs.TanimotoSimilarity(query_fp, fp)

            if similarity >= min_similarity:
                results.append({
                    "name": item.get("name"),
                    "smiles": item.get("smiles"),
                    "function": item.get("function"),
                    "similarity": round(similarity, 3)
                })

    # 유사도 순 정렬
    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results

# 사용 예시: Niacinamide와 유사한 원료 검색
COSMETIC_DB = [
    {"name": "Niacinamide", "smiles": "NC(=O)c1cccnc1", "function": "Brightening"},
    {"name": "Nicotinic Acid", "smiles": "OC(=O)c1cccnc1", "function": "Vasodilation"},
    {"name": "Picolinic Acid", "smiles": "OC(=O)c1ccccn1", "function": "Chelating"},
    {"name": "Pyridoxine", "smiles": "Cc1ncc(CO)c(CO)c1O", "function": "Vitamin B6"},
    {"name": "Caffeine", "smiles": "Cn1cnc2c1c(=O)n(c(=O)n2C)C", "function": "Anti-cellulite"},
]

similar = find_similar_molecules("NC(=O)c1cccnc1", COSMETIC_DB, 0.3)
```

---

## 7. 활성 성분 스크리닝

### 미백 성분 후보 스크리닝

```python
def screen_brightening_candidates(smiles_list: list) -> list:
    """
    미백 활성 후보 스크리닝

    미백 메커니즘 관련 구조적 특징:
    - 페놀기 (tyrosinase 기질 유사성)
    - 카르복실기 (킬레이팅 능력)
    - 방향족 고리
    """
    candidates = []

    for item in smiles_list:
        smiles = item.get("smiles")
        name = item.get("name", "Unknown")

        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            continue

        # 구조적 특징 분석
        phenol = mol.GetSubstructMatches(Chem.MolFromSmarts("c1ccccc1O"))
        carboxylic = mol.GetSubstructMatches(Chem.MolFromSmarts("C(=O)O"))
        aromatic = sum(1 for a in mol.GetAtoms() if a.GetIsAromatic())

        # 물리화학적 특성
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        psa = Descriptors.TPSA(mol)

        # 스코어 계산
        score = 0
        reasons = []

        # 페놀 구조 (tyrosinase 상호작용)
        if len(phenol) > 0:
            score += 3
            reasons.append("Phenol structure (tyrosinase interaction)")

        # 카르복실기 (금속 킬레이팅)
        if len(carboxylic) > 0:
            score += 2
            reasons.append("Carboxylic acid (chelating potential)")

        # 방향족 (UV 보호)
        if aromatic > 0:
            score += 1
            reasons.append("Aromatic system")

        # MW 페널티
        if mw > 500:
            score -= 1
            reasons.append("High MW (penetration concern)")

        # LogP 체크
        if 0 <= logp <= 3:
            score += 1
            reasons.append("Favorable LogP for penetration")

        candidates.append({
            "name": name,
            "smiles": smiles,
            "brightening_score": score,
            "reasons": reasons,
            "properties": {
                "mw": round(mw, 2),
                "logp": round(logp, 2),
                "psa": round(psa, 2)
            }
        })

    # 스코어 순 정렬
    candidates.sort(key=lambda x: x["brightening_score"], reverse=True)

    return candidates
```

---

## 8. 배치 분석 및 보고서 생성

### 전체 원료 분석 보고서

```python
def generate_ingredient_report(smiles: str, name: str = None) -> str:
    """
    화장품 원료 종합 분석 보고서 생성 (Markdown 형식)
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return f"# Error\nInvalid SMILES: {smiles}"

    # 기본 정보
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    psa = Descriptors.TPSA(mol)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)
    rotatable = Descriptors.NumRotatableBonds(mol)
    formula = rdMolDescriptors.CalcMolFormula(mol)

    # Lipinski
    lipinski_violations = sum([
        mw > 500,
        logp > 5,
        hbd > 5,
        hba > 10
    ])

    # 보고서 생성
    report = f"""# Ingredient Analysis Report

## Basic Information
- **Name**: {name or 'Unknown'}
- **SMILES**: `{smiles}`
- **Molecular Formula**: {formula}

## Molecular Properties

| Property | Value | Lipinski Limit | Status |
|----------|-------|----------------|--------|
| Molecular Weight | {mw:.2f} Da | ≤ 500 | {'PASS' if mw <= 500 else 'FAIL'} |
| LogP | {logp:.2f} | ≤ 5 | {'PASS' if logp <= 5 else 'FAIL'} |
| H-Bond Donors | {hbd} | ≤ 5 | {'PASS' if hbd <= 5 else 'FAIL'} |
| H-Bond Acceptors | {hba} | ≤ 10 | {'PASS' if hba <= 10 else 'FAIL'} |
| PSA | {psa:.2f} Å² | ≤ 140 | {'PASS' if psa <= 140 else 'FAIL'} |
| Rotatable Bonds | {rotatable} | ≤ 10 | {'PASS' if rotatable <= 10 else 'FAIL'} |

## Lipinski Rule of Five
- **Violations**: {lipinski_violations}
- **Assessment**: {'PASS' if lipinski_violations <= 1 else 'FAIL'}

## Skin Penetration Assessment
- **LogP Range**: {'Optimal (1-3)' if 1 <= logp <= 3 else 'Suboptimal'}
- **MW Assessment**: {'Good (<500 Da)' if mw < 500 else 'Limited (>500 Da)'}
- **Overall**: {'Good penetration potential' if mw < 500 and 1 <= logp <= 3 else 'May require penetration enhancement'}

## Solubility Prediction
- **Water Solubility**: {'Good' if logp < 1 else 'Limited' if logp < 3 else 'Poor'}
- **Oil Solubility**: {'Poor' if logp < 0 else 'Limited' if logp < 2 else 'Good'}
- **Recommended Phase**: {'Water' if logp < 0 else 'Co-solvent' if logp < 2 else 'Oil'}

---
*Report generated using RDKit {rdkit.__version__}*
"""

    return report
```

---

## 요약

RDKit을 활용한 화장품 R&D 주요 응용:

1. **피부 침투성 예측**: Potts-Guy equation, 층별 분석
2. **HLB 추정**: Griffin/Davies 방법
3. **용해도 예측**: ESOL, 오일 용해도
4. **UV 필터 분석**: 발색단 분석
5. **호환성 예측**: 산화/pH 민감성
6. **유사 원료 검색**: 분자 지문 기반
7. **활성 스크리닝**: 구조 기반 평가
8. **보고서 생성**: 종합 분석

이 도구들을 조합하여 신규 원료 평가, 제형 최적화, 대량 스크리닝을 효율적으로 수행할 수 있습니다.
