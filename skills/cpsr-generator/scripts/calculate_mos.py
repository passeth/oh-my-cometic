#!/usr/bin/env python3
"""
MoS (Margin of Safety) and SED (Systemic Exposure Dose) Calculator

Calculates safety margins for cosmetic ingredients based on:
- SCCS Notes of Guidance (11th revision)
- EU Cosmetics Regulation 1223/2009

Usage:
    python calculate_mos.py formula.json --product-type face_cream -o results.json
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


# SCCS Default Exposure Parameters (11th Revision)
EXPOSURE_PARAMS = {
    "body_lotion": {
        "amount_mg": 7820,
        "frequency": 1,
        "retention": 1.0,
        "surface_area_cm2": 15670,
        "description": "Body lotion/cream - whole body",
    },
    "face_cream": {
        "amount_mg": 800,
        "frequency": 2,
        "retention": 1.0,
        "surface_area_cm2": 565,
        "description": "Face cream - leave-on",
    },
    "hand_cream": {
        "amount_mg": 2160,
        "frequency": 2,
        "retention": 1.0,
        "surface_area_cm2": 860,
        "description": "Hand cream",
    },
    "lipstick": {
        "amount_mg": 57,
        "frequency": 2,
        "retention": 1.0,
        "surface_area_cm2": 3.5,
        "oral_exposure": True,
        "description": "Lipstick/lip gloss",
    },
    "eye_cream": {
        "amount_mg": 200,
        "frequency": 2,
        "retention": 1.0,
        "surface_area_cm2": 32,
        "description": "Eye cream/serum",
    },
    "shampoo": {
        "amount_mg": 10460,
        "frequency": 1,
        "retention": 0.01,
        "surface_area_cm2": 580,
        "description": "Shampoo - rinse-off",
    },
    "conditioner": {
        "amount_mg": 3920,
        "frequency": 1,
        "retention": 0.01,
        "surface_area_cm2": 580,
        "description": "Hair conditioner - rinse-off",
    },
    "shower_gel": {
        "amount_mg": 16200,
        "frequency": 1,
        "retention": 0.01,
        "surface_area_cm2": 17500,
        "description": "Shower gel/body wash",
    },
    "toothpaste": {
        "amount_mg": 138,
        "frequency": 2,
        "retention": 0.05,
        "surface_area_cm2": 50,
        "oral_exposure": True,
        "description": "Toothpaste",
    },
    "mouthwash": {
        "amount_mg": 32000,
        "frequency": 2,
        "retention": 0.1,
        "oral_exposure": True,
        "description": "Mouthwash",
    },
    "sunscreen_face": {
        "amount_mg": 800,
        "frequency": 2,
        "retention": 1.0,
        "surface_area_cm2": 565,
        "description": "Sunscreen - face only",
    },
    "sunscreen_body": {
        "amount_mg": 18000,
        "frequency": 1,
        "retention": 1.0,
        "surface_area_cm2": 17500,
        "description": "Sunscreen - whole body",
    },
    "serum": {
        "amount_mg": 500,
        "frequency": 2,
        "retention": 1.0,
        "surface_area_cm2": 565,
        "description": "Face serum/ampoule",
    },
    "toner": {
        "amount_mg": 1400,
        "frequency": 2,
        "retention": 1.0,
        "surface_area_cm2": 565,
        "description": "Face toner/lotion",
    },
    "essence": {
        "amount_mg": 600,
        "frequency": 2,
        "retention": 1.0,
        "surface_area_cm2": 565,
        "description": "Face essence",
    },
    "sheet_mask": {
        "amount_mg": 20000,
        "frequency": 0.14,  # ~1x per week
        "retention": 0.5,
        "surface_area_cm2": 565,
        "description": "Sheet mask (weekly use)",
    },
    "makeup_foundation": {
        "amount_mg": 510,
        "frequency": 1,
        "retention": 1.0,
        "surface_area_cm2": 565,
        "description": "Foundation/BB cream",
    },
    "mascara": {
        "amount_mg": 25,
        "frequency": 1,
        "retention": 1.0,
        "surface_area_cm2": 0.7,
        "description": "Mascara",
    },
    "nail_polish": {
        "amount_mg": 100,
        "frequency": 0.14,  # Weekly
        "retention": 1.0,
        "surface_area_cm2": 11,
        "description": "Nail polish",
    },
}

# Common NOAEL values (mg/kg bw/day) from CIR, SCCS, literature
# Extended database v2.0 - 150+ ingredients synchronized with noael_database.md
NOAEL_DATABASE = {
    # === PRESERVATIVES (40) ===
    "PHENOXYETHANOL": {
        "noael": 250,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 80,
    },
    "ETHYLHEXYLGLYCERIN": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "BENZYL_ALCOHOL": {
        "noael": 400,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 100,
    },
    "SODIUM_BENZOATE": {
        "noael": 500,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "POTASSIUM_SORBATE": {
        "noael": 1500,
        "study": "Oral, rat, 2-year",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "CHLORPHENESIN": {
        "noael": 250,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 100,
    },
    "METHYLISOTHIAZOLINONE": {
        "noael": 2.8,
        "study": "Oral, rat, 2-year",
        "source": "SCCS",
        "dermal_absorption": 100,
    },
    "BENZISOTHIAZOLINONE": {
        "noael": 9.4,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 100,
    },
    "CAPRYLYL_GLYCOL": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "1_2_HEXANEDIOL": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "PENTYLENE_GLYCOL": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "ECHA",
        "dermal_absorption": 100,
    },
    "CAPRYLHYDROXAMIC_ACID": {
        "noael": 100,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 100,
    },
    "METHYLPARABEN": {
        "noael": 1000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "ETHYLPARABEN": {
        "noael": 1000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "PROPYLPARABEN": {
        "noael": 1000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "BUTYLPARABEN": {
        "noael": 100,
        "study": "Oral, rat, chronic",
        "source": "SCCS",
        "dermal_absorption": 100,
    },
    "IODOPROPYNYL_BUTYLCARBAMATE": {
        "noael": 8,
        "study": "Oral, rat, chronic",
        "source": "SCCS",
        "dermal_absorption": 65,
    },
    "TRICLOSAN": {
        "noael": 12,
        "study": "Oral, rat, chronic",
        "source": "SCCS",
        "dermal_absorption": 14,
    },
    "CHLORHEXIDINE": {
        "noael": 15,
        "study": "Oral, rat, chronic",
        "source": "SCCS",
        "dermal_absorption": 1,
    },
    "PIROCTONE_OLAMINE": {
        "noael": 50,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 100,
    },
    "ZINC_PYRITHIONE": {
        "noael": 10,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 2,
    },
    "SORBIC_ACID": {
        "noael": 1500,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "BENZOIC_ACID": {
        "noael": 500,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "DEHYDROACETIC_ACID": {
        "noael": 100,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    # === HUMECTANTS & MOISTURIZERS (33) ===
    "GLYCERIN": {
        "noael": 10000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "BUTYLENE_GLYCOL": {
        "noael": 1500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "PROPYLENE_GLYCOL": {
        "noael": 2500,
        "study": "Oral, rat, 2-year",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "HEXYLENE_GLYCOL": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "DIPROPYLENE_GLYCOL": {
        "noael": 400,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "HYALURONIC_ACID": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 0.5,
    },
    "SODIUM_HYALURONATE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 0.5,
    },
    "SODIUM_PCA": {
        "noael": 2000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "UREA": {
        "noael": 3200,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "BETAINE": {
        "noael": 5000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "TREHALOSE": {
        "noael": 5000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "XYLITOL": {
        "noael": 5000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 80,
    },
    "SORBITOL": {
        "noael": 5000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "ERYTHRITOL": {
        "noael": 4000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "POLYGLUTAMIC_ACID": {
        "noael": 2000,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 2,
    },
    # === BRIGHTENING ACTIVES (25) ===
    "NIACINAMIDE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "ALPHA_ARBUTIN": {
        "noael": 450,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 50,
    },
    "ARBUTIN": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "KOJIC_ACID": {
        "noael": 125,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 10,
    },
    "TRANEXAMIC_ACID": {
        "noael": 300,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 20,
    },
    "ASCORBIC_ACID": {
        "noael": 1000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 8,
    },
    "ASCORBYL_GLUCOSIDE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 12,
    },
    "ETHYL_ASCORBIC_ACID": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 30,
    },
    "MAGNESIUM_ASCORBYL_PHOSPHATE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 15,
    },
    "SODIUM_ASCORBYL_PHOSPHATE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 18,
    },
    "GLUTATHIONE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 5,
    },
    "AZELAIC_ACID": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 3.5,
    },
    "PHENYLETHYL_RESORCINOL": {
        "noael": 50,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 40,
    },
    "4_BUTYLRESORCINOL": {
        "noael": 100,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 60,
    },
    "GLABRIDIN": {
        "noael": 100,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 30,
    },
    "DIPOTASSIUM_GLYCYRRHIZATE": {
        "noael": 300,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 25,
    },
    "CYSTEAMINE": {
        "noael": 50,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 70,
    },
    # === ANTI-AGING ACTIVES (50) ===
    "RETINOL": {
        "noael": 3,
        "study": "Oral, rat, developmental",
        "source": "SCCS",
        "dermal_absorption": 20,
    },
    "RETINYL_PALMITATE": {
        "noael": 3,
        "study": "Oral, rat, developmental",
        "source": "SCCS",
        "dermal_absorption": 10,
    },
    "RETINALDEHYDE": {
        "noael": 3,
        "study": "Oral, rat, developmental",
        "source": "SCCS",
        "dermal_absorption": 20,
    },
    "HYDROXYPINACOLONE_RETINOATE": {
        "noael": 100,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 15,
    },
    "BAKUCHIOL": {
        "noael": 100,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 40,
    },
    "ADENOSINE": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 30,
    },
    "ACETYL_HEXAPEPTIDE_8": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 5,
    },
    "PALMITOYL_TRIPEPTIDE_1": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 5,
    },
    "PALMITOYL_TETRAPEPTIDE_7": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 5,
    },
    "PALMITOYL_PENTAPEPTIDE_4": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 5,
    },
    "COPPER_TRIPEPTIDE_1": {
        "noael": 200,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 10,
    },
    "TOCOPHEROL": {
        "noael": 500,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "TOCOPHERYL_ACETATE": {
        "noael": 500,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 25,
    },
    "UBIQUINONE": {
        "noael": 1200,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 5,
    },
    "IDEBENONE": {
        "noael": 200,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 15,
    },
    "RESVERATROL": {
        "noael": 300,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 20,
    },
    "EPIGALLOCATECHIN_GALLATE": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "EFSA",
        "dermal_absorption": 12,
    },
    "ASTAXANTHIN": {
        "noael": 200,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 10,
    },
    "CARNOSINE": {
        "noael": 1500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 15,
    },
    "THIOCTIC_ACID": {
        "noael": 60,
        "study": "Oral, rat, 2-year",
        "source": "Literature",
        "dermal_absorption": 30,
    },
    "ERGOTHIONEINE": {
        "noael": 800,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 25,
    },
    "FERULIC_ACID": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 35,
    },
    "MADECASSOSIDE": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 30,
    },
    "ASIATICOSIDE": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 25,
    },
    "ECTOIN": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 50,
    },
    "FULLERENES": {
        "noael": 25,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 3,
    },
    # === ACIDS & EXFOLIANTS (25) ===
    "GLYCOLIC_ACID": {
        "noael": 150,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "LACTIC_ACID": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "MALIC_ACID": {
        "noael": 700,
        "study": "Oral, rat, 90-day",
        "source": "JECFA",
        "dermal_absorption": 40,
    },
    "TARTARIC_ACID": {
        "noael": 500,
        "study": "Oral, rat, chronic",
        "source": "JECFA",
        "dermal_absorption": 35,
    },
    "CITRIC_ACID": {
        "noael": 1200,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 30,
    },
    "MANDELIC_ACID": {
        "noael": 200,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 25,
    },
    "SALICYLIC_ACID": {
        "noael": 50,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 25,
    },
    "BETAINE_SALICYLATE": {
        "noael": 100,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 15,
    },
    "PHYTIC_ACID": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 5,
    },
    "LACTOBIONIC_ACID": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 2,
    },
    "GLUCONOLACTONE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 3,
    },
    "PYRUVIC_ACID": {
        "noael": 200,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 60,
    },
    "PAPAIN": {
        "noael": 100,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 1,
    },
    "BROMELAIN": {
        "noael": 200,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 1,
    },
    "RETINOIC_ACID": {
        "noael": 1,
        "study": "Oral, rat, developmental",
        "source": "SCCS",
        "dermal_absorption": 30,
    },
    # === SOOTHING & ANTI-INFLAMMATORY (24) ===
    "CENTELLA_ASIATICA_EXTRACT": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 50,
    },
    "ASIATIC_ACID": {
        "noael": 300,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 40,
    },
    "MADECASSIC_ACID": {
        "noael": 300,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 40,
    },
    "ALLANTOIN": {
        "noael": 2000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 60,
    },
    "BISABOLOL": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "RIFM",
        "dermal_absorption": 70,
    },
    "PANTHENOL": {
        "noael": 10000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "PANTOTHENIC_ACID": {
        "noael": 10000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 40,
    },
    "CHAMOMILLA_RECUTITA_FLOWER_EXTRACT": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 45,
    },
    "AZULENE": {
        "noael": 200,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 55,
    },
    "ALOE_BARBADENSIS_LEAF_EXTRACT": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 35,
    },
    "CALENDULA_OFFICINALIS_FLOWER_EXTRACT": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 40,
    },
    "GLYCYRRHIZA_GLABRA_ROOT_EXTRACT": {
        "noael": 200,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 35,
    },
    "CAMELLIA_SINENSIS_LEAF_EXTRACT": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 30,
    },
    "HOUTTUYNIA_CORDATA_EXTRACT": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 35,
    },
    "ARTEMISIA_PRINCEPS_LEAF_EXTRACT": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 40,
    },
    "PORTULACA_OLERACEA_EXTRACT": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 30,
    },
    "BETA_GLUCAN": {
        "noael": 2000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 15,
    },
    # === ANTIOXIDANTS (36) ===
    "TOCOTRIENOLS": {
        "noael": 120,
        "study": "Oral, rat, 13-week",
        "source": "Literature",
        "dermal_absorption": 35,
    },
    "ASCORBYL_PALMITATE": {
        "noael": 750,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 15,
    },
    "LYCOPENE": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 8,
    },
    "BETA_CAROTENE": {
        "noael": 250,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 5,
    },
    "SUPEROXIDE_DISMUTASE": {
        "noael": 2000,
        "study": "Oral, rat, acute",
        "source": "CIR",
        "dermal_absorption": 2,
    },
    "CATALASE": {
        "noael": 2000,
        "study": "Oral, rat, acute",
        "source": "CIR",
        "dermal_absorption": 1,
    },
    "ACETYL_CYSTEINE": {
        "noael": 250,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 20,
    },
    "VITIS_VINIFERA_SEED_EXTRACT": {
        "noael": 1500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 18,
    },
    "PINUS_PINASTER_BARK_EXTRACT": {
        "noael": 1000,
        "study": "Oral, human, clinical",
        "source": "Literature",
        "dermal_absorption": 15,
    },
    "SILYMARIN": {
        "noael": 300,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 10,
    },
    "QUERCETIN": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 12,
    },
    "CURCUMIN": {
        "noael": 250,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 8,
    },
    "HYDROXYTYROSOL": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 45,
    },
    "TETRAHEXYLDECYL_ASCORBATE": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 60,
    },
    "ROSMARINUS_OFFICINALIS_LEAF_EXTRACT": {
        "noael": 180,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 25,
    },
    # === SURFACTANTS & EMULSIFIERS (27) ===
    "SODIUM_LAURYL_SULFATE": {
        "noael": 130,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "SODIUM_LAURETH_SULFATE": {
        "noael": 100,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "COCAMIDOPROPYL_BETAINE": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "SODIUM_COCOYL_ISETHIONATE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "DECYL_GLUCOSIDE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "COCO_GLUCOSIDE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "LAURYL_GLUCOSIDE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "SODIUM_COCOYL_GLUTAMATE": {
        "noael": 2000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 80,
    },
    "POLYSORBATE_20": {
        "noael": 1500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "POLYSORBATE_80": {
        "noael": 1500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "PEG_40_HYDROGENATED_CASTOR_OIL": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 20,
    },
    "CETEARYL_ALCOHOL": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "CETYL_ALCOHOL": {
        "noael": 2000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "STEARYL_ALCOHOL": {
        "noael": 2000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "GLYCERYL_STEARATE": {
        "noael": 1500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "SORBITAN_OLEATE": {
        "noael": 2500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 20,
    },
    # === OILS & EMOLLIENTS (34) ===
    "SQUALANE": {
        "noael": 2000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "SQUALENE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 45,
    },
    "SIMMONDSIA_CHINENSIS_SEED_OIL": {
        "noael": 2500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 20,
    },
    "ARGANIA_SPINOSA_KERNEL_OIL": {
        "noael": 2000,
        "study": "Oral, rat, estimated",
        "source": "Literature",
        "dermal_absorption": 35,
    },
    "ROSA_CANINA_SEED_OIL": {
        "noael": 1500,
        "study": "Oral, rat, estimated",
        "source": "Literature",
        "dermal_absorption": 40,
    },
    "CAMELLIA_JAPONICA_SEED_OIL": {
        "noael": 2500,
        "study": "Oral, rat, estimated",
        "source": "Literature",
        "dermal_absorption": 30,
    },
    "PRUNUS_AMYGDALUS_DULCIS_OIL": {
        "noael": 2000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 25,
    },
    "PERSEA_GRATISSIMA_OIL": {
        "noael": 2000,
        "study": "Oral, rat, estimated",
        "source": "CIR",
        "dermal_absorption": 35,
    },
    "OLEA_EUROPAEA_FRUIT_OIL": {
        "noael": 4000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 30,
    },
    "COCOS_NUCIFERA_OIL": {
        "noael": 2500,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 20,
    },
    "CAPRYLIC_CAPRIC_TRIGLYCERIDE": {
        "noael": 5000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 15,
    },
    "BUTYROSPERMUM_PARKII_BUTTER": {
        "noael": 2000,
        "study": "Oral, rat, estimated",
        "source": "CIR",
        "dermal_absorption": 15,
    },
    "DIMETHICONE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 0.5,
    },
    "CYCLOPENTASILOXANE": {
        "noael": 500,
        "study": "Inhalation, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 0.5,
    },
    "ISOPROPYL_MYRISTATE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 60,
    },
    "ISOPROPYL_PALMITATE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    "PARAFFINUM_LIQUIDUM": {
        "noael": 2000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 0.5,
    },
    "PETROLATUM": {
        "noael": 2000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 0.1,
    },
    "HELIANTHUS_ANNUUS_SEED_OIL": {
        "noael": 4000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 35,
    },
    "VITIS_VINIFERA_SEED_OIL": {
        "noael": 2000,
        "study": "Oral, rat, estimated",
        "source": "CIR",
        "dermal_absorption": 40,
    },
    "OENOTHERA_BIENNIS_OIL": {
        "noael": 2000,
        "study": "Oral, human, clinical",
        "source": "Literature",
        "dermal_absorption": 45,
    },
    "RICINUS_COMMUNIS_SEED_OIL": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 20,
    },
    "LANOLIN": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 30,
    },
    # === CERAMIDES & LIPIDS ===
    "CERAMIDE_NP": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 10,
    },
    "CERAMIDE_AP": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 10,
    },
    "CERAMIDE_EOP": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 10,
    },
    "PHYTOSPHINGOSINE": {
        "noael": 500,
        "study": "Oral, rat, 90-day",
        "source": "Literature",
        "dermal_absorption": 20,
    },
    "CHOLESTEROL": {
        "noael": 1000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 50,
    },
    # === POLYMERS & FILM FORMERS ===
    "CARBOMER": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 0,
    },
    "XANTHAN_GUM": {
        "noael": 1000,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 0,
    },
    "HYDROXYETHYLCELLULOSE": {
        "noael": 5000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 0,
    },
    "SODIUM_POLYACRYLATE": {
        "noael": 1000,
        "study": "Oral, rat, 90-day",
        "source": "CIR",
        "dermal_absorption": 0,
    },
    # === CHELATING AGENTS ===
    "DISODIUM_EDTA": {
        "noael": 250,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    "TETRASODIUM_EDTA": {
        "noael": 250,
        "study": "Oral, rat, chronic",
        "source": "CIR",
        "dermal_absorption": 100,
    },
    # === UV FILTERS (Reference) ===
    "ETHYLHEXYL_METHOXYCINNAMATE": {
        "noael": 200,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 100,
    },
    "BUTYL_METHOXYDIBENZOYLMETHANE": {
        "noael": 100,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 100,
    },
    "OCTOCRYLENE": {
        "noael": 62,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 10,
    },
    "HOMOSALATE": {
        "noael": 80,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 5,
    },
    "BENZOPHENONE_3": {
        "noael": 200,
        "study": "Oral, rat, 90-day",
        "source": "SCCS",
        "dermal_absorption": 10,
    },
}


@dataclass
class SEDResult:
    """Result of SED calculation for an ingredient"""

    ingredient: str
    concentration_pct: float
    sed_mg_kg_day: float
    dermal_absorption_pct: float
    daily_exposure_mg: float


@dataclass
class MoSResult:
    """Result of MoS calculation for an ingredient"""

    ingredient: str
    cas_number: Optional[str]
    concentration_pct: float
    sed_mg_kg_day: float
    noael_mg_kg_day: float
    noael_source: str
    mos: float
    status: str  # "PASS", "REVIEW", "FAIL"
    notes: str


def normalize_ingredient_name(name: str) -> str:
    """Normalize ingredient name for database lookup"""
    normalized = name.upper().strip()
    normalized = normalized.replace(" ", "_")
    normalized = normalized.replace("-", "_")
    normalized = normalized.replace(",", "")
    return normalized


def get_dermal_absorption(
    ingredient: str, molecular_weight: Optional[float] = None
) -> float:
    """
    Get dermal absorption percentage.

    Priority:
    1. Database value if available
    2. MW-based default (>500 Da = 50%, <500 Da = 100%)
    3. Conservative default (100%)
    """
    normalized = normalize_ingredient_name(ingredient)

    if normalized in NOAEL_DATABASE:
        return NOAEL_DATABASE[normalized].get("dermal_absorption", 100)

    if molecular_weight:
        return 50.0 if molecular_weight > 500 else 100.0

    return 100.0  # Conservative default


def calculate_sed(
    concentration_pct: float,
    product_params: Dict[str, Any],
    dermal_absorption_pct: float,
    body_weight_kg: float = 60.0,
) -> float:
    """
    Calculate Systemic Exposure Dose (SED).

    SED = (A × C/100 × DA/100 × F × RF) / BW

    Where:
    - A = Amount applied (mg/day)
    - C = Concentration (%)
    - DA = Dermal absorption (%)
    - F = Frequency (per day)
    - RF = Retention factor
    - BW = Body weight (kg)
    """
    amount_mg = product_params["amount_mg"]
    frequency = product_params["frequency"]
    retention = product_params.get("retention", 1.0)

    # Calculate daily exposure
    daily_exposure_mg = amount_mg * (concentration_pct / 100) * frequency * retention

    # Apply dermal absorption
    absorbed_mg = daily_exposure_mg * (dermal_absorption_pct / 100)

    # Calculate SED
    sed = absorbed_mg / body_weight_kg

    return sed


def calculate_mos(sed: float, noael: float) -> float:
    """
    Calculate Margin of Safety.

    MoS = NOAEL / SED

    MoS >= 100 is generally considered safe.
    """
    if sed <= 0:
        return float("inf")
    return noael / sed


def get_mos_status(mos: float) -> str:
    """Determine pass/fail status based on MoS value"""
    if mos >= 100:
        return "PASS"
    elif mos >= 50:
        return "REVIEW"
    else:
        return "FAIL"


def calculate_ingredient_safety(
    ingredient: str,
    concentration_pct: float,
    product_type: str,
    cas_number: Optional[str] = None,
    custom_noael: Optional[float] = None,
    custom_dermal_absorption: Optional[float] = None,
    body_weight_kg: float = 60.0,
) -> MoSResult:
    """
    Calculate full safety assessment for an ingredient.

    Returns MoSResult with SED, NOAEL, MoS, and status.
    """
    normalized = normalize_ingredient_name(ingredient)
    product_params = EXPOSURE_PARAMS.get(product_type, EXPOSURE_PARAMS["face_cream"])

    # Get dermal absorption
    if custom_dermal_absorption is not None:
        dermal_absorption = custom_dermal_absorption
    else:
        dermal_absorption = get_dermal_absorption(ingredient)

    # Calculate SED
    sed = calculate_sed(
        concentration_pct=concentration_pct,
        product_params=product_params,
        dermal_absorption_pct=dermal_absorption,
        body_weight_kg=body_weight_kg,
    )

    # Get NOAEL
    noael = custom_noael
    noael_source = "User provided"

    if noael is None:
        if normalized in NOAEL_DATABASE:
            noael = NOAEL_DATABASE[normalized]["noael"]
            noael_source = f"{NOAEL_DATABASE[normalized]['source']} - {NOAEL_DATABASE[normalized]['study']}"
        else:
            # No NOAEL available
            return MoSResult(
                ingredient=ingredient,
                cas_number=cas_number,
                concentration_pct=concentration_pct,
                sed_mg_kg_day=sed,
                noael_mg_kg_day=0,
                noael_source="NOT AVAILABLE",
                mos=0,
                status="DATA NEEDED",
                notes="NOAEL data not found. Please provide NOAEL from CIR, SCCS, or other authoritative source.",
            )

    # Calculate MoS
    mos = calculate_mos(sed, noael)
    status = get_mos_status(mos)

    # Generate notes
    notes = ""
    if status == "PASS":
        notes = f"MoS of {mos:.0f} exceeds safety threshold of 100."
    elif status == "REVIEW":
        notes = (
            f"MoS of {mos:.0f} is below 100. Additional justification may be required."
        )
    else:
        notes = f"MoS of {mos:.0f} is below 50. Consider reducing concentration or providing additional safety data."

    return MoSResult(
        ingredient=ingredient,
        cas_number=cas_number,
        concentration_pct=concentration_pct,
        sed_mg_kg_day=round(sed, 6),
        noael_mg_kg_day=noael,
        noael_source=noael_source,
        mos=round(mos, 1) if mos != float("inf") else float("inf"),
        status=status,
        notes=notes,
    )


def process_formula(
    formula: List[Dict[str, Any]], product_type: str, body_weight_kg: float = 60.0
) -> Dict[str, Any]:
    """
    Process complete formula and generate safety assessment.

    Args:
        formula: List of ingredients with concentrations
        product_type: Product type key from EXPOSURE_PARAMS
        body_weight_kg: Body weight for calculations

    Returns:
        Dictionary with all safety calculations
    """
    results = []
    summary = {
        "total_ingredients": 0,
        "assessed": 0,
        "passed": 0,
        "review_needed": 0,
        "failed": 0,
        "data_needed": 0,
    }

    for ingredient in formula:
        inci_name = ingredient.get("inci_name", ingredient.get("name", ""))
        concentration = ingredient.get("concentration", ingredient.get("conc", 0))
        cas_number = ingredient.get("cas_number", ingredient.get("cas", None))

        if not inci_name or concentration <= 0:
            continue

        summary["total_ingredients"] += 1

        result = calculate_ingredient_safety(
            ingredient=inci_name,
            concentration_pct=concentration,
            product_type=product_type,
            cas_number=cas_number,
            body_weight_kg=body_weight_kg,
        )

        results.append(asdict(result))

        if result.status == "PASS":
            summary["passed"] += 1
            summary["assessed"] += 1
        elif result.status == "REVIEW":
            summary["review_needed"] += 1
            summary["assessed"] += 1
        elif result.status == "FAIL":
            summary["failed"] += 1
            summary["assessed"] += 1
        else:
            summary["data_needed"] += 1

    product_params = EXPOSURE_PARAMS.get(product_type, EXPOSURE_PARAMS["face_cream"])

    return {
        "timestamp": datetime.now().isoformat(),
        "product_type": product_type,
        "product_description": product_params["description"],
        "exposure_parameters": {
            "amount_mg_day": product_params["amount_mg"],
            "frequency_per_day": product_params["frequency"],
            "retention_factor": product_params["retention"],
            "body_weight_kg": body_weight_kg,
        },
        "summary": summary,
        "results": results,
    }


def generate_report(assessment: Dict[str, Any]) -> str:
    """Generate markdown report from assessment results"""
    report = []

    report.append("# Margin of Safety (MoS) Assessment Report")
    report.append(f"\n**Generated**: {assessment['timestamp']}")
    report.append(f"**Product Type**: {assessment['product_description']}")

    report.append("\n## Exposure Parameters (SCCS Default Values)")
    params = assessment["exposure_parameters"]
    report.append(f"- Amount applied: {params['amount_mg_day']} mg/day")
    report.append(f"- Frequency: {params['frequency_per_day']}x per day")
    report.append(f"- Retention factor: {params['retention_factor']}")
    report.append(f"- Body weight: {params['body_weight_kg']} kg")

    report.append("\n## Summary")
    summary = assessment["summary"]
    report.append(f"- Total ingredients: {summary['total_ingredients']}")
    report.append(f"- Assessed: {summary['assessed']}")
    report.append(f"- ✓ Passed (MoS ≥ 100): {summary['passed']}")
    report.append(f"- ⚠ Review needed (50 ≤ MoS < 100): {summary['review_needed']}")
    report.append(f"- ✗ Failed (MoS < 50): {summary['failed']}")
    report.append(f"- Data needed: {summary['data_needed']}")

    report.append("\n## Detailed Results")
    report.append(
        "\n| Ingredient | Conc. (%) | SED (mg/kg/day) | NOAEL | MoS | Status |"
    )
    report.append("|------------|-----------|-----------------|-------|-----|--------|")

    for result in assessment["results"]:
        status_icon = {"PASS": "✓", "REVIEW": "⚠", "FAIL": "✗", "DATA NEEDED": "?"}
        icon = status_icon.get(result["status"], "?")

        mos_str = f"{result['mos']:.0f}" if result["mos"] != float("inf") else "∞"
        noael_str = (
            f"{result['noael_mg_kg_day']}" if result["noael_mg_kg_day"] > 0 else "N/A"
        )

        report.append(
            f"| {result['ingredient']} | {result['concentration_pct']} | "
            f"{result['sed_mg_kg_day']:.4f} | {noael_str} | {mos_str} | {icon} {result['status']} |"
        )

    # Detailed ingredient sections for failed/review items
    problem_items = [
        r
        for r in assessment["results"]
        if r["status"] in ["FAIL", "REVIEW", "DATA NEEDED"]
    ]

    if problem_items:
        report.append("\n## Items Requiring Attention")

        for item in problem_items:
            report.append(f"\n### {item['ingredient']}")
            report.append(f"- **Status**: {item['status']}")
            report.append(f"- **Concentration**: {item['concentration_pct']}%")
            report.append(f"- **SED**: {item['sed_mg_kg_day']:.6f} mg/kg/day")

            if item["noael_mg_kg_day"] > 0:
                report.append(f"- **NOAEL**: {item['noael_mg_kg_day']} mg/kg/day")
                report.append(f"- **NOAEL Source**: {item['noael_source']}")
                report.append(f"- **MoS**: {item['mos']:.1f}")

            report.append(f"- **Notes**: {item['notes']}")

    report.append("\n---")
    report.append(
        "*This report was generated automatically and should be reviewed by a qualified Safety Assessor.*"
    )

    return "\n".join(report)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Calculate Margin of Safety (MoS) for cosmetic ingredients"
    )
    parser.add_argument("formula", help="Path to formula file (JSON or CSV)")
    parser.add_argument(
        "--product-type",
        "-t",
        default="face_cream",
        choices=list(EXPOSURE_PARAMS.keys()),
        help="Product type for exposure parameters",
    )
    parser.add_argument(
        "--body-weight",
        "-w",
        type=float,
        default=60.0,
        help="Body weight in kg (default: 60)",
    )
    parser.add_argument("--output", "-o", help="Output file path (JSON)")
    parser.add_argument(
        "--report", "-r", help="Generate markdown report to specified path"
    )
    parser.add_argument(
        "--list-products", action="store_true", help="List available product types"
    )

    args = parser.parse_args()

    if args.list_products:
        print("Available product types:")
        for key, params in EXPOSURE_PARAMS.items():
            print(f"  {key}: {params['description']}")
        return 0

    # Load formula
    formula_path = Path(args.formula)

    if not formula_path.exists():
        print(f"Error: Formula file not found: {args.formula}")
        return 1

    try:
        if formula_path.suffix.lower() == ".json":
            with open(formula_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "formula" in data:
                    formula = data["formula"]
                elif isinstance(data, list):
                    formula = data
                else:
                    print("Error: Invalid JSON format")
                    return 1
        elif formula_path.suffix.lower() == ".csv":
            import csv

            formula = []
            with open(formula_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    formula.append(
                        {
                            "inci_name": row.get("inci_name", row.get("name", "")),
                            "concentration": float(
                                row.get("concentration", row.get("conc", 0))
                            ),
                            "cas_number": row.get("cas_number", row.get("cas", None)),
                        }
                    )
        else:
            print(f"Error: Unsupported file format: {formula_path.suffix}")
            return 1
    except Exception as e:
        print(f"Error loading formula: {e}")
        return 1

    # Process formula
    print(f"Processing {len(formula)} ingredients...")
    assessment = process_formula(
        formula=formula, product_type=args.product_type, body_weight_kg=args.body_weight
    )

    # Output results
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(assessment, f, indent=2, ensure_ascii=False)
        print(f"Results saved to: {args.output}")

    if args.report:
        report = generate_report(assessment)
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to: {args.report}")

    # Print summary
    summary = assessment["summary"]
    print(f"\n{'=' * 50}")
    print("ASSESSMENT SUMMARY")
    print(f"{'=' * 50}")
    print(f"Product Type: {assessment['product_description']}")
    print(f"Total Ingredients: {summary['total_ingredients']}")
    print(f"✓ Passed: {summary['passed']}")
    print(f"⚠ Review Needed: {summary['review_needed']}")
    print(f"✗ Failed: {summary['failed']}")
    print(f"? Data Needed: {summary['data_needed']}")

    if summary["failed"] > 0:
        return 2
    elif summary["review_needed"] > 0 or summary["data_needed"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
