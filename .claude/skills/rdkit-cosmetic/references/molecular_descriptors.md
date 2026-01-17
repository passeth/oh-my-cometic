# Molecular Descriptors for Cosmetics

## 화장품 R&D를 위한 핵심 분자 기술자

분자 기술자(Molecular Descriptor)는 분자 구조로부터 계산되는 수치적 특성입니다. 화장품 원료 평가에서 특히 중요한 기술자들을 상세히 설명합니다.

---

## 1. LogP (Partition Coefficient)

### 정의

LogP는 옥탄올(octanol)과 물(water) 사이의 분배계수의 로그값입니다.

```
LogP = log₁₀ ([solute]_octanol / [solute]_water)

[solute]_octanol = 옥탄올 상의 용질 농도
[solute]_water = 수상의 용질 농도
```

### 화장품에서의 의미

| LogP 범위 | 특성 | 화장품 적용 |
|----------|------|------------|
| < -1 | 매우 친수성 | 수용액 제형, 제한된 피부 침투 |
| -1 ~ 0 | 친수성 | 토너, 에센스 원료 |
| 0 ~ 1 | 약한 친유성 | 양쪽성 원료, 좋은 용해도 |
| **1 ~ 3** | **중간 친유성** | **최적 피부 침투**, 로션/크림 활성성분 |
| 3 ~ 5 | 강한 친유성 | 오일 용해성, 피부 잔류 경향 |
| > 5 | 매우 친유성 | 오일상 용해, 각질층 축적 |

### 피부 침투와의 관계

피부 침투 최적 LogP: **1 ~ 3**

이유:
1. **각질층 통과**: 적당한 친유성 필요 (각질층은 친유성)
2. **생존 표피 이동**: 적당한 친수성 필요 (세포간 수분 환경)
3. **균형**: 너무 친유성 → 각질층 잔류, 너무 친수성 → 각질층 투과 불가

```
피부 구조와 LogP:
┌─────────────────────────────────┐
│  표피 (친유성) - LogP > 1 필요   │
├─────────────────────────────────┤
│  생존 표피 - 친수/친유 균형 필요  │
├─────────────────────────────────┤
│  진피 (친수성) - LogP < 4 선호   │
└─────────────────────────────────┘
```

### RDKit에서의 계산

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

def calculate_logp(smiles: str) -> dict:
    """
    LogP 계산 및 해석

    RDKit은 Wildman-Crippen 방법 사용:
    - 원자 기여도 기반 계산
    - 실험값과 높은 상관관계 (R² > 0.9)
    """
    mol = Chem.MolFromSmiles(smiles)

    logp = Descriptors.MolLogP(mol)

    # 해석
    if logp < 0:
        character = "hydrophilic"
        penetration = "limited"
    elif 0 <= logp < 1:
        character = "slightly lipophilic"
        penetration = "moderate"
    elif 1 <= logp <= 3:
        character = "moderately lipophilic"
        penetration = "optimal"
    elif 3 < logp <= 5:
        character = "lipophilic"
        penetration = "may accumulate in stratum corneum"
    else:
        character = "highly lipophilic"
        penetration = "poor, retained in stratum corneum"

    return {
        "logp": round(logp, 2),
        "character": character,
        "skin_penetration_prediction": penetration
    }
```

### 주요 화장품 원료의 LogP

| 원료 | LogP | 특성 |
|------|------|------|
| Glycerin | -1.76 | 매우 친수성, 보습제 |
| Niacinamide | -0.37 | 친수성, 수용성 활성 |
| Salicylic Acid | 2.24 | 중간, 좋은 침투 |
| Retinol | 6.30 | 매우 친유성, 오일 용해 |
| Tocopherol | 10.7 | 극도 친유성, 오일상 |
| Caffeine | -0.07 | 중성, 양호한 용해도 |
| Alpha-Arbutin | -1.49 | 친수성, 수용성 미백 |

---

## 2. Molecular Weight (분자량)

### 정의

분자를 구성하는 모든 원자의 원자량 합계 (단위: Da 또는 g/mol)

```
MW = Σ (각 원자의 원자량 × 개수)
```

### 화장품에서의 의미 (500 Da 규칙)

**Lipinski Rule**: 분자량 500 Da 이하가 경구 흡수에 유리

**Bos & Meinardi Rule** (피부): 분자량 500 Da 이하가 피부 침투에 유리

| MW 범위 | 피부 침투 | 예시 원료 |
|---------|----------|-----------|
| < 150 Da | 우수하나 휘발 가능 | Ethanol (46), Water (18) |
| 150-300 Da | 최적 침투 | Salicylic Acid (138), Niacinamide (122) |
| 300-500 Da | 양호한 침투 | Retinol (286), Avobenzone (310) |
| 500-1000 Da | 제한적 침투 | Hyaluronic acid monomer |
| > 1000 Da | 피부 표면 잔류 | Hyaluronic acid polymer |

### 피부 침투 메커니즘

```
분자량과 경피 흡수:

큰 분자 (>500 Da)
    ↓
각질층의 세포간 지질 경로 통과 어려움
    ↓
표면 잔류 (보습, 피막 형성)


작은 분자 (<500 Da)
    ↓
세포간 지질 경로 또는 모낭 경로 통과
    ↓
표피/진피 도달 (활성 효과)
```

### RDKit에서의 계산

```python
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

def calculate_mw(smiles: str) -> dict:
    """
    분자량 계산 및 분류
    """
    mol = Chem.MolFromSmiles(smiles)

    # 평균 분자량 (자연 동위원소 분포 고려)
    mw = Descriptors.MolWt(mol)

    # 정확 분자량 (단일 동위원소)
    exact_mw = Descriptors.ExactMolWt(mol)

    # 분자식
    formula = rdMolDescriptors.CalcMolFormula(mol)

    # 분류
    if mw < 150:
        category = "Very small"
        penetration = "Excellent but may evaporate"
    elif mw < 300:
        category = "Small"
        penetration = "Optimal for skin penetration"
    elif mw < 500:
        category = "Medium"
        penetration = "Good penetration potential"
    elif mw < 1000:
        category = "Large"
        penetration = "Limited penetration"
    else:
        category = "Very large"
        penetration = "Surface activity only"

    return {
        "molecular_weight": round(mw, 2),
        "exact_mass": round(exact_mw, 4),
        "formula": formula,
        "category": category,
        "penetration_assessment": penetration
    }
```

---

## 3. PSA (Polar Surface Area)

### 정의

분자 표면 중 극성 원자(N, O 및 연결된 H)가 차지하는 면적

```
PSA = Σ (극성 원자들의 반데르발스 표면적)

단위: Å² (제곱 옹스트롬)
```

### 화장품에서의 의미

PSA는 분자의 전체적인 극성 정도를 나타내며, 막 투과성과 밀접한 관계가 있습니다.

| PSA 범위 | 의미 | 피부 침투 |
|----------|------|----------|
| < 60 Å² | 낮은 극성 | 우수한 침투 |
| 60-90 Å² | 중간 극성 | 양호한 침투 |
| 90-140 Å² | 높은 극성 | 보통 침투 |
| > 140 Å² | 매우 높은 극성 | 제한적 침투 |

### 구조적 해석

```
PSA 기여 원자:
- 산소 (O): ~9-15 Å² per atom
- 질소 (N): ~12-26 Å² per atom
- OH 기: ~20 Å²
- NH2 기: ~26 Å²
- C=O 기: ~17 Å²

예시:
Glycerin: C3H8O3
- 3개 OH 기 ≈ 60 Å²

Niacinamide: C6H6N2O
- 1개 C=O, 1개 NH2, 1개 N ≈ 56 Å²
```

### RDKit에서의 계산

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

def calculate_psa(smiles: str) -> dict:
    """
    위상적 극성 표면적(TPSA) 계산

    RDKit은 Ertl 방법 사용:
    - 원자 기여도 기반 계산
    - 빠르고 정확함 (3D 계산 불필요)
    """
    mol = Chem.MolFromSmiles(smiles)

    # TPSA (Topological PSA)
    tpsa = Descriptors.TPSA(mol)

    # 극성 원자 분석
    n_oxygen = sum(1 for a in mol.GetAtoms() if a.GetSymbol() == 'O')
    n_nitrogen = sum(1 for a in mol.GetAtoms() if a.GetSymbol() == 'N')

    # 분류
    if tpsa < 60:
        category = "Low polarity"
        membrane_permeability = "High"
    elif tpsa < 90:
        category = "Moderate polarity"
        membrane_permeability = "Good"
    elif tpsa < 140:
        category = "High polarity"
        membrane_permeability = "Moderate"
    else:
        category = "Very high polarity"
        membrane_permeability = "Low"

    return {
        "tpsa": round(tpsa, 2),
        "unit": "Å²",
        "oxygen_atoms": n_oxygen,
        "nitrogen_atoms": n_nitrogen,
        "polarity_category": category,
        "membrane_permeability": membrane_permeability
    }
```

---

## 4. HBD & HBA (Hydrogen Bond Donors/Acceptors)

### 정의

- **HBD (Hydrogen Bond Donors)**: 수소 결합을 제공할 수 있는 원자 (주로 OH, NH)
- **HBA (Hydrogen Bond Acceptors)**: 수소 결합을 받을 수 있는 원자 (주로 O, N)

```
HBD: -OH, -NH2, -NH-, =NH
HBA: =O, -O-, -N=, -N<
```

### Lipinski 기준

```
Rule of Five 중 수소결합 관련:
- HBD ≤ 5
- HBA ≤ 10

위반 시: 경구 흡수율 감소, 피부 침투성 감소
```

### 화장품에서의 의미

수소 결합 능력은 용해도와 막 투과성에 영향:

| 특성 | 높은 HBD/HBA | 낮은 HBD/HBA |
|------|-------------|-------------|
| 수용성 | 높음 | 낮음 |
| 피부 침투 | 제한적 | 양호 |
| 보습 효과 | 강함 | 약함 |
| 단백질 결합 | 강함 | 약함 |

### 보습제와 HBD/HBA

```
보습제의 수소결합과 물 결합능:

Glycerin (3 OH): HBD=3, HBA=3
- 물 분자 3개 결합 가능
- 뛰어난 보습 효과

Hyaluronic Acid (다수 OH, COOH, NHCOCH3):
- 분자당 1000개 이상의 물 분자 결합
- 최고의 보습 효과
```

### RDKit에서의 계산

```python
from rdkit import Chem
from rdkit.Chem import Lipinski, Descriptors

def calculate_hbond(smiles: str) -> dict:
    """
    수소결합 공여/수용체 분석
    """
    mol = Chem.MolFromSmiles(smiles)

    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)

    # 총 수소결합 능력
    total_hb = hbd + hba

    # 분석
    analysis = {
        "hbd": hbd,
        "hba": hba,
        "total_hbond_capacity": total_hb,
        "lipinski_hbd_pass": hbd <= 5,
        "lipinski_hba_pass": hba <= 10
    }

    # 특성 예측
    if total_hb <= 5:
        analysis["water_solubility"] = "Low"
        analysis["skin_penetration"] = "Good"
    elif total_hb <= 10:
        analysis["water_solubility"] = "Moderate"
        analysis["skin_penetration"] = "Moderate"
    else:
        analysis["water_solubility"] = "High"
        analysis["skin_penetration"] = "Limited"

    # 보습제 특성
    if hbd >= 3:
        analysis["humectant_potential"] = "Good"
    else:
        analysis["humectant_potential"] = "Limited"

    return analysis
```

---

## 5. 회전 결합 (Rotatable Bonds)

### 정의

자유롭게 회전할 수 있는 단일 결합의 수

```
회전 결합 조건:
- 단일 결합
- 비말단 (터미널 아님)
- 고리의 일부가 아님
- 아마이드 결합 제외 (부분 이중결합 특성)
```

### 화장품에서의 의미

분자의 유연성과 관련되어 막 투과 및 수용체 결합에 영향:

| 회전 결합 수 | 분자 특성 | 의미 |
|------------|----------|------|
| 0-2 | 강직 | 안정적, 특정 구조 유지 |
| 3-5 | 적당한 유연성 | 막 투과 최적 |
| 6-10 | 유연 | 다양한 배좌 가능 |
| >10 | 매우 유연 | 엔트로피 불리, 결합 감소 |

### Veber 규칙

경구 생체이용률 예측 (피부에도 참고 가능):

```
Veber 기준:
- 회전 결합 ≤ 10
- PSA ≤ 140 Å² (또는 HBD+HBA ≤ 12)

→ 두 조건 충족 시 좋은 생체이용률
```

### RDKit에서의 계산

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

def count_rotatable_bonds(smiles: str) -> dict:
    """
    회전 결합 수 계산 및 분석
    """
    mol = Chem.MolFromSmiles(smiles)

    n_rot = Descriptors.NumRotatableBonds(mol)

    # 분자 유연성 평가
    if n_rot <= 2:
        flexibility = "Rigid"
    elif n_rot <= 5:
        flexibility = "Semi-flexible"
    elif n_rot <= 10:
        flexibility = "Flexible"
    else:
        flexibility = "Highly flexible"

    # Veber 규칙 확인
    psa = Descriptors.TPSA(mol)
    veber_rotatable = n_rot <= 10
    veber_psa = psa <= 140

    return {
        "rotatable_bonds": n_rot,
        "flexibility": flexibility,
        "veber_rule": {
            "rotatable_pass": veber_rotatable,
            "psa_pass": veber_psa,
            "overall_pass": veber_rotatable and veber_psa
        }
    }
```

---

## 6. 복합 지표: 피부 침투 예측 스코어

여러 기술자를 조합한 피부 침투 예측 모델:

```python
def calculate_skin_penetration_score(smiles: str) -> dict:
    """
    통합 피부 침투 예측 스코어

    기반 모델:
    - Potts-Guy equation (기본)
    - Modified for cosmetic applications
    """
    mol = Chem.MolFromSmiles(smiles)

    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    psa = Descriptors.TPSA(mol)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)
    rotatable = Descriptors.NumRotatableBonds(mol)

    # 점수 계산 (100점 만점)
    score = 100

    # MW 페널티 (500 초과 시)
    if mw > 500:
        score -= min(30, (mw - 500) / 20)

    # LogP 보정 (최적 1-3)
    if logp < 0:
        score -= 15 * abs(logp)
    elif logp > 5:
        score -= 10 * (logp - 5)
    elif 1 <= logp <= 3:
        score += 10  # 보너스

    # PSA 페널티 (140 초과 시)
    if psa > 140:
        score -= (psa - 140) / 5

    # HBD 페널티 (5 초과 시)
    if hbd > 5:
        score -= 5 * (hbd - 5)

    # HBA 페널티 (10 초과 시)
    if hba > 10:
        score -= 3 * (hba - 10)

    # 회전 결합 페널티 (10 초과 시)
    if rotatable > 10:
        score -= 3 * (rotatable - 10)

    score = max(0, min(100, score))

    # 분류
    if score >= 80:
        classification = "Excellent"
        recommendation = "High penetration potential, suitable for active delivery"
    elif score >= 60:
        classification = "Good"
        recommendation = "Moderate penetration, effective for most applications"
    elif score >= 40:
        classification = "Fair"
        recommendation = "Limited penetration, may need enhancement"
    else:
        classification = "Poor"
        recommendation = "Surface activity, not suitable for deep delivery"

    return {
        "penetration_score": round(score, 1),
        "classification": classification,
        "recommendation": recommendation,
        "parameters_used": {
            "mw": round(mw, 2),
            "logp": round(logp, 2),
            "psa": round(psa, 2),
            "hbd": hbd,
            "hba": hba,
            "rotatable_bonds": rotatable
        }
    }
```

---

## 7. 화장품 원료별 기술자 참조표

| 원료 | MW (Da) | LogP | PSA (Å²) | HBD | HBA | 침투 예측 |
|------|---------|------|----------|-----|-----|----------|
| Niacinamide | 122.1 | -0.37 | 56.0 | 1 | 2 | Excellent |
| Salicylic Acid | 138.1 | 2.24 | 57.5 | 2 | 3 | Excellent |
| Glycolic Acid | 76.1 | -0.93 | 57.5 | 2 | 3 | Good |
| Retinol | 286.5 | 6.30 | 20.2 | 1 | 1 | Moderate* |
| Caffeine | 194.2 | -0.07 | 58.4 | 0 | 6 | Good |
| Alpha-Arbutin | 272.3 | -1.49 | 119.6 | 5 | 7 | Fair |
| Ascorbic Acid | 176.1 | -1.85 | 107.2 | 4 | 6 | Fair |
| Hyaluronic Acid (monomer) | 401.3 | -3.5 | 186.5 | 7 | 12 | Poor |
| Tocopherol | 430.7 | 10.7 | 29.5 | 1 | 2 | Poor* |

*Retinol: LogP 높아 각질층 잔류 경향
*Tocopherol: LogP 극히 높아 피부 장벽 통과 제한

---

## 요약

화장품 원료 평가에 핵심적인 분자 기술자:

1. **LogP**: 친유성/친수성 균형, 최적 1-3
2. **MW**: 분자 크기, 500 Da 이하 권장
3. **PSA**: 극성 정도, 140 Å² 이하 선호
4. **HBD/HBA**: 수소결합 능력, 적을수록 침투 유리
5. **Rotatable Bonds**: 분자 유연성, 10 이하 권장

이들 기술자의 조합으로 피부 침투성을 예측하고, 제형 설계 및 원료 선정에 활용하세요.
