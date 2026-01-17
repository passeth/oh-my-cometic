# 인용 스타일 상세 가이드

K-Dense 보고서 및 화장품 기술 문서를 위한 인용 스타일 가이드

## 1. Vancouver Style (권장)

### 개요

의학, 생명과학 분야 표준 인용 스타일. K-Dense 보고서의 기본 형식으로 권장.

### 기본 형식

```
저자. 제목. 저널명(약어). 연도;권(호):페이지. doi:DOI번호
```

### 저자 표기

| 저자 수 | 형식 | 예시 |
|--------|------|------|
| 1명 | 성 이니셜 | Kim HJ |
| 2-6명 | 쉼표로 구분 | Kim HJ, Lee SY, Park JH |
| 7명 이상 | 처음 3명 + et al. | Kim HJ, Lee SY, Park JH, et al. |

### 예시

**저널 논문**:
```
Kim HJ, Lee SY, Park JH. Double-blind randomized controlled trial
of 5% niacinamide for skin brightening. J Cosmet Dermatol.
2023;22(3):123-130. doi:10.1111/jcd.12345
```

**리뷰 논문**:
```
Chen AC, Damian DL. Nicotinamide and the skin. Australas J Dermatol.
2014;55(3):169-175. doi:10.1111/ajd.12163
```

**도서**:
```
Barel AO, Paye M, Maibach HI, editors. Handbook of Cosmetic Science
and Technology. 4th ed. Boca Raton: CRC Press; 2014.
```

**도서 챕터**:
```
Bissett DL. Niacinamide. In: Draelos ZD, editor. Cosmeceuticals.
3rd ed. Philadelphia: Elsevier; 2016. p. 145-152.
```

**웹사이트**:
```
U.S. Food and Drug Administration. Guidance for Industry:
Cosmetic Good Manufacturing Practices. 2013 [cited 2024 Jan 15].
Available from: https://www.fda.gov/cosmetics/...
```

---

## 2. APA 7th Edition

### 개요

심리학, 사회과학 분야 표준. 국제 학술지 투고 시 자주 사용.

### 기본 형식

```
저자. (연도). 제목. 저널명(이탤릭), 권(이탤릭)(호), 페이지. DOI URL
```

### 저자 표기

| 저자 수 | 본문 인용 | 참고문헌 목록 |
|--------|----------|--------------|
| 1명 | (Kim, 2023) | Kim, H. J. |
| 2명 | (Kim & Lee, 2023) | Kim, H. J., & Lee, S. Y. |
| 3명 이상 | (Kim et al., 2023) | Kim, H. J., Lee, S. Y., & Park, J. H. |
| 21명 이상 | 처음 19명 ... 마지막 저자 | - |

### 예시

**저널 논문**:
```
Kim, H. J., & Lee, S. Y. (2023). Double-blind randomized controlled
trial of 5% niacinamide for skin brightening. *Journal of Cosmetic
Dermatology*, *22*(3), 123-130. https://doi.org/10.1111/jcd.12345
```

**도서**:
```
Barel, A. O., Paye, M., & Maibach, H. I. (Eds.). (2014). *Handbook
of Cosmetic Science and Technology* (4th ed.). CRC Press.
```

**웹사이트**:
```
U.S. Food and Drug Administration. (2013, December 23). *Guidance
for Industry: Cosmetic Good Manufacturing Practices*.
https://www.fda.gov/cosmetics/...
```

---

## 3. ACS Style

### 개요

화학 분야 표준. 성분 화학적 특성 관련 문헌에 적합.

### 기본 형식

```
저자. 저널명(축약, 이탤릭) 연도(굵게), 권(이탤릭), 페이지.
```

### 저자 표기

- 세미콜론(;)으로 구분
- 이름 이니셜 뒤에 마침표

### 예시

**저널 논문**:
```
Kim, H. J.; Lee, S. Y.; Park, J. H. *J. Cosmet. Dermatol.*
**2023**, *22*, 123-130.
```

**도서**:
```
Barel, A. O.; Paye, M.; Maibach, H. I. *Handbook of Cosmetic
Science and Technology*, 4th ed.; CRC Press: Boca Raton, 2014.
```

---

## 4. Harvard Style

### 개요

영국, 호주 학술계 표준. 일부 국제 저널에서 사용.

### 기본 형식

```
저자 연도, '제목', 저널명(이탤릭), vol. 권, no. 호, pp. 페이지.
```

### 저자 표기

| 저자 수 | 본문 인용 | 참고문헌 |
|--------|----------|---------|
| 1명 | (Kim 2023) | Kim, HJ |
| 2명 | (Kim & Lee 2023) | Kim, HJ & Lee, SY |
| 3명 이상 | (Kim et al. 2023) | Kim, HJ et al. |

### 예시

**저널 논문**:
```
Kim, HJ & Lee, SY 2023, 'Double-blind randomized controlled trial
of 5% niacinamide for skin brightening', *Journal of Cosmetic
Dermatology*, vol. 22, no. 3, pp. 123-130.
```

---

## 5. K-Dense 보고서 인용 규칙

### 본문 내 인용

```markdown
방법 1: 문장 끝 번호
나이아신아마이드는 미백 효과가 있다 [1].

방법 2: 저자-연도 (학술적)
Kim et al. (2023)의 연구에서...

방법 3: 연속 번호
여러 연구에서 효과가 확인되었다 [1-3].

방법 4: 비연속 번호
다수의 연구가 이를 지지한다 [1,3,7].
```

### 참고문헌 섹션 구조

```markdown
## 참고문헌 (References)

### 임상 연구
1. Kim HJ, Lee SY. Title... J Cosmet Dermatol. 2023;22(3):123-130.
2. Park JY, et al. Title... Skin Res Technol. 2022;28(5):456-462.

### 기전 연구
3. Lee KS. Title... J Invest Dermatol. 2021;141(4):234-240.

### 리뷰 / 메타분석
4. Chen AC, Damian DL. Title... Australas J Dermatol. 2014;55(3):169-175.

### 규제 / 가이드라인
5. MFDS. 기능성화장품 심사에 관한 규정. 2023.
```

### 권장 인용 수

| 보고서 유형 | 권장 인용 수 | 최소 RCT |
|------------|------------|---------|
| 성분 분석 | 10-15건 | 2건 |
| 제품 기획 | 15-20건 | 3건 |
| 기능성 심사 | 20-25건 | 5건 |

---

## 6. 특수 출처 인용

### 규제 문서

**MFDS 고시**:
```
식품의약품안전처. 기능성화장품 심사에 관한 규정 [인터넷].
세종: 식품의약품안전처; 2023 [인용일 2024년 1월 15일].
https://www.mfds.go.kr/...
```

**EU 규정**:
```
European Commission. Regulation (EC) No 1223/2009 of the European
Parliament and of the Council on cosmetic products. Off J Eur Union.
2009;L342:59-209.
```

**FDA 가이던스**:
```
U.S. Food and Drug Administration. Guidance for Industry: Cosmetic
Good Manufacturing Practices. Silver Spring: FDA; 2013.
```

### 원료 데이터시트

```
BASF Care Chemicals. Technical Information: Niacinamide PC
[데이터시트]. Ludwigshafen: BASF; 2022.
```

### 특허

```
Smith J, inventor; Company A, assignee. Cosmetic composition
comprising niacinamide. United States patent US 1234567. 2020 Jan 15.
```

### 학위논문

```
Park SY. Effects of niacinamide on skin barrier function
[석사학위논문]. 서울: 서울대학교; 2022.
```

---

## 7. 스타일 비교 요약

| 요소 | Vancouver | APA 7th | ACS | Harvard |
|-----|-----------|---------|-----|---------|
| **저자 구분** | 쉼표 | 쉼표 & | 세미콜론 | & |
| **연도 위치** | 저널 뒤 | 저자 뒤 () | 저널 뒤 굵게 | 저자 뒤 |
| **저널명** | 약어 | 전체명 이탤릭 | 약어 이탤릭 | 전체명 이탤릭 |
| **권호** | 22(3) | *22*(3) | *22* | vol. 22, no. 3 |
| **DOI 형식** | doi:10.xxx | https://doi.org/10.xxx | 생략 가능 | DOI: 10.xxx |

---

## 8. 인용 관리 도구 호환성

| 도구 | 지원 스타일 | 내보내기 형식 |
|-----|------------|--------------|
| EndNote | 모든 스타일 | RIS, BibTeX, XML |
| Zotero | 모든 스타일 | RIS, BibTeX |
| Mendeley | 모든 스타일 | RIS, BibTeX |
| Reference Manager | Vancouver, APA, ACS, Harvard | RIS, BibTeX, JSON |

---

## 9. 체크리스트

### 인용 전 확인

- [ ] DOI 또는 PMID 포함
- [ ] 저자명 정확성
- [ ] 출판 연도 확인
- [ ] 저널명 약어 일관성

### 참고문헌 목록 확인

- [ ] 본문 인용과 목록 일치
- [ ] 알파벳/번호순 정렬
- [ ] 형식 일관성
- [ ] 접근 가능한 URL

### K-Dense 제출 전

- [ ] 최소 인용 수 충족
- [ ] RCT 인용 포함
- [ ] 최근 5년 내 문헌 포함
- [ ] 중복 인용 제거
