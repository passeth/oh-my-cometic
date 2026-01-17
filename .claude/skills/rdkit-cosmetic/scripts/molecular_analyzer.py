#!/usr/bin/env python3
"""
Molecular Analyzer for Cosmetic Ingredients

화장품 원료의 분자 수준 분석 도구
- 분자량, LogP, PSA, HBD/HBA 계산
- Lipinski Rule of Five 검증
- 피부 침투성 예측
- HLB 추정

Author: EVAS Cosmetic
License: MIT
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, Lipinski, rdMolDescriptors
    from rdkit.Chem import AllChem, DataStructs
except ImportError:
    print("Error: RDKit is not installed.")
    print("Install with: conda install -c conda-forge rdkit")
    print("Or: pip install rdkit")
    sys.exit(1)


@dataclass
class MolecularProperties:
    """분자 특성 데이터 클래스"""
    smiles: str
    canonical_smiles: str
    formula: str
    molecular_weight: float
    logp: float
    tpsa: float
    hbd: int  # H-bond donors
    hba: int  # H-bond acceptors
    rotatable_bonds: int
    heavy_atoms: int
    aromatic_rings: int


@dataclass
class LipinskiAnalysis:
    """Lipinski 분석 결과"""
    mw_pass: bool
    logp_pass: bool
    hbd_pass: bool
    hba_pass: bool
    violations: int
    overall_pass: bool


@dataclass
class SkinPenetrationPrediction:
    """피부 침투성 예측 결과"""
    score: float  # 0-100
    classification: str
    log_kp: float  # Potts-Guy
    factors: Dict


# =============================================================================
# 화장품 원료 SMILES 데이터베이스
# =============================================================================

COSMETIC_INGREDIENTS = {
    # 활성 성분
    "niacinamide": {
        "inci": "Niacinamide",
        "smiles": "NC(=O)c1cccnc1",
        "cas": "98-92-0",
        "function": "Skin conditioning, Brightening"
    },
    "retinol": {
        "inci": "Retinol",
        "smiles": "CC1=C(C(CCC1)(C)C)/C=C/C(=C/C=C/C(=C/CO)/C)/C",
        "cas": "68-26-8",
        "function": "Anti-aging"
    },
    "salicylic_acid": {
        "inci": "Salicylic Acid",
        "smiles": "OC(=O)c1ccccc1O",
        "cas": "69-72-7",
        "function": "Keratolytic, BHA"
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
    "ascorbic_acid": {
        "inci": "Ascorbic Acid",
        "smiles": "C([C@@H]([C@@H]1C(=C(C(=O)O1)O)O)O)O",
        "cas": "50-81-7",
        "function": "Antioxidant, Brightening"
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
    "caffeine": {
        "inci": "Caffeine",
        "smiles": "Cn1cnc2c1c(=O)n(c(=O)n2C)C",
        "cas": "58-08-2",
        "function": "Anti-cellulite, Eye care"
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
    "urea": {
        "inci": "Urea",
        "smiles": "NC(N)=O",
        "cas": "57-13-6",
        "function": "Humectant, Keratolytic"
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

    # 항산화제
    "tocopherol": {
        "inci": "Tocopherol",
        "smiles": "CC(C)CCCC(C)CCCC(C)CCCC1(C)CCc2c(C)c(O)c(C)c(C)c2O1",
        "cas": "59-02-9",
        "function": "Antioxidant"
    },
}


# =============================================================================
# 핵심 분석 함수
# =============================================================================

def validate_smiles(smiles: str) -> bool:
    """SMILES 유효성 검증"""
    mol = Chem.MolFromSmiles(smiles)
    return mol is not None


def canonicalize_smiles(smiles: str) -> str:
    """표준 SMILES로 변환"""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    return Chem.MolToSmiles(mol, canonical=True)


def calculate_molecular_properties(smiles: str) -> MolecularProperties:
    """
    분자 특성 계산

    Args:
        smiles: SMILES 문자열

    Returns:
        MolecularProperties 객체
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")

    return MolecularProperties(
        smiles=smiles,
        canonical_smiles=Chem.MolToSmiles(mol, canonical=True),
        formula=rdMolDescriptors.CalcMolFormula(mol),
        molecular_weight=round(Descriptors.MolWt(mol), 2),
        logp=round(Descriptors.MolLogP(mol), 2),
        tpsa=round(Descriptors.TPSA(mol), 2),
        hbd=Lipinski.NumHDonors(mol),
        hba=Lipinski.NumHAcceptors(mol),
        rotatable_bonds=Descriptors.NumRotatableBonds(mol),
        heavy_atoms=Lipinski.HeavyAtomCount(mol),
        aromatic_rings=rdMolDescriptors.CalcNumAromaticRings(mol)
    )


def check_lipinski(smiles: str) -> LipinskiAnalysis:
    """
    Lipinski Rule of Five 검증

    규칙:
    - MW ≤ 500 Da
    - LogP ≤ 5
    - HBD ≤ 5
    - HBA ≤ 10

    Returns:
        LipinskiAnalysis 객체
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")

    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)

    mw_pass = mw <= 500
    logp_pass = logp <= 5
    hbd_pass = hbd <= 5
    hba_pass = hba <= 10

    violations = sum([not mw_pass, not logp_pass, not hbd_pass, not hba_pass])

    return LipinskiAnalysis(
        mw_pass=mw_pass,
        logp_pass=logp_pass,
        hbd_pass=hbd_pass,
        hba_pass=hba_pass,
        violations=violations,
        overall_pass=violations <= 1
    )


def predict_skin_penetration(smiles: str) -> SkinPenetrationPrediction:
    """
    피부 침투성 예측

    Potts-Guy equation + 추가 보정:
    log Kp = 0.71 × LogP - 0.0061 × MW - 2.72

    Returns:
        SkinPenetrationPrediction 객체
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")

    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    psa = Descriptors.TPSA(mol)
    hbd = Lipinski.NumHDonors(mol)

    # Potts-Guy equation
    log_kp = 0.71 * logp - 0.0061 * mw - 2.72

    # 침투 점수 계산 (0-100)
    score = 100

    # MW 패널티
    if mw > 500:
        score -= min(40, (mw - 500) / 10)
    elif mw < 100:
        score -= 10  # 너무 작으면 휘발 가능

    # LogP 최적화 (1-3 최적)
    if 1 <= logp <= 3:
        score += 10
    elif logp < 0:
        score -= 15 * abs(logp)
    elif logp > 5:
        score -= 10 * (logp - 5)

    # PSA 패널티
    if psa > 140:
        score -= (psa - 140) / 5

    # HBD 패널티
    if hbd > 5:
        score -= 5 * (hbd - 5)

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

    return SkinPenetrationPrediction(
        score=round(score, 1),
        classification=classification,
        log_kp=round(log_kp, 2),
        factors={
            "mw": round(mw, 2),
            "logp": round(logp, 2),
            "psa": round(psa, 2),
            "hbd": hbd
        }
    )


def estimate_hlb(smiles: str) -> Dict:
    """
    분자 구조 기반 HLB 추정

    Griffin 방법 + Davies 방법 근사

    Returns:
        HLB 추정 결과 딕셔너리
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")

    mw = Descriptors.MolWt(mol)

    # 친수성 원자 기여 (Griffin 근사)
    hydrophilic_mw = 0
    for atom in mol.GetAtoms():
        symbol = atom.GetSymbol()
        if symbol == 'O':
            hydrophilic_mw += 16
            hydrophilic_mw += atom.GetTotalNumHs()
        elif symbol == 'N':
            hydrophilic_mw += 14
            hydrophilic_mw += atom.GetTotalNumHs()

    hlb_griffin = 20 * (hydrophilic_mw / mw) if mw > 0 else 0

    # Davies 방법 근사
    n_oh = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[OX2H]')))
    n_ether = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[OD2]([#6])[#6]')))
    n_cooh = len(mol.GetSubstructMatches(Chem.MolFromSmarts('C(=O)[OH]')))
    n_carbons = sum(1 for a in mol.GetAtoms() if a.GetSymbol() == 'C')

    hydrophilic_sum = n_oh * 1.9 + n_ether * 1.3 + n_cooh * 2.1
    lipophilic_sum = n_carbons * 0.475

    hlb_davies = 7 + hydrophilic_sum - lipophilic_sum

    # 평균
    hlb_avg = (hlb_griffin + hlb_davies) / 2

    # 범위 제한
    hlb_griffin = max(0, min(20, hlb_griffin))
    hlb_davies = max(0, min(20, hlb_davies))
    hlb_avg = max(0, min(20, hlb_avg))

    # 분류
    if hlb_avg < 4:
        classification = "W/O emulsifier"
    elif hlb_avg < 8:
        classification = "Wetting agent"
    elif hlb_avg < 12:
        classification = "O/W emulsifier"
    elif hlb_avg < 16:
        classification = "Detergent"
    else:
        classification = "Solubilizer"

    return {
        "hlb_griffin": round(hlb_griffin, 1),
        "hlb_davies": round(hlb_davies, 1),
        "hlb_average": round(hlb_avg, 1),
        "classification": classification,
        "structure_info": {
            "oh_groups": n_oh,
            "ether_groups": n_ether,
            "cooh_groups": n_cooh,
            "carbons": n_carbons
        }
    }


def full_analysis(smiles: str, name: str = None) -> Dict:
    """
    종합 분석

    Args:
        smiles: SMILES 문자열
        name: 원료명 (선택)

    Returns:
        종합 분석 결과 딕셔너리
    """
    props = calculate_molecular_properties(smiles)
    lipinski = check_lipinski(smiles)
    penetration = predict_skin_penetration(smiles)
    hlb = estimate_hlb(smiles)

    return {
        "name": name or "Unknown",
        "smiles": smiles,
        "molecular_properties": asdict(props),
        "lipinski_analysis": asdict(lipinski),
        "skin_penetration": asdict(penetration),
        "hlb_estimation": hlb,
        "summary": {
            "formula": props.formula,
            "mw": f"{props.molecular_weight} Da",
            "logp": props.logp,
            "psa": f"{props.tpsa} Å²",
            "lipinski_pass": lipinski.overall_pass,
            "penetration_class": penetration.classification,
            "hlb": hlb["hlb_average"]
        }
    }


def batch_analysis(smiles_list: List[Dict]) -> List[Dict]:
    """
    배치 분석

    Args:
        smiles_list: [{"name": str, "smiles": str}, ...]

    Returns:
        분석 결과 리스트
    """
    results = []

    for item in smiles_list:
        try:
            result = full_analysis(
                smiles=item.get("smiles", ""),
                name=item.get("name", "Unknown")
            )
            result["status"] = "success"
        except Exception as e:
            result = {
                "name": item.get("name", "Unknown"),
                "smiles": item.get("smiles", ""),
                "status": "error",
                "error": str(e)
            }

        results.append(result)

    return results


def find_ingredient(query: str) -> Optional[Dict]:
    """
    내장 데이터베이스에서 원료 검색

    Args:
        query: 검색어 (INCI명 또는 키)

    Returns:
        원료 정보 또는 None
    """
    query_lower = query.lower().replace(" ", "_").replace("-", "_")

    # 직접 키 매칭
    if query_lower in COSMETIC_INGREDIENTS:
        return COSMETIC_INGREDIENTS[query_lower]

    # INCI명 검색
    for key, data in COSMETIC_INGREDIENTS.items():
        if query_lower == data["inci"].lower().replace(" ", "_"):
            return data

    return None


def list_ingredients() -> List[str]:
    """내장 원료 목록 반환"""
    return sorted(COSMETIC_INGREDIENTS.keys())


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Molecular Analyzer for Cosmetic Ingredients",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a SMILES string
  python molecular_analyzer.py --smiles "NC(=O)c1cccnc1" --name "Niacinamide"

  # Analyze from built-in database
  python molecular_analyzer.py --ingredient niacinamide

  # List all available ingredients
  python molecular_analyzer.py --list

  # Batch analyze from JSON file
  python molecular_analyzer.py --batch input.json --output results.json

  # Quick analysis (properties only)
  python molecular_analyzer.py --smiles "C(C(CO)O)O" --quick
        """
    )

    parser.add_argument("--smiles", "-s", help="SMILES string to analyze")
    parser.add_argument("--name", "-n", help="Ingredient name")
    parser.add_argument("--ingredient", "-i", help="Search built-in database")
    parser.add_argument("--list", "-l", action="store_true", help="List all ingredients")
    parser.add_argument("--batch", "-b", help="Batch analyze from JSON file")
    parser.add_argument("--output", "-o", help="Output file (JSON)")
    parser.add_argument("--quick", "-q", action="store_true", help="Quick analysis (properties only)")
    parser.add_argument("--format", "-f", choices=["json", "text"], default="text",
                        help="Output format")

    args = parser.parse_args()

    # 원료 목록 출력
    if args.list:
        print("Available ingredients:")
        print("-" * 40)
        for key in list_ingredients():
            data = COSMETIC_INGREDIENTS[key]
            print(f"  {key}: {data['inci']} ({data['function']})")
        return

    # 내장 DB 검색
    if args.ingredient:
        data = find_ingredient(args.ingredient)
        if data is None:
            print(f"Error: Ingredient '{args.ingredient}' not found")
            print("Use --list to see available ingredients")
            return

        smiles = data["smiles"]
        name = data["inci"]
        print(f"Found: {name} (CAS: {data.get('cas', 'N/A')})")
        print(f"Function: {data['function']}")
        print()
    elif args.smiles:
        smiles = args.smiles
        name = args.name
    elif args.batch:
        # 배치 분석
        with open(args.batch, 'r', encoding='utf-8') as f:
            batch_data = json.load(f)

        results = batch_analysis(batch_data)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        return
    else:
        parser.print_help()
        return

    # SMILES 검증
    if not validate_smiles(smiles):
        print(f"Error: Invalid SMILES: {smiles}")
        return

    # 분석 수행
    if args.quick:
        props = calculate_molecular_properties(smiles)
        result = asdict(props)
    else:
        result = full_analysis(smiles, name)

    # 출력
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 텍스트 포맷
        print("=" * 60)
        print(f"Analysis: {result.get('name', 'Unknown')}")
        print("=" * 60)

        if args.quick:
            print(f"\nSMILES: {result['smiles']}")
            print(f"Formula: {result['formula']}")
            print(f"MW: {result['molecular_weight']} Da")
            print(f"LogP: {result['logp']}")
            print(f"PSA: {result['tpsa']} Å²")
            print(f"HBD: {result['hbd']}")
            print(f"HBA: {result['hba']}")
        else:
            summary = result.get("summary", {})
            print(f"\nFormula: {summary.get('formula')}")
            print(f"MW: {summary.get('mw')}")
            print(f"LogP: {summary.get('logp')}")
            print(f"PSA: {summary.get('psa')}")
            print(f"\nLipinski Rule of Five: {'PASS' if summary.get('lipinski_pass') else 'FAIL'}")
            print(f"Skin Penetration: {summary.get('penetration_class')}")
            print(f"Estimated HLB: {summary.get('hlb')}")

            # 상세 정보
            lipinski = result.get("lipinski_analysis", {})
            print(f"\nLipinski Details:")
            print(f"  - MW ≤ 500: {'PASS' if lipinski.get('mw_pass') else 'FAIL'}")
            print(f"  - LogP ≤ 5: {'PASS' if lipinski.get('logp_pass') else 'FAIL'}")
            print(f"  - HBD ≤ 5: {'PASS' if lipinski.get('hbd_pass') else 'FAIL'}")
            print(f"  - HBA ≤ 10: {'PASS' if lipinski.get('hba_pass') else 'FAIL'}")

            penetration = result.get("skin_penetration", {})
            print(f"\nSkin Penetration Details:")
            print(f"  - Score: {penetration.get('score')}/100")
            print(f"  - log Kp: {penetration.get('log_kp')}")

            hlb = result.get("hlb_estimation", {})
            print(f"\nHLB Estimation:")
            print(f"  - Griffin method: {hlb.get('hlb_griffin')}")
            print(f"  - Davies method: {hlb.get('hlb_davies')}")
            print(f"  - Classification: {hlb.get('classification')}")

    # 결과 저장
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
